#!/usr/bin/env python3
"""
Nautilus Backup Extension
Adds right-click backup options to Nautilus file manager
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
from gi.repository import Nautilus, GObject, Gtk, Gio
import subprocess
import tarfile

class BackupExtension(GObject.GObject, Nautilus.MenuProvider):
    """Nautilus extension for easy file/folder backups"""
    
    def __init__(self):
        super().__init__()
        
        # Load backup folder from config or use default
        config_dir = Path.home() / ".config" / "nautilus-backup"
        config_file = config_dir / "config.txt"
        
        if config_file.exists():
            try:
                saved_path = config_file.read_text().strip()
                if saved_path:  # Check not empty
                    self.backup_folder = Path(saved_path)
                else:
                    self.backup_folder = Path.home() / "Backups"
            except Exception:
                # If config is corrupted, use default
                self.backup_folder = Path.home() / "Backups"
        else:
            self.backup_folder = Path.home() / "Backups"
        
        # Create backup folder if it doesn't exist
        self.backup_folder.mkdir(parents=True, exist_ok=True)
    
    def get_file_items(self, files):
        """Add backup menu items to right-click context menu"""
        if len(files) == 0:
            return []
        
        # Create main backup menu
        backup_menu = Nautilus.Menu()
        backup_item = Nautilus.MenuItem(
            name='BackupExtension::Backup',
            label='🔄 Backup',
            tip='Backup options for selected file(s)'
        )
        backup_item.set_submenu(backup_menu)
        
        # Quick Backup (same folder with timestamp)
        quick_item = Nautilus.MenuItem(
            name='BackupExtension::QuickBackup',
            label='⚡ Quick Backup (Same Folder)',
            tip='Create timestamped backup in same folder'
        )
        quick_item.connect('activate', self.quick_backup, files)
        backup_menu.append_item(quick_item)
        
        # Backup As... (choose name and location)
        backup_as_item = Nautilus.MenuItem(
            name='BackupExtension::BackupAs',
            label='💾 Backup As...',
            tip='Choose backup name and location'
        )
        backup_as_item.connect('activate', self.backup_as, files)
        backup_menu.append_item(backup_as_item)
        
        # Backup to ~/Backups
        backup_home_item = Nautilus.MenuItem(
            name='BackupExtension::BackupToHome',
            label='🗂️ Backup to ~/Backups',
            tip='Save backup to ~/Backups folder'
        )
        backup_home_item.connect('activate', self.backup_to_home, files)
        backup_menu.append_item(backup_home_item)
        
        # Add separator
        separator = Nautilus.MenuItem(
            name='BackupExtension::Separator1',
            label='─────────────────',
            tip=''
        )
        backup_menu.append_item(separator)
        
        # Settings
        settings_item = Nautilus.MenuItem(
            name='BackupExtension::Settings',
            label='⚙️ Backup Settings',
            tip='Configure backup options'
        )
        settings_item.connect('activate', self.show_settings, files)
        backup_menu.append_item(settings_item)
        
        return [backup_item]
    
    def get_background_items(self, current_folder):
        """No background items"""
        return []
    
    def _get_file_path(self, file_info):
        """Convert Nautilus file info to path"""
        uri = file_info.get_uri()
        return Path(unquote(urlparse(uri).path))
    
    def _generate_backup_name(self, original_path):
        """Generate timestamped backup filename"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        if original_path.is_file():
            # For files: filename_backup_2024-12-22_14-30-00.ext
            stem = original_path.stem
            suffix = original_path.suffix
            backup_name = f"{stem}_backup_{timestamp}{suffix}"
        else:
            # For folders: foldername_backup_2024-12-22_14-30-00.tar.gz
            backup_name = f"{original_path.name}_backup_{timestamp}.tar.gz"
        
        return backup_name
    
    def _create_backup(self, source_path, dest_path):
        """Create backup of file or folder"""
        try:
            if source_path.is_file():
                # Copy file
                shutil.copy2(source_path, dest_path)
            else:
                # Create tar.gz of folder
                with tarfile.open(dest_path, "w:gz") as tar:
                    tar.add(source_path, arcname=source_path.name)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def _show_notification(self, title, message, success=True):
        """Show desktop notification"""
        try:
            icon = "emblem-default" if success else "dialog-error"
            subprocess.run([
                'notify-send',
                '-i', icon,
                '-t', '3000',
                title,
                message
            ], check=False)
        except:
            pass
    
    def quick_backup(self, menu, files):
        """Quick backup in same folder with timestamp"""
        success_count = 0
        error_count = 0
        last_dest_path = None
        
        for file_info in files:
            source_path = self._get_file_path(file_info)
            backup_name = self._generate_backup_name(source_path)
            dest_path = source_path.parent / backup_name
            
            success, error = self._create_backup(source_path, dest_path)
            
            if success:
                success_count += 1
                last_dest_path = dest_path
            else:
                error_count += 1
                self._show_notification(
                    "Backup Failed",
                    f"Failed to backup {source_path.name}\n{error}",
                    success=False
                )
        
        if success_count > 0:
            if success_count == 1 and last_dest_path:
                msg = f"Backed up to:\n{last_dest_path.parent}"
            else:
                msg = f"{success_count} file(s) backed up"
            
            self._show_notification("Backup Complete ✓", msg)
    
    def backup_as(self, menu, files):
        """Backup with custom name and location"""
        if len(files) != 1:
            self._show_error_dialog(
                "Multiple Selection",
                "Please select only one file/folder for 'Backup As...'"
            )
            return
        
        source_path = self._get_file_path(files[0])
        
        # Create file chooser dialog
        dialog = Gtk.FileChooserDialog(
            title="Backup As...",
            parent=None,
            action=Gtk.FileChooserAction.SAVE,
            buttons=(
                "_Cancel", Gtk.ResponseType.CANCEL,
                "_Save", Gtk.ResponseType.OK
            )
        )
        dialog.set_modal(True)
        
        # Set default name
        backup_name = self._generate_backup_name(source_path)
        dialog.set_current_name(backup_name)
        dialog.set_current_folder(str(source_path.parent))
        
        # Add file filters
        if source_path.is_file():
            filter_any = Gtk.FileFilter()
            filter_any.set_name("All files")
            filter_any.add_pattern("*")
            dialog.add_filter(filter_any)
        
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            dest_path = Path(dialog.get_filename())
            dialog.destroy()
            
            success, error = self._create_backup(source_path, dest_path)
            
            if success:
                self._show_notification(
                    "Backup Complete ✓",
                    f"Backed up to:\n{dest_path}"
                )
            else:
                self._show_error_dialog("Backup Failed", error)
        else:
            dialog.destroy()
    
    def backup_to_home(self, menu, files):
        """Backup to ~/Backups folder"""
        success_count = 0
        error_count = 0
        last_dest_path = None
        
        for file_info in files:
            source_path = self._get_file_path(file_info)
            backup_name = self._generate_backup_name(source_path)
            dest_path = self.backup_folder / backup_name
            
            success, error = self._create_backup(source_path, dest_path)
            
            if success:
                success_count += 1
                last_dest_path = dest_path
            else:
                error_count += 1
                self._show_notification(
                    "Backup Failed",
                    f"Failed to backup {source_path.name}\n{error}",
                    success=False
                )
        
        if success_count > 0:
            if success_count == 1:
                msg = f"Backed up to ~/Backups"
            else:
                msg = f"{success_count} file(s) backed up to ~/Backups"
            
            self._show_notification("Backup Complete ✓", msg)
            
            # Optionally open backup folder
            # subprocess.Popen(['nautilus', str(self.backup_folder)])
    
    def show_settings(self, menu, files):
        """Show settings dialog"""
        dialog = Gtk.Dialog(
            title="Backup Settings",
            parent=None,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
        )
        dialog.set_default_size(400, 300)
        dialog.set_position(Gtk.WindowPosition.CENTER)
        
        content = dialog.get_content_area()
        
        # Header
        header_label = Gtk.Label()
        header_label.set_markup("<b>Backup Extension Settings</b>")
        header_label.set_margin_top(10)
        header_label.set_margin_bottom(10)
        content.pack_start(header_label, False, False, 0)
        
        # Backup folder location
        folder_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        folder_box.set_margin_start(10)
        folder_box.set_margin_end(10)
        folder_box.set_margin_top(10)
        
        folder_label = Gtk.Label(label="Backup Folder:")
        folder_label.set_width_chars(15)
        folder_label.set_xalign(0)
        folder_box.pack_start(folder_label, False, False, 0)
        
        folder_entry = Gtk.Entry()
        folder_entry.set_text(str(self.backup_folder))
        folder_entry.set_editable(False)
        folder_box.pack_start(folder_entry, True, True, 0)
        
        browse_button = Gtk.Button(label="Browse")
        browse_button.connect("clicked", self._browse_backup_folder, folder_entry)
        folder_box.pack_start(browse_button, False, False, 0)
        
        content.pack_start(folder_box, False, False, 0)
        
        # Info section
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        info_box.set_margin_start(10)
        info_box.set_margin_end(10)
        info_box.set_margin_top(20)
        
        info_label = Gtk.Label()
        info_label.set_markup("<b>Features:</b>")
        info_label.set_xalign(0)
        info_box.pack_start(info_label, False, False, 0)
        
        features = [
            "⚡ Quick Backup - Creates timestamped backup in same folder",
            "💾 Backup As - Choose custom name and location",
            "🗂️ Backup to ~/Backups - Organized backup folder",
            "📁 Works with files and folders (folders → .tar.gz)",
            "🔔 Desktop notifications for status",
        ]
        
        for feature in features:
            label = Gtk.Label(label=feature)
            label.set_xalign(0)
            label.set_margin_start(10)
            info_box.pack_start(label, False, False, 0)
        
        content.pack_start(info_box, False, False, 0)
        
        # Version info
        version_label = Gtk.Label()
        version_label.set_markup("<small>Nautilus Backup Extension v1.0.1</small>")
        version_label.set_margin_top(20)
        version_label.set_margin_bottom(10)
        content.pack_start(version_label, False, False, 0)
        
        # Buttons
        dialog.add_button("Open Backups Folder", 1)
        dialog.add_button("_Close", Gtk.ResponseType.CLOSE)
        
        dialog.show_all()
        response = dialog.run()
        
        if response == 1:
            # Open backups folder
            subprocess.Popen(['nautilus', str(self.backup_folder)])
        
        dialog.destroy()
    
    def _browse_backup_folder(self, button, entry):
        """Browse for backup folder"""
        dialog = Gtk.FileChooserDialog(
            title="Select Backup Folder",
            parent=None,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(
                "_Cancel", Gtk.ResponseType.CANCEL,
                "_Open", Gtk.ResponseType.OK
            )
        )
        dialog.set_modal(True)
        dialog.set_current_folder(str(self.backup_folder))
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            new_folder = Path(dialog.get_filename())
            self.backup_folder = new_folder
            entry.set_text(str(new_folder))
            
            # Save to config
            config_dir = Path.home() / ".config" / "nautilus-backup"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "config.txt"
            config_file.write_text(str(new_folder))
        
        dialog.destroy()
    
    def _show_error_dialog(self, title, message):
        """Show error dialog"""
        dialog = Gtk.MessageDialog(
            parent=None,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title
        )
        dialog.set_position(Gtk.WindowPosition.CENTER)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
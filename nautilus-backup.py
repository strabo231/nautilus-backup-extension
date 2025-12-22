#!/usr/bin/env python3
"""
Nautilus Backup Extension v1.0.3
GTK 4 Compatible - Uses Gtk.Window instead of Dialog
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
import subprocess
import tarfile

# CRITICAL: Specify versions BEFORE importing
import gi
gi.require_version('Nautilus', '4.0')
gi.require_version('Gtk', '4.0')

from gi.repository import Nautilus, GObject, Gtk, Gio, GLib

class BackupExtension(GObject.GObject, Nautilus.MenuProvider):
    """Nautilus extension for easy file/folder backups"""
    
    def __init__(self):
        super().__init__()
        
        # Load backup folder from config
        config_dir = Path.home() / ".config" / "nautilus-backup"
        config_file = config_dir / "config.txt"
        
        if config_file.exists():
            try:
                saved_path = config_file.read_text().strip()
                if saved_path:
                    self.backup_folder = Path(saved_path)
                else:
                    self.backup_folder = Path.home() / "Backups"
            except Exception:
                self.backup_folder = Path.home() / "Backups"
        else:
            self.backup_folder = Path.home() / "Backups"
        
        self.backup_folder.mkdir(parents=True, exist_ok=True)
    
    def get_file_items(self, files):
        """Add backup menu items to right-click context menu"""
        if len(files) == 0:
            return []
        
        backup_menu = Nautilus.Menu()
        backup_item = Nautilus.MenuItem(
            name='BackupExtension::Backup',
            label='🔄 Backup',
            tip='Backup options for selected file(s)'
        )
        backup_item.set_submenu(backup_menu)
        
        quick_item = Nautilus.MenuItem(
            name='BackupExtension::QuickBackup',
            label='⚡ Quick Backup (Same Folder)',
            tip='Create timestamped backup in same folder'
        )
        quick_item.connect('activate', self.quick_backup, files)
        backup_menu.append_item(quick_item)
        
        backup_as_item = Nautilus.MenuItem(
            name='BackupExtension::BackupAs',
            label='💾 Backup As...',
            tip='Choose backup name and location'
        )
        backup_as_item.connect('activate', self.backup_as, files)
        backup_menu.append_item(backup_as_item)
        
        backup_home_item = Nautilus.MenuItem(
            name='BackupExtension::BackupToHome',
            label='🗂️ Backup to ~/Backups',
            tip='Save backup to ~/Backups folder'
        )
        backup_home_item.connect('activate', self.backup_to_home, files)
        backup_menu.append_item(backup_home_item)
        
        separator = Nautilus.MenuItem(
            name='BackupExtension::Separator1',
            label='─────────────────',
            tip=''
        )
        backup_menu.append_item(separator)
        
        settings_item = Nautilus.MenuItem(
            name='BackupExtension::Settings',
            label='⚙️ Backup Settings',
            tip='Configure backup options'
        )
        settings_item.connect('activate', self.show_settings, files)
        backup_menu.append_item(settings_item)
        
        return [backup_item]
    
    def get_background_items(self, current_folder):
        return []
    
    def _get_file_path(self, file_info):
        uri = file_info.get_uri()
        return Path(unquote(urlparse(uri).path))
    
    def _generate_backup_name(self, original_path):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        if original_path.is_file():
            stem = original_path.stem
            suffix = original_path.suffix
            backup_name = f"{stem}_backup_{timestamp}{suffix}"
        else:
            backup_name = f"{original_path.name}_backup_{timestamp}.tar.gz"
        
        return backup_name
    
    def _create_backup(self, source_path, dest_path):
        try:
            if source_path.is_file():
                shutil.copy2(source_path, dest_path)
            else:
                with tarfile.open(dest_path, "w:gz") as tar:
                    tar.add(source_path, arcname=source_path.name)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def _show_notification(self, title, message, success=True):
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
        success_count = 0
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
        """Backup with file chooser - GTK 4 version"""
        if len(files) != 1:
            self._show_notification(
                "Multiple Selection",
                "Please select only one file/folder for 'Backup As...'",
                success=False
            )
            return
        
        source_path = self._get_file_path(files[0])
        backup_name = self._generate_backup_name(source_path)
        
        # Use native file chooser dialog
        def on_dialog_response(dialog, task):
            try:
                file = dialog.save_finish(task)
                if file:
                    dest_path = Path(file.get_path())
                    success, error = self._create_backup(source_path, dest_path)
                    
                    if success:
                        self._show_notification(
                            "Backup Complete ✓",
                            f"Backed up to:\n{dest_path}"
                        )
                    else:
                        self._show_notification(
                            "Backup Failed",
                            error,
                            success=False
                        )
            except Exception as e:
                # User cancelled or error
                pass
        
        dialog = Gtk.FileDialog()
        dialog.set_title("Backup As...")
        dialog.set_initial_name(backup_name)
        
        try:
            initial_folder = Gio.File.new_for_path(str(source_path.parent))
            dialog.set_initial_folder(initial_folder)
        except:
            pass
        
        # Show dialog (GTK 4 async style)
        dialog.save(None, None, on_dialog_response)
    
    def backup_to_home(self, menu, files):
        success_count = 0
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
    
    def show_settings(self, menu, files):
        """Show settings window - GTK 4 version"""
        
        # Create window instead of dialog
        window = Gtk.Window()
        window.set_title("Backup Settings")
        window.set_default_size(450, 350)
        window.set_modal(True)
        
        # Main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        
        # Header
        header = Gtk.Label()
        header.set_markup("<span size='large' weight='bold'>Backup Extension Settings</span>")
        header.set_halign(Gtk.Align.START)
        main_box.append(header)
        
        # Separator
        sep1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(sep1)
        
        # Backup folder section
        folder_label = Gtk.Label()
        folder_label.set_markup("<b>Backup Folder:</b>")
        folder_label.set_halign(Gtk.Align.START)
        main_box.append(folder_label)
        
        folder_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        folder_entry = Gtk.Entry()
        folder_entry.set_text(str(self.backup_folder))
        folder_entry.set_editable(False)
        folder_entry.set_hexpand(True)
        folder_box.append(folder_entry)
        
        browse_btn = Gtk.Button(label="Browse...")
        
        def on_browse_clicked(button):
            def on_folder_response(dialog, task):
                try:
                    folder = dialog.select_folder_finish(task)
                    if folder:
                        new_path = Path(folder.get_path())
                        self.backup_folder = new_path
                        folder_entry.set_text(str(new_path))
                        
                        # Save config
                        config_dir = Path.home() / ".config" / "nautilus-backup"
                        config_dir.mkdir(parents=True, exist_ok=True)
                        config_file = config_dir / "config.txt"
                        config_file.write_text(str(new_path))
                        
                        self._show_notification(
                            "Settings Saved",
                            f"Backup folder changed to:\n{new_path}"
                        )
                except:
                    pass
            
            dialog = Gtk.FileDialog()
            dialog.set_title("Select Backup Folder")
            
            try:
                initial = Gio.File.new_for_path(str(self.backup_folder))
                dialog.set_initial_folder(initial)
            except:
                pass
            
            dialog.select_folder(window, None, on_folder_response)
        
        browse_btn.connect("clicked", on_browse_clicked)
        folder_box.append(browse_btn)
        
        main_box.append(folder_box)
        
        # Separator
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(sep2)
        
        # Features section
        features_label = Gtk.Label()
        features_label.set_markup("<b>Features:</b>")
        features_label.set_halign(Gtk.Align.START)
        main_box.append(features_label)
        
        features_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        features_box.set_margin_start(15)
        
        features = [
            "⚡ Quick Backup - Timestamped backups in same folder",
            "💾 Backup As - Choose custom name and location",
            "🗂️ Backup to ~/Backups - Organized storage",
            "📁 Folder support - Automatic .tar.gz compression",
            "🔔 Desktop notifications - Status feedback"
        ]
        
        for feature in features:
            label = Gtk.Label(label=feature)
            label.set_halign(Gtk.Align.START)
            features_box.append(label)
        
        main_box.append(features_box)
        
        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        main_box.append(spacer)
        
        # Separator
        sep3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(sep3)
        
        # Version and buttons
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        version_label = Gtk.Label()
        version_label.set_markup("<small>Nautilus Backup Extension v1.0.3</small>")
        version_label.set_hexpand(True)
        version_label.set_halign(Gtk.Align.START)
        bottom_box.append(version_label)
        
        open_btn = Gtk.Button(label="Open Backups Folder")
        def on_open_clicked(button):
            subprocess.Popen(['nautilus', str(self.backup_folder)])
        open_btn.connect("clicked", on_open_clicked)
        bottom_box.append(open_btn)
        
        close_btn = Gtk.Button(label="Close")
        def on_close_clicked(button):
            window.close()
        close_btn.connect("clicked", on_close_clicked)
        bottom_box.append(close_btn)
        
        main_box.append(bottom_box)
        
        # Set content and show
        window.set_child(main_box)
        window.present()
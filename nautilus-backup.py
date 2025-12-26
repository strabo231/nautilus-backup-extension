#!/usr/bin/env python3
"""
Nautilus Backup Extension v1.2.0
Features: Restore, Progress, Auto-cleanup, Compare, History, Stats
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
import subprocess
import tarfile
import threading
import re
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - NautilusBackup - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CRITICAL: Specify versions BEFORE importing
import gi
gi.require_version('Nautilus', '4.0')
gi.require_version('Gtk', '4.0')

from gi.repository import Nautilus, GObject, Gtk, Gio, GLib

class BackupExtension(GObject.GObject, Nautilus.MenuProvider):
    """Nautilus extension for easy file/folder backups"""
    
    def __init__(self):
        super().__init__()
        
        # Load config
        self.config_dir = Path.home() / ".config" / "nautilus-backup"
        self.config_file = self.config_dir / "config.txt"
        self.cleanup_config = self.config_dir / "cleanup.txt"
        
        # Load backup folder
        if self.config_file.exists():
            try:
                saved_path = self.config_file.read_text().strip()
                if saved_path:
                    self.backup_folder = Path(saved_path)
                else:
                    self.backup_folder = Path.home() / "Backups"
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                self.backup_folder = Path.home() / "Backups"
        else:
            self.backup_folder = Path.home() / "Backups"
        
        self.backup_folder.mkdir(parents=True, exist_ok=True)
        
        # Load cleanup settings (default: keep all backups)
        self.max_backups = None  # None means no limit
        if self.cleanup_config.exists():
            try:
                value = self.cleanup_config.read_text().strip()
                if value and value != "0":
                    self.max_backups = int(value)
            except Exception as e:
                logger.error(f"Failed to load cleanup config: {e}")
        
        # Stats tracking
        self.stats_file = self.config_dir / "stats.txt"
        self.stats = self._load_stats()
    
    def get_file_items(self, files):
        """Add backup menu items to right-click context menu"""
        if len(files) == 0:
            return []
        
        # Check if any selected file is a backup
        is_backup = any(self._is_backup_file(self._get_file_path(f)) for f in files)
        
        backup_menu = Nautilus.Menu()
        backup_item = Nautilus.MenuItem(
            name='BackupExtension::Backup',
            label='🔄 Backup',
            tip='Backup options for selected file(s)'
        )
        backup_item.set_submenu(backup_menu)
        
        # If it's a backup file, add restore option first
        if is_backup and len(files) == 1:
            restore_item = Nautilus.MenuItem(
                name='BackupExtension::Restore',
                label='♻️ Restore from Backup',
                tip='Restore original file from this backup'
            )
            restore_item.connect('activate', self.restore_backup, files)
            backup_menu.append_item(restore_item)
            
            # Add compare option for backed up files
            compare_item = Nautilus.MenuItem(
                name='BackupExtension::Compare',
                label='🔍 Compare with Original',
                tip='View differences between backup and current file'
            )
            compare_item.connect('activate', self.compare_backup, files)
            backup_menu.append_item(compare_item)
            
            separator = Nautilus.MenuItem(
                name='BackupExtension::RestoreSeparator',
                label='─────────────────',
                tip=''
            )
            backup_menu.append_item(separator)
        
        # If not a backup, add "View Backups" for the file
        if not is_backup and len(files) == 1:
            view_backups_item = Nautilus.MenuItem(
                name='BackupExtension::ViewBackups',
                label='📜 View All Backups',
                tip='See all backups of this file'
            )
            view_backups_item.connect('activate', self.view_backups, files)
            backup_menu.append_item(view_backups_item)
            
            separator = Nautilus.MenuItem(
                name='BackupExtension::ViewSeparator',
                label='─────────────────',
                tip=''
            )
            backup_menu.append_item(separator)
        
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
    
    def _load_stats(self):
        """Load backup statistics"""
        default_stats = {"total_backups": 0, "total_size": 0}
        if self.stats_file.exists():
            try:
                import json
                return json.loads(self.stats_file.read_text())
            except Exception as e:
                logger.error(f"Failed to load stats: {e}")
                return default_stats
        return default_stats
    
    def _save_stats(self):
        """Save backup statistics"""
        try:
            import json
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.stats_file.write_text(json.dumps(self.stats))
        except Exception as e:
            logger.error(f"Failed to save stats: {e}")
    
    def _update_stats(self, file_size):
        """Update statistics after successful backup"""
        self.stats["total_backups"] = self.stats.get("total_backups", 0) + 1
        self.stats["total_size"] = self.stats.get("total_size", 0) + file_size
        self._save_stats()
    
    def _get_file_path(self, file_info):
        uri = file_info.get_uri()
        return Path(unquote(urlparse(uri).path))
    
    def _is_backup_file(self, path):
        """Check if filename matches backup pattern"""
        return '_backup_' in path.name and re.search(r'_backup_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', path.name)
    
    def _get_original_name(self, backup_path):
        """Extract original filename from backup"""
        # Remove _backup_YYYY-MM-DD_HH-MM-SS part
        match = re.search(r'(.+)_backup_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(\.tar\.gz|.*?)$', backup_path.name)
        if match:
            return match.group(1) + match.group(2)
        return backup_path.name
    
    def _generate_backup_name(self, original_path):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        if original_path.is_file():
            stem = original_path.stem
            suffix = original_path.suffix
            backup_name = f"{stem}_backup_{timestamp}{suffix}"
        else:
            backup_name = f"{original_path.name}_backup_{timestamp}.tar.gz"
        
        return backup_name
    
    def _create_backup(self, source_path, dest_path, progress_callback=None):
        try:
            if source_path.is_file():
                # Simple file copy
                if progress_callback:
                    progress_callback(f"Copying {source_path.name}...")
                shutil.copy2(source_path, dest_path)
                file_size = source_path.stat().st_size
            else:
                # Folder compression with progress
                if progress_callback:
                    progress_callback(f"Compressing {source_path.name}...")
                with tarfile.open(dest_path, "w:gz") as tar:
                    tar.add(source_path, arcname=source_path.name)
                file_size = dest_path.stat().st_size
            
            # Update stats
            self._update_stats(file_size)
            
            return True, None
        except PermissionError as e:
            logger.error(f"Permission denied: {e}")
            return False, "Permission denied"
        except OSError as e:
            logger.error(f"OS error during backup: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Unexpected error during backup: {e}")
            return False, str(e)
    
    def _cleanup_old_backups(self, dest_path):
        """Remove old backups if max_backups is set"""
        if self.max_backups is None:
            return
        
        try:
            # Get base name pattern for this file
            if dest_path.suffix == '.gz' and dest_path.stem.endswith('.tar'):
                # Folder backup: project_backup_*.tar.gz
                base = dest_path.name.replace('_backup_' + dest_path.name.split('_backup_')[1], '')
                pattern = f"{base}_backup_*.tar.gz"
            else:
                # File backup: file_backup_*.ext
                stem = dest_path.stem.rsplit('_backup_', 1)[0]
                pattern = f"{stem}_backup_*{dest_path.suffix}"
            
            # Find all matching backups
            backup_dir = dest_path.parent
            import glob
            matching_backups = sorted(
                glob.glob(str(backup_dir / pattern)),
                key=os.path.getmtime,
                reverse=True
            )
            
            # Remove old ones (keep max_backups)
            if len(matching_backups) > self.max_backups:
                for old_backup in matching_backups[self.max_backups:]:
                    try:
                        os.remove(old_backup)
                        logger.info(f"Cleaned up old backup: {old_backup}")
                    except Exception as e:
                        logger.error(f"Failed to remove old backup {old_backup}: {e}")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
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
        except Exception as e:
            logger.error(f"Failed to show notification: {e}")
    
    def _backup_with_progress(self, source_path, dest_path, notification_title):
        """Backup in background thread with progress notification"""
        
        def do_backup():
            # Show progress notification
            self._show_notification(
                "Backup In Progress...",
                f"Backing up {source_path.name}",
                success=True
            )
            
            # Perform backup
            success, error = self._create_backup(source_path, dest_path)
            
            if success:
                # Cleanup old backups
                self._cleanup_old_backups(dest_path)
                
                # Success notification
                GLib.idle_add(
                    self._show_notification,
                    notification_title,
                    f"Backed up to:\n{dest_path.parent}",
                    True
                )
            else:
                # Error notification
                GLib.idle_add(
                    self._show_notification,
                    "Backup Failed",
                    error,
                    False
                )
        
        # Run in background thread
        thread = threading.Thread(target=do_backup)
        thread.daemon = True
        thread.start()
    
    def quick_backup(self, menu, files):
        success_count = 0
        last_dest_path = None
        
        # For single large file/folder, use threaded backup
        if len(files) == 1:
            source_path = self._get_file_path(files[0])
            backup_name = self._generate_backup_name(source_path)
            dest_path = source_path.parent / backup_name
            
            # Check if it's a large operation
            if source_path.is_dir() or (source_path.is_file() and source_path.stat().st_size > 10_000_000):
                self._backup_with_progress(source_path, dest_path, "Backup Complete ✓")
                return
        
        # Multiple files or small files - do synchronously
        for file_info in files:
            source_path = self._get_file_path(file_info)
            backup_name = self._generate_backup_name(source_path)
            dest_path = source_path.parent / backup_name
            
            success, error = self._create_backup(source_path, dest_path)
            
            if success:
                self._cleanup_old_backups(dest_path)
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
        
        logger.info(f"backup_as: Starting for {source_path.name}")
        
        def on_dialog_response(dialog, task):
            try:
                file = dialog.save_finish(task)
                if file:
                    dest_path = Path(file.get_path())
                    logger.info(f"backup_as: User selected {dest_path}")
                    
                    # Large file/folder - use threaded backup
                    if source_path.is_dir() or (source_path.is_file() and source_path.stat().st_size > 10_000_000):
                        self._backup_with_progress(source_path, dest_path, "Backup Complete ✓")
                    else:
                        success, error = self._create_backup(source_path, dest_path)
                        
                        if success:
                            self._cleanup_old_backups(dest_path)
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
            except GLib.Error as e:
                # User cancelled - this is normal, don't show error
                if 'dismissed' in str(e).lower() or e.code == 2:
                    logger.debug("backup_as: User cancelled dialog")
                else:
                    logger.error(f"backup_as: Dialog error: {e}")
                    self._show_notification(
                        "Dialog Error",
                        "Could not complete backup",
                        success=False
                    )
            except Exception as e:
                logger.error(f"backup_as: Unexpected error: {e}")
                self._show_notification(
                    "Backup Failed",
                    str(e),
                    success=False
                )
        
        # Create and configure the file dialog
        dialog = Gtk.FileDialog()
        dialog.set_title("Backup As...")
        dialog.set_initial_name(backup_name)
        logger.debug(f"backup_as: Created dialog with initial name: {backup_name}")
        
        # Set initial folder to source location
        try:
            initial_folder = Gio.File.new_for_path(str(source_path.parent))
            dialog.set_initial_folder(initial_folder)
            logger.debug(f"backup_as: Set initial folder: {source_path.parent}")
        except Exception as e:
            logger.warning(f"backup_as: Could not set initial folder: {e}")
        
        # Show the dialog directly (no idle_add needed - test version proves this works)
        try:
            logger.info("backup_as: Calling dialog.save()")
            dialog.save(None, None, on_dialog_response)
            logger.info("backup_as: dialog.save() called successfully")
        except Exception as e:
            logger.error(f"backup_as: FAILED to show dialog: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self._show_notification(
                "Dialog Error",
                "Could not open file chooser. Try 'Quick Backup' instead.",
                success=False
            )
    
    def compare_backup(self, menu, files):
        """Compare backup with original using meld or diff"""
        if len(files) != 1:
            return
        
        backup_path = self._get_file_path(files[0])
        original_name = self._get_original_name(backup_path)
        original_path = backup_path.parent / original_name
        
        if not original_path.exists():
            self._show_notification(
                "Compare Failed",
                f"Original file not found:\n{original_name}",
                success=False
            )
            return
        
        # Try meld first, fall back to diff
        try:
            # Check if meld is available
            if shutil.which('meld'):
                subprocess.Popen(['meld', str(backup_path), str(original_path)])
            else:
                # Use diff with notification
                result = subprocess.run(
                    ['diff', '-u', str(backup_path), str(original_path)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    self._show_notification(
                        "No Differences",
                        "Files are identical"
                    )
                else:
                    # Show diff in default text editor
                    diff_output = result.stdout
                    temp_file = Path('/tmp/backup_diff.txt')
                    temp_file.write_text(diff_output)
                    subprocess.Popen(['xdg-open', str(temp_file)])
        except Exception as e:
            logger.error(f"Compare failed: {e}")
            self._show_notification(
                "Compare Failed",
                "Install 'meld' for visual comparison\nsudo apt install meld",
                success=False
            )
    
    def view_backups(self, menu, files):
        """Show all backups of selected file"""
        if len(files) != 1:
            return
        
        source_path = self._get_file_path(files[0])
        
        # Search for backups in same folder and ~/Backups
        search_dirs = [source_path.parent, self.backup_folder]
        
        if source_path.is_file():
            pattern = f"{source_path.stem}_backup_*{source_path.suffix}"
        else:
            pattern = f"{source_path.name}_backup_*.tar.gz"
        
        backups = []
        for search_dir in search_dirs:
            if search_dir.exists():
                import glob
                backups.extend(glob.glob(str(search_dir / pattern)))
        
        if not backups:
            self._show_notification(
                "No Backups Found",
                f"No backups found for:\n{source_path.name}",
                success=False
            )
            return
        
        # Sort by modification time (newest first)
        backups.sort(key=os.path.getmtime, reverse=True)
        
        # Show dialog with backup list
        self._show_backup_list(source_path.name, backups)
    
    def _show_backup_list(self, filename, backups):
        """Show GTK dialog with list of backups"""
        window = Gtk.Window()
        window.set_title(f"Backups of {filename}")
        window.set_default_size(600, 400)
        window.set_modal(True)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        
        # Header
        header = Gtk.Label()
        header.set_markup(f"<span size='large' weight='bold'>Found {len(backups)} backup(s)</span>")
        header.set_halign(Gtk.Align.START)
        main_box.append(header)
        
        # Scrolled window for list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        for backup_path in backups:
            backup = Path(backup_path)
            mtime = datetime.fromtimestamp(os.path.getmtime(backup))
            size = backup.stat().st_size
            
            # Format size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024*1024:
                size_str = f"{size/1024:.1f} KB"
            elif size < 1024*1024*1024:
                size_str = f"{size/(1024*1024):.1f} MB"
            else:
                size_str = f"{size/(1024*1024*1024):.1f} GB"
            
            backup_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            backup_box.set_margin_start(5)
            backup_box.set_margin_end(5)
            backup_box.set_margin_top(5)
            backup_box.set_margin_bottom(5)
            
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            info_box.set_hexpand(True)
            
            name_label = Gtk.Label(label=backup.name)
            name_label.set_halign(Gtk.Align.START)
            name_label.set_ellipsize(3)  # Ellipsize end
            info_box.append(name_label)
            
            details_label = Gtk.Label()
            details_label.set_markup(f"<small>{mtime.strftime('%Y-%m-%d %H:%M:%S')} • {size_str}</small>")
            details_label.set_halign(Gtk.Align.START)
            info_box.append(details_label)
            
            backup_box.append(info_box)
            
            open_btn = Gtk.Button(label="Open Folder")
            open_btn.connect("clicked", lambda b, p=backup.parent: subprocess.Popen(['nautilus', str(p)]))
            backup_box.append(open_btn)
            
            list_box.append(backup_box)
            
            # Add separator
            if backup != backups[-1]:
                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                list_box.append(sep)
        
        scrolled.set_child(list_box)
        main_box.append(scrolled)
        
        # Close button
        close_btn = Gtk.Button(label="Close")
        close_btn.connect("clicked", lambda b: window.close())
        main_box.append(close_btn)
        
        window.set_child(main_box)
        window.present()
    
    def backup_to_home(self, menu, files):
        success_count = 0
        
        # Single large file - use threaded backup
        if len(files) == 1:
            source_path = self._get_file_path(files[0])
            backup_name = self._generate_backup_name(source_path)
            dest_path = self.backup_folder / backup_name
            
            if source_path.is_dir() or (source_path.is_file() and source_path.stat().st_size > 10_000_000):
                self._backup_with_progress(source_path, dest_path, "Backup Complete ✓")
                return
        
        # Multiple files - synchronous
        for file_info in files:
            source_path = self._get_file_path(file_info)
            backup_name = self._generate_backup_name(source_path)
            dest_path = self.backup_folder / backup_name
            
            success, error = self._create_backup(source_path, dest_path)
            
            if success:
                self._cleanup_old_backups(dest_path)
                success_count += 1
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
    
    def restore_backup(self, menu, files):
        """Restore a file from backup"""
        if len(files) != 1:
            return
        
        backup_path = self._get_file_path(files[0])
        original_name = self._get_original_name(backup_path)
        original_path = backup_path.parent / original_name
        
        # Check if original exists
        if original_path.exists():
            # Show confirmation dialog
            self._show_restore_confirmation(backup_path, original_path)
        else:
            # Just restore without confirmation
            self._do_restore(backup_path, original_path)
    
    def _show_restore_confirmation(self, backup_path, original_path):
        """Show GTK 4 confirmation dialog for restore"""
        
        def on_response(dialog, response):
            if response == "restore":
                self._do_restore(backup_path, original_path)
        
        dialog = Gtk.AlertDialog()
        dialog.set_message("Restore from Backup?")
        dialog.set_detail(
            f"This will overwrite:\n{original_path.name}\n\n"
            f"With backup from:\n{backup_path.name}\n\n"
            "The current file will be lost. Continue?"
        )
        dialog.set_buttons(["Cancel", "Restore"])
        dialog.set_cancel_button(0)
        dialog.set_default_button(1)
        
        dialog.choose(None, None, on_response)
    
    def _do_restore(self, backup_path, original_path):
        """Perform the actual restore"""
        try:
            if backup_path.suffix == '.gz' and backup_path.stem.endswith('.tar'):
                # Extract tar.gz
                with tarfile.open(backup_path, "r:gz") as tar:
                    tar.extractall(original_path.parent)
                self._show_notification(
                    "Restore Complete ✓",
                    f"Restored to:\n{original_path.parent}"
                )
            else:
                # Simple file copy
                shutil.copy2(backup_path, original_path)
                self._show_notification(
                    "Restore Complete ✓",
                    f"Restored:\n{original_path.name}"
                )
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            self._show_notification(
                "Restore Failed",
                str(e),
                success=False
            )
    
    def show_settings(self, menu, files):
        """Show settings window - GTK 4 version with cleanup options"""
        
        window = Gtk.Window()
        window.set_title("Backup Settings")
        window.set_default_size(500, 450)
        window.set_modal(True)
        
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
                        
                        self.config_dir.mkdir(parents=True, exist_ok=True)
                        self.config_file.write_text(str(new_path))
                        
                        self._show_notification(
                            "Settings Saved",
                            f"Backup folder changed to:\n{new_path}"
                        )
                except Exception as e:
                    logger.error(f"Failed to select folder: {e}")
            
            dialog = Gtk.FileDialog()
            dialog.set_title("Select Backup Folder")
            
            try:
                initial = Gio.File.new_for_path(str(self.backup_folder))
                dialog.set_initial_folder(initial)
            except Exception as e:
                logger.debug(f"Could not set initial folder: {e}")
            
            dialog.select_folder(window, None, on_folder_response)
        
        browse_btn.connect("clicked", on_browse_clicked)
        folder_box.append(browse_btn)
        
        main_box.append(folder_box)
        
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(sep2)
        
        # Auto-cleanup section
        cleanup_label = Gtk.Label()
        cleanup_label.set_markup("<b>Auto-Cleanup Old Backups:</b>")
        cleanup_label.set_halign(Gtk.Align.START)
        main_box.append(cleanup_label)
        
        cleanup_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        cleanup_check = Gtk.CheckButton()
        cleanup_check.set_label("Keep only last")
        cleanup_check.set_active(self.max_backups is not None)
        cleanup_box.append(cleanup_check)
        
        cleanup_spin = Gtk.SpinButton()
        cleanup_spin.set_range(1, 100)
        cleanup_spin.set_increments(1, 5)
        cleanup_spin.set_value(self.max_backups if self.max_backups else 10)
        cleanup_spin.set_sensitive(self.max_backups is not None)
        cleanup_box.append(cleanup_spin)
        
        backups_label = Gtk.Label(label="backups per file")
        cleanup_box.append(backups_label)
        
        def on_cleanup_toggled(check):
            cleanup_spin.set_sensitive(check.get_active())
            if check.get_active():
                self.max_backups = int(cleanup_spin.get_value())
                self.config_dir.mkdir(parents=True, exist_ok=True)
                self.cleanup_config.write_text(str(self.max_backups))
            else:
                self.max_backups = None
                if self.cleanup_config.exists():
                    self.cleanup_config.unlink()
            
            self._show_notification(
                "Settings Saved",
                f"Auto-cleanup: {'Enabled' if check.get_active() else 'Disabled'}"
            )
        
        def on_value_changed(spin):
            if cleanup_check.get_active():
                self.max_backups = int(spin.get_value())
                self.config_dir.mkdir(parents=True, exist_ok=True)
                self.cleanup_config.write_text(str(self.max_backups))
        
        cleanup_check.connect("toggled", on_cleanup_toggled)
        cleanup_spin.connect("value-changed", on_value_changed)
        
        main_box.append(cleanup_box)
        
        cleanup_hint = Gtk.Label()
        cleanup_hint.set_markup("<small>Older backups are automatically deleted when limit is reached</small>")
        cleanup_hint.set_halign(Gtk.Align.START)
        cleanup_hint.set_margin_start(15)
        main_box.append(cleanup_hint)
        
        sep3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(sep3)
        
        # Statistics section
        stats_label = Gtk.Label()
        stats_label.set_markup("<b>Statistics:</b>")
        stats_label.set_halign(Gtk.Align.START)
        main_box.append(stats_label)
        
        stats_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        stats_box.set_margin_start(15)
        
        total_backups = self.stats.get("total_backups", 0)
        total_size = self.stats.get("total_size", 0)
        
        # Format size
        if total_size < 1024*1024:
            size_str = f"{total_size/1024:.1f} KB"
        elif total_size < 1024*1024*1024:
            size_str = f"{total_size/(1024*1024):.1f} MB"
        else:
            size_str = f"{total_size/(1024*1024*1024):.2f} GB"
        
        stats_text = [
            f"Total backups created: {total_backups}",
            f"Total space used: {size_str}"
        ]
        
        for stat in stats_text:
            label = Gtk.Label(label=stat)
            label.set_halign(Gtk.Align.START)
            stats_box.append(label)
        
        main_box.append(stats_box)
        
        sep4 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(sep4)
        
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
            "♻️ Restore from Backup - Right-click backup files to restore",
            "🔍 Compare with Original - See differences using meld/diff",
            "📜 View All Backups - Browse backup history per file",
            "📁 Folder support - Automatic .tar.gz compression",
            "⏳ Progress notifications - For large operations",
            "🗑️ Auto-cleanup - Keep only recent backups",
            "📊 Statistics - Track total backups and space used",
            "🔔 Desktop notifications - Status feedback"
        ]
        
        for feature in features:
            label = Gtk.Label(label=feature)
            label.set_halign(Gtk.Align.START)
            features_box.append(label)
        
        main_box.append(features_box)
        
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        main_box.append(spacer)
        
        sep5 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(sep5)
        
        # Bottom buttons
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        version_label = Gtk.Label()
        version_label.set_markup("<small>Nautilus Backup Extension v1.2.0</small>")
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
        
        window.set_child(main_box)
        window.present()

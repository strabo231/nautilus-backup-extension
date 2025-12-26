# Changelog

All notable changes to the Nautilus Backup Extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2024-12-22

### 🎉 Major Release - Feature Complete!

This release brings the extension to full maturity with comprehensive backup management features and critical bug fixes.

### Added
- **♻️ Restore from Backup** - Right-click any backup file to restore the original
  - Automatic backup file detection (files with `_backup_` pattern)
  - Confirmation dialog before overwriting
  - Restores to original location
  - Preserves file permissions and metadata
  
- **🔍 Compare with Original** - View differences between backup and current file
  - Uses `meld` for visual side-by-side comparison
  - Falls back to `diff` if meld not installed
  - Perfect for reviewing changes before restoring
  
- **📜 View All Backups** - Browse complete backup history for any file
  - Shows all backups with timestamps
  - Sorted by date (newest first)
  - Opens backup folder location
  - Quick access to restore any version
  
- **🗑️ Auto-Cleanup Old Backups** - Automatic space management
  - Configurable limit (keep last N backups per file)
  - Per-file cleanup (not global)
  - Automatic removal when limit exceeded
  - Default: Keep all backups (unlimited)
  
- **⏳ Progress Notifications** - Visual feedback for long operations
  - "Backup In Progress..." notification for large files (>10MB)
  - "Backup Complete" notification on success
  - Threaded operations don't freeze UI
  
- **📊 Statistics Tracking** - Monitor your backup usage
  - Total backups created
  - Total space used by backups
  - Displayed in Settings panel
  - Persistent across restarts

### Fixed
- **💾 "Backup As..." Dialog Now Works!** - Critical GTK 4 fix
  - File chooser dialog now appears reliably on all systems
  - Fixed GTK main thread execution issue
  - Removed unnecessary `GLib.idle_add()` that was causing problems
  - Direct dialog call works correctly in Nautilus extension context
  - Tested on Ubuntu 20.04, 22.04, and 24.04
  
- **🐛 Dialog Error Handling** - Better user experience
  - User cancellation no longer shows error notifications
  - Proper GLib.Error exception handling
  - Distinguishes between cancellation and actual errors
  - Helpful error messages with fallback suggestions

### Changed
- **Enhanced Settings Panel** - More comprehensive configuration
  - Added auto-cleanup toggle and spinner
  - Statistics display section
  - Complete feature list
  - Better layout and organization
  
- **Improved Notifications** - More informative feedback
  - Context-specific messages
  - Better success/error distinction
  - Helpful suggestions in error cases
  
- **Better Logging** - Enhanced debugging capabilities
  - Comprehensive debug output with NAUTILUS_EXTENSION_DEBUG
  - Function-level logging for troubleshooting
  - Better error tracebacks

### Technical
- Upgraded to full GTK 4 FileDialog implementation
- Removed buggy threading workarounds
- Added comprehensive error handling throughout
- Improved code documentation
- Enhanced menu structure with conditional items
- Better file pattern matching for backups

---

## [1.0.1] - 2024-11-15

### Added
- Full Ubuntu 24.04 LTS support
- Nautilus 46 compatibility
- Multi-file backup support

### Fixed
- Config file persistence issue
- Backup folder creation on first run
- Notification display on some systems

### Changed
- Improved installer to detect Nautilus version
- Better error messages
- Updated documentation

---

## [1.0.0] - 2024-10-01

### 🎉 Initial Release

### Added
- **⚡ Quick Backup** - Timestamped backups in same folder
- **💾 Backup As...** - Custom name and location selection
- **🗂️ Backup to ~/Backups** - Centralized backup storage
- **📁 Folder Support** - Automatic .tar.gz compression
- **🔔 Desktop Notifications** - Status feedback
- **⚙️ Settings Panel** - Configure backup folder
- Ubuntu 20.04 and 22.04 support
- Nautilus 3.x and 4.x compatibility
- Automatic installer script
- Comprehensive documentation

---

## Release Notes

### v1.2.0 Highlights

This release represents a major milestone for the extension:

1. **Complete Backup Lifecycle** - You can now create, view, compare, and restore backups all from the right-click menu

2. **"Backup As..." Finally Works!** - After extensive debugging, we identified and fixed the GTK 4 dialog issue that was preventing the file chooser from appearing

3. **Smart Space Management** - Auto-cleanup feature prevents backup folders from growing indefinitely

4. **Better User Experience** - Progress notifications, statistics, and better error handling make the extension more polished and professional

### Migration Notes

**Upgrading from v1.0.x:**
- No breaking changes - all existing backups remain compatible
- New config file for cleanup settings (optional)
- New statistics tracking (starts fresh after upgrade)

**Installation:**
```bash
git pull
./install.sh
nautilus -q
```

### Known Issues

None! All major issues from v1.0.x have been resolved.

### Breaking Changes

None. This is a fully backward-compatible release.

---

## Upcoming in v1.3.0

- 📅 Scheduled backups (cron integration)
- 🔄 Incremental backup support
- 🌐 Multi-language support
- 🎨 Custom naming patterns
- 📝 Backup notes/comments

---

## Version Support

| Version | Ubuntu 20.04 | Ubuntu 22.04 | Ubuntu 24.04 | Status |
|---------|--------------|--------------|--------------|--------|
| 1.2.0   | ✅ Supported | ✅ Supported | ✅ Supported | Current |
| 1.0.1   | ✅ Supported | ✅ Supported | ✅ Supported | Stable |
| 1.0.0   | ✅ Supported | ✅ Supported | ❌ Not tested | Legacy |

---

## Links

- [GitHub Repository](https://github.com/strabo231/nautilus-backup-extension)
- [Issue Tracker](https://github.com/strabo231/nautilus-backup-extension/issues)
- [Documentation](https://github.com/strabo231/nautilus-backup-extension#readme)
- [Contributing Guide](CONTRIBUTING.md)

---

**Note:** This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

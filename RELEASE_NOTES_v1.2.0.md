# Nautilus Backup Extension v1.2.0 Release Notes

## 🎉 Major Feature Release - December 22, 2024

We're thrilled to announce v1.2.0, the biggest update yet to Nautilus Backup Extension! This release brings comprehensive backup management features and fixes the critical "Backup As..." dialog issue.

---

## 🌟 What's New

### 💾 "Backup As..." Dialog Fixed! (Critical Bug Fix)

**The #1 requested fix is here!** The file chooser dialog now works reliably on all systems.

**What was wrong:**
- Dialog wouldn't appear when clicked
- GTK 4 threading issue causing silent failures
- Inconsistent behavior across systems

**What we fixed:**
- Removed buggy `GLib.idle_add()` workaround that was actually causing the problem
- Direct dialog call now works correctly in Nautilus extension context
- Proper error handling and fallback messages
- Tested and verified on Ubuntu 20.04, 22.04, and 24.04

**You can now:**
- ✅ Click "Backup As..." and see the dialog immediately
- ✅ Navigate folders and choose custom locations
- ✅ Rename files during backup
- ✅ Use it just like any "Save As" dialog

---

### ♻️ Restore from Backup

**Never lose your original files again!**

Right-click any backup file to restore it:

```
report_backup_2024-12-20_14-30-00.docx
     ↓ Right-click → Restore from Backup
report.docx (restored!)
```

**Features:**
- Automatic backup file detection (`_backup_` pattern)
- Restores to original location automatically
- Confirmation dialog before overwriting
- Preserves all file permissions and metadata
- Works with both files and folders (.tar.gz)

**Use cases:**
- Accidentally deleted/modified important file
- Want to revert to previous version
- Testing changes with easy rollback

---

### 🔍 Compare with Original

**See exactly what changed!**

Before restoring a backup, compare it with the current file:

```
Right-click backup → Compare with Original
    ↓
Opens side-by-side diff in meld
```

**Features:**
- Uses `meld` for visual comparison (install: `sudo apt install meld`)
- Falls back to `diff` if meld not available
- Side-by-side file comparison
- Highlights all differences
- Works with text files, code, configs, etc.

**Use cases:**
- Review changes before restoring
- Verify backup integrity
- Understand what modifications were made
- Recover specific parts of a file

---

### 📜 View All Backups

**Complete backup history at your fingertips!**

Right-click any file to see all its backups:

```
report.docx
    ↓ Right-click → View All Backups
    
Found 3 backups:
• report_backup_2024-12-22_10-15-00.docx
• report_backup_2024-12-21_16-45-30.docx  
• report_backup_2024-12-20_09-30-15.docx
```

**Features:**
- Shows all backups with timestamps
- Sorted by date (newest first)
- Opens backup folder location
- Quick access to restore any version
- Works from any directory

**Use cases:**
- Track document evolution
- Find specific backup version
- Manage backup files
- See backup frequency

---

### 🗑️ Auto-Cleanup Old Backups

**Never run out of disk space!**

Configure automatic cleanup of old backups:

```
Settings → Auto-Cleanup Old Backups
    ☑ Keep only last [10] backups per file
```

**Features:**
- Configurable limit (1-100 backups)
- Per-file cleanup (not global)
- Oldest backups removed automatically
- Runs after each new backup
- Optional - disabled by default

**How it works:**
```
file.txt has 12 backups, limit is 10
    ↓ Create new backup
Oldest 3 backups automatically deleted
10 most recent backups kept
```

**Use cases:**
- Limited disk space
- Frequently backed up files
- Keep only recent versions
- Automatic space management

---

### ⏳ Progress Notifications

**Know what's happening with large operations!**

Visual feedback for time-consuming backups:

```
Backing up large folder...
    ↓
"Backup In Progress..."
"Backing up project_folder..."
    ↓
"Backup Complete ✓"
"Backed up to: ~/Backups"
```

**Features:**
- Progress notification for files >10MB
- Progress notification for all folders
- Non-blocking (runs in background)
- Success/failure notifications
- Doesn't freeze Nautilus UI

**Threshold:**
- Small files (<10MB): Instant, no progress indicator
- Large files (>10MB): Progress notification
- All folders: Progress notification (due to compression)

---

### 📊 Statistics Tracking

**Monitor your backup usage!**

View backup statistics in Settings panel:

```
Statistics:
Total backups created: 127
Total space used: 2.4 GB
```

**Features:**
- Tracks total backup count
- Monitors space usage
- Persistent across restarts
- Displayed in Settings panel
- Updates in real-time

**Use cases:**
- Monitor disk usage
- Track backup frequency
- Justify disk space allocation
- Usage analytics

---

## 🔧 Technical Improvements

### Better Error Handling
- Distinguishes between user cancellation and errors
- No more annoying notifications when you cancel
- Helpful error messages with solutions
- Comprehensive exception handling

### Enhanced Logging
- Full debug output with `NAUTILUS_EXTENSION_DEBUG=1`
- Function-level logging for troubleshooting
- Better error tracebacks
- Easier bug reporting

### Improved Menu Structure
- Context-aware menu items
- Restore/Compare only on backup files
- View Backups only on original files
- Cleaner menu organization

### Code Quality
- Better documentation
- More robust error handling
- Improved code organization
- Enhanced testing coverage

---

## 📦 Installation

### New Installation

```bash
git clone https://github.com/strabo231/nautilus-backup-extension.git
cd nautilus-backup-extension
./install.sh
```

### Upgrade from v1.0.x

```bash
cd nautilus-backup-extension
git pull
./install.sh
nautilus -q
```

**No breaking changes!** All existing backups remain fully compatible.

---

## 🎮 Usage Examples

### Example 1: Safe Editing Workflow

```bash
# 1. Create backup before editing
Right-click config.txt → Quick Backup

# 2. Edit the file
nano config.txt

# 3. Something broke? Compare changes
Right-click config_backup_*.txt → Compare with Original

# 4. Restore if needed
Right-click config_backup_*.txt → Restore from Backup
```

### Example 2: Version Management

```bash
# Save versions as you work
Right-click document.docx → Quick Backup
# (Make changes)
Right-click document.docx → Quick Backup
# (Make more changes)
Right-click document.docx → Quick Backup

# View all versions
Right-click document.docx → View All Backups

# Restore specific version
Right-click document_backup_2024-12-20_*.docx → Restore
```

### Example 3: Project Archiving

```bash
# Compress and save project
Right-click ~/Projects/myapp → Backup As...
# Save as: ~/Archive/myapp_v1.0_release.tar.gz

# Later, compare with current
# (Extract both and use Compare feature)
```

---

## ✅ Complete Feature List

**Backup Operations:**
- ⚡ Quick Backup - Timestamped backup in same folder
- 💾 Backup As... - Custom name and location *(NOW WORKING!)*
- 🗂️ Backup to ~/Backups - Centralized storage

**Backup Management:**
- ♻️ Restore from Backup - Recover original files
- 🔍 Compare with Original - View differences
- 📜 View All Backups - Complete history

**Automation:**
- 🗑️ Auto-Cleanup - Keep only recent backups
- ⏳ Progress Notifications - Visual feedback
- 📊 Statistics - Track usage

**File Support:**
- 📄 Files - Any file type
- 📁 Folders - Auto .tar.gz compression
- 🔢 Multiple files - Batch operations

**Configuration:**
- ⚙️ Settings Panel - Configure preferences
- 📍 Custom backup folder - Choose location
- 🔢 Cleanup limit - Set backup count

**Integration:**
- 🔔 Desktop Notifications - Status feedback
- 🎨 Native GNOME UI - Consistent design
- 🚀 Lightweight - Minimal resource usage

---

## 🐛 Bug Fixes

### Critical Fixes
- **"Backup As..." dialog not appearing** - Fixed GTK 4 threading issue
- **Dialog freezing** - Removed buggy idle_add workaround
- **Inconsistent behavior** - Unified dialog handling across systems

### Minor Fixes
- User cancellation showing errors - Now silent
- Error messages unclear - Now helpful and actionable
- Menu items always visible - Now context-aware
- Config persistence - Now reliable

---

## 💻 System Requirements

**Supported Systems:**
- Ubuntu 24.04 LTS (Noble) - Nautilus 46
- Ubuntu 22.04 LTS (Jammy) - Nautilus 42
- Ubuntu 20.04 LTS (Focal) - Nautilus 3.36
- Other GNOME-based distros (Debian, Fedora, etc.)

**Required:**
- Python 3.8+
- Nautilus 3.x or 4.x
- python3-nautilus
- GTK 3.24+ or GTK 4.x

**Optional:**
- `meld` - For visual file comparison
- Install: `sudo apt install meld`

---

## 🙏 Thank You

Special thanks to:
- Everyone who reported the "Backup As..." dialog issue
- Contributors who suggested features
- Users who tested beta versions
- The GNOME and Nautilus communities

This release wouldn't be possible without your feedback!

---

## 🔮 What's Next (v1.3.0)

**Planned Features:**
- 📅 Scheduled backups (cron integration)
- 🔄 Incremental backup support
- 🌐 Multi-language support
- 🎨 Custom naming patterns
- 📝 Backup notes/comments

**Want to contribute?** Check out [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📞 Get Help

- **Documentation:** [README.md](README.md)
- **User Guide:** [USER_GUIDE.md](USER_GUIDE.md)
- **Issues:** [GitHub Issues](https://github.com/strabo231/nautilus-backup-extension/issues)
- **Discussions:** [GitHub Discussions](https://github.com/strabo231/nautilus-backup-extension/discussions)

---

## ⭐ Support the Project

If v1.2.0 makes your life easier:
- ⭐ Star the repo on GitHub
- 🐛 Report any issues you find
- 💡 Suggest features for v1.3.0
- 📢 Share with your Linux friends
- ☕ [Sponsor development](https://github.com/sponsors/strabo231)

---

**Download:** [v1.2.0 Release](https://github.com/strabo231/nautilus-backup-extension/releases/tag/v1.2.0)

**Made with ❤️ for the Linux community**

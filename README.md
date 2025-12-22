# Nautilus Backup Extension

**Easy right-click backups for Ubuntu/Linux!** 🚀

Never lose files again. Just right-click → Backup. No terminal needed!

[![Test Nautilus Backup Extension](https://github.com/yourusername/nautilus-backup-extension/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/nautilus-backup-extension/actions/workflows/test.yml)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
[![Sponsor](https://img.shields.io/github/sponsors/strabo231?label=Sponsor&logo=github&color=ff69b4)](https://github.com/sponsors/strabo231)

## 🎯 The Problem

On Linux, backing up files is unnecessarily complicated:
- ❌ Need to open terminal
- ❌ Remember `cp` command syntax
- ❌ Type out full paths
- ❌ Add timestamps manually
- ❌ Create archives for folders

## ✨ The Solution

**Right-click → Backup. Done!**

This Nautilus extension adds beautiful backup options to your right-click menu. Simple as Windows/macOS, but better.

## 🚀 Features

### ⚡ Quick Backup
Creates timestamped backup in the same folder
- `document.pdf` → `document_backup_2024-12-22_14-30-00.pdf`
- Perfect for quick "save before editing"
- One click, done!

### 💾 Backup As...
Choose custom name and location
- Full file chooser dialog
- Rename on backup
- Save anywhere you want
- Just like "Save As"

### 🗂️ Backup to ~/Backups
Organized backup folder
- All backups in one place
- Easy to find later
- Timestamped for organization
- Automatic folder creation

### 📁 Folder Support
Automatically creates `.tar.gz` archives
- `project/` → `project_backup_2024-12-22_14-30-00.tar.gz`
- Compressed to save space
- Preserves all permissions
- Easy to restore

### 🔔 Desktop Notifications
Visual feedback for every action
- Success notifications
- Error alerts
- No guessing if it worked

### ⚙️ Settings Panel
Configure your preferences
- Change backup folder location
- View backup features
- Open backups folder
- Version information

## 📦 Installation

### One-Line Install

```bash
git clone https://github.com/yourusername/nautilus-backup-extension.git
cd nautilus-backup-extension
./install.sh
```

### Manual Installation

**1. Install Dependencies:**

```bash
# Ubuntu/Debian
sudo apt install python3-nautilus

# Fedora
sudo dnf install nautilus-python

# Arch
sudo pacman -S python-nautilus
```

**2. Install Extension:**

```bash
mkdir -p ~/.local/share/nautilus-python/extensions
cp nautilus-backup.py ~/.local/share/nautilus-python/extensions/
chmod +x ~/.local/share/nautilus-python/extensions/nautilus-backup.py
```

**3. Restart Nautilus:**

```bash
nautilus -q
nautilus &
```

**Done!** Right-click any file to see the Backup menu.

## 🎮 Usage

### Basic Usage

1. **Right-click** any file or folder in Nautilus
2. Look for **🔄 Backup** in the menu
3. Choose your option:
   - **⚡ Quick Backup** - Instant timestamped backup
   - **💾 Backup As...** - Choose name/location
   - **🗂️ Backup to ~/Backups** - Organized storage

### Quick Backup Example

```
Before:  /home/user/Documents/report.docx

After:   /home/user/Documents/report.docx
         /home/user/Documents/report_backup_2024-12-22_14-30-00.docx
```

### Backup As Example

```
1. Right-click report.docx
2. Backup → Backup As...
3. Choose name: report_v2.docx
4. Choose location: /home/user/Archive/
5. Click Save

Result: /home/user/Archive/report_v2.docx
```

### Folder Backup Example

```
Before:  /home/user/Projects/myapp/

After:   /home/user/Backups/myapp_backup_2024-12-22_14-30-00.tar.gz
         (Contains entire folder structure)
```

## 📸 Screenshots

### Right-Click Menu
```
┌─────────────────────────┐
│ Open                    │
│ Open With...            │
│ ──────────────          │
│ Cut                     │
│ Copy                    │
│ Paste                   │
│ ──────────────          │
│ 🔄 Backup             ▶ │ ┌──────────────────────────────┐
│ ──────────────          │ │ ⚡ Quick Backup (Same Folder) │
│ Properties              │ │ 💾 Backup As...               │
└─────────────────────────┘ │ 🗂️ Backup to ~/Backups       │
                             │ ─────────────────────────    │
                             │ ⚙️ Backup Settings            │
                             └──────────────────────────────┘
```

### Backup As Dialog
```
╔══════════════════════════════════════╗
║           Backup As...               ║
╠══════════════════════════════════════╣
║                                      ║
║  Save in: /home/user/Documents  [▼] ║
║                                      ║
║  Name: report_backup_2024-12-2...   ║
║                                      ║
║  ┌────────────────────────────────┐ ║
║  │ document.pdf                   │ ║
║  │ image.png                      │ ║
║  │ report.docx                    │ ║
║  └────────────────────────────────┘ ║
║                                      ║
║          [Cancel]  [Save]            ║
╚══════════════════════════════════════╝
```

### Settings Panel
```
╔════════════════════════════════════════╗
║         Backup Settings                ║
╠════════════════════════════════════════╣
║                                        ║
║  Backup Folder: /home/user/Backups [📁]║
║                                        ║
║  Features:                             ║
║   ⚡ Quick Backup - Timestamped       ║
║   💾 Backup As - Custom name          ║
║   🗂️ Backup to ~/Backups             ║
║   📁 Works with folders (.tar.gz)     ║
║   🔔 Desktop notifications            ║
║                                        ║
║        [Open Backups Folder] [Close]   ║
╚════════════════════════════════════════╝
```

## 🎯 Use Cases

### Before Editing
```bash
Right-click → Quick Backup
# Edit with confidence, original is safe
```

### Weekly Backups
```bash
Right-click → Backup to ~/Backups
# Organized collection of backups
```

### Version Control
```bash
Right-click → Backup As... → project_v1.0.tar.gz
Right-click → Backup As... → project_v1.1.tar.gz
Right-click → Backup As... → project_v2.0.tar.gz
```

### Sharing Backups
```bash
Right-click folder → Backup As... 
# Save to USB/cloud folder
# Already compressed and ready to share
```

### Before System Update
```bash
# Backup important configs
Right-click ~/.bashrc → Backup to ~/Backups
Right-click ~/.config/app/ → Backup to ~/Backups
# Update system safely
```

## ⚙️ Configuration

### Change Backup Folder

1. Right-click any file → Backup → Backup Settings
2. Click "Browse" next to Backup Folder
3. Select new location
4. Settings auto-save

Or manually edit:
```bash
echo "/path/to/backup/folder" > ~/.config/nautilus-backup/config.txt
```

### Default Backup Location

By default: `~/Backups`

Change it anytime via Settings dialog.

## 🔧 Troubleshooting

### Menu Not Appearing?

**1. Check dependencies:**
```bash
python3 -c "import gi; gi.require_version('Nautilus', '3.0')"
```
If error, install: `sudo apt install python3-nautilus`

**2. Restart Nautilus:**
```bash
nautilus -q
nautilus &
```

**3. Check installation:**
```bash
ls ~/.local/share/nautilus-python/extensions/nautilus-backup.py
```

**4. Check permissions:**
```bash
chmod +x ~/.local/share/nautilus-python/extensions/nautilus-backup.py
```

### Nautilus Version Issues

This extension works with:
- Nautilus 3.x (Ubuntu 18.04+)
- Nautilus 4.x (Ubuntu 22.04+)
- GNOME Files 40+

For older versions, you may need `python-nautilus` instead of `python3-nautilus`.

### Import Errors

If you see import errors:
```bash
# Install GObject introspection
sudo apt install python3-gi gir1.2-gtk-3.0

# Reinstall nautilus-python
sudo apt install --reinstall python3-nautilus
```

### Extension Not Loading

Check Nautilus logs:
```bash
nautilus -q
nautilus 2>&1 | grep -i backup
```

Verify Python path:
```bash
python3 -c "import sys; print('\n'.join(sys.path))"
```

### Backup Fails

**Permission denied:**
- Check destination folder permissions
- Try backing up to ~/Backups instead

**No space left:**
- Check disk space: `df -h`
- Clean up old backups

**Folder too large:**
- Compression may take time
- Check system resources
- Consider excluding large files

## 🗑️ Uninstallation

### Easy Uninstall

```bash
./uninstall.sh
```

### Manual Uninstall

```bash
rm ~/.local/share/nautilus-python/extensions/nautilus-backup.py
rm -rf ~/.config/nautilus-backup
nautilus -q
```

Your backup files in `~/Backups` are NOT deleted.

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Restore from backup option
- [ ] Compare file with backup
- [ ] Auto-cleanup old backups (keep last N)
- [ ] Backup scheduling
- [ ] Exclude patterns for folders
- [ ] Progress bar for large backups
- [ ] Backup history view
- [ ] Cloud storage integration

## 📋 Requirements

- **OS:** Ubuntu/Debian/Fedora/Arch Linux
- **Desktop:** GNOME (with Nautilus)
- **Python:** 3.6+
- **Dependencies:** python3-nautilus

## 🐛 Known Issues

- Very large folders (>10GB) may take time to compress
- No progress bar for long operations (yet)
- Settings changes require Nautilus restart in some cases

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 👤 Author

Created with ❤️ for the Linux community

## 🌟 Acknowledgments

- Nautilus Python extension framework
- GNOME community
- All the frustrated users who just wanted to right-click → backup

## 🔮 Future Plans

### v1.1.0
- Restore from backup
- Compare files
- Auto-cleanup options

### v1.2.0
- Multiple backup profiles
- Exclude patterns
- Progress dialogs

### v1.3.0
- Backup scheduling
- Automatic backups
- Version control integration

## 💡 Tips & Tricks

**Quick Alias:**
```bash
# Add to ~/.bashrc
alias backup='nautilus $(pwd) &'
# Opens current folder in Nautilus for easy backups
```

**Keyboard Shortcut:**
1. Right-click file
2. Press 'B' (highlights Backup)
3. Press Enter
4. Press 'Q' (Quick Backup)

**Batch Backup:**
- Select multiple files (Ctrl+Click)
- Right-click → Quick Backup
- All files backed up at once!

**Backup Script Integration:**
```bash
#!/bin/bash
# Auto-backup important files on login
important_files=(
    "$HOME/.bashrc"
    "$HOME/.ssh/config"
)

for file in "${important_files[@]}"; do
    # Uses the same timestamp format
    cp "$file" "$file.backup.$(date +%Y-%m-%d_%H-%M-%S)"
done
```

---

**Made backups effortless? ⭐ Star this repo!**

**Questions or issues?** Open a GitHub issue!

**Enjoy hassle-free backups!** 🚀📦

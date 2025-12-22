# User Guide - Nautilus Backup Extension

Complete guide to mastering file backups in Linux!

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Best Practices](#best-practices)
6. [Comparison with Other Methods](#comparison)
7. [FAQ](#faq)

---

## Introduction

### What is this?

A Nautilus extension that adds **right-click backup functionality** to Ubuntu/Linux, just like Windows and macOS have built-in.

### Why do you need it?

**Without this extension:**
```bash
# Manual terminal commands
cp important.txt important_backup_$(date +%Y-%m-%d).txt
tar -czf project_backup.tar.gz project/
# Every. Single. Time. 😫
```

**With this extension:**
```
Right-click → Backup → Done! 🎉
```

### Key Benefits

✅ **Zero terminal commands**  
✅ **Automatic timestamps**  
✅ **Visual feedback**  
✅ **Works like native OS feature**  
✅ **Handles files and folders**  
✅ **Desktop notifications**  

---

## Installation

### Prerequisites Check

```bash
# Check Nautilus version
nautilus --version

# Check Python
python3 --version
```

### Quick Install

```bash
git clone https://github.com/yourusername/nautilus-backup-extension.git
cd nautilus-backup-extension
chmod +x install.sh
./install.sh
```

The installer will:
1. ✓ Check for dependencies
2. ✓ Install `python3-nautilus` if needed (asks for sudo)
3. ✓ Copy extension to correct location
4. ✓ Create backup folder (`~/Backups`)
5. ✓ Restart Nautilus
6. ✓ Show success message

### Verify Installation

```bash
# Check extension is installed
ls ~/.local/share/nautilus-python/extensions/nautilus-backup.py

# Open Nautilus and right-click any file
# You should see "🔄 Backup" in menu
```

---

## Basic Usage

### Quick Backup (Most Common)

**When to use:** Before editing a file, quick safety copy

**Steps:**
1. Right-click file/folder
2. Hover over **🔄 Backup**
3. Click **⚡ Quick Backup (Same Folder)**
4. Done! 

**Result:**
```
Original:  report.docx
Backup:    report_backup_2024-12-22_14-30-00.docx
           ↑ Same folder, timestamped
```

**Notification:**
```
╔════════════════════════════╗
║   Backup Complete ✓        ║
╠════════════════════════════╣
║ Backed up to:              ║
║ /home/user/Documents       ║
╚════════════════════════════╝
```

### Backup As... (Custom)

**When to use:** Archive with specific name, save to different location

**Steps:**
1. Right-click file/folder
2. Hover over **🔄 Backup**
3. Click **💾 Backup As...**
4. Choose name (or keep suggested)
5. Choose location
6. Click **Save**

**Example Dialog:**
```
╔══════════════════════════════════════╗
║           Backup As...               ║
╠══════════════════════════════════════╣
║ Save in: ~/Documents          [▼]   ║
║ Name: project_v1.0.tar.gz            ║
║                                      ║
║ [Cancel]              [Save]         ║
╚══════════════════════════════════════╝
```

### Backup to ~/Backups (Organized)

**When to use:** Regular backups, keeping all backups in one place

**Steps:**
1. Right-click file/folder
2. Hover over **🔄 Backup**
3. Click **🗂️ Backup to ~/Backups**
4. Done!

**Result:**
All backups organized in `~/Backups/`:
```
~/Backups/
├── report_backup_2024-12-20_10-00-00.docx
├── report_backup_2024-12-21_15-30-00.docx
├── report_backup_2024-12-22_14-30-00.docx
├── project_backup_2024-12-22_14-35-00.tar.gz
└── image_backup_2024-12-22_14-40-00.png
```

---

## Advanced Features

### Multiple File Backup

Select multiple files at once:

**Steps:**
1. Hold **Ctrl** and click multiple files
2. Right-click selection
3. Choose backup option
4. All files backed up with one click!

**Example:**
```
Selected:
  ✓ report.docx
  ✓ presentation.pptx
  ✓ data.xlsx

After Quick Backup:
  ✓ report_backup_2024-12-22_14-30-00.docx
  ✓ presentation_backup_2024-12-22_14-30-01.pptx
  ✓ data_backup_2024-12-22_14-30-02.xlsx
```

### Folder Backup (Compression)

**Automatic tar.gz creation:**

When you backup a folder, it's automatically compressed:

```
Folder:  ~/Projects/myapp/
         ├── src/
         ├── docs/
         └── config/

Backup:  myapp_backup_2024-12-22_14-30-00.tar.gz
         (All contents preserved, compressed)
```

**Benefits:**
- ✓ Saves disk space (compression)
- ✓ Single file to manage
- ✓ Easy to share
- ✓ Preserves structure and permissions

### Settings Configuration

**Access Settings:**
1. Right-click any file
2. Backup → **⚙️ Backup Settings**

**Settings Panel:**
```
╔════════════════════════════════════════╗
║         Backup Settings                ║
╠════════════════════════════════════════╣
║                                        ║
║  Backup Folder:                        ║
║  /home/user/Backups        [Browse]    ║
║                                        ║
║  Features:                             ║
║   ⚡ Quick Backup - Timestamped       ║
║   💾 Backup As - Custom name          ║
║   🗂️ Backup to ~/Backups             ║
║   📁 Works with folders (.tar.gz)     ║
║   🔔 Desktop notifications            ║
║                                        ║
║  v1.0.0                                ║
║                                        ║
║  [Open Backups Folder]    [Close]      ║
╚════════════════════════════════════════╝
```

**Change Backup Folder:**
1. Click **Browse**
2. Select new location
3. Auto-saves!

---

## Best Practices

### Before Editing Important Files

```
✓ Right-click → Quick Backup
✓ Edit file
✓ If mistakes → Use backup
✓ If good → Delete backup (or keep)
```

### Regular Backup Schedule

**Daily:**
```bash
# Important configs
~/.bashrc → Backup to ~/Backups
~/.ssh/config → Backup to ~/Backups
```

**Weekly:**
```bash
# Project folders
~/Projects/current-project/ → Backup to ~/Backups
~/Documents/important/ → Backup to ~/Backups
```

**Before System Changes:**
```bash
# System configs (if editing)
/etc/fstab → Backup As... → ~/safe-place/
/etc/ssh/sshd_config → Backup As...
```

### Naming Conventions

**Use Backup As... for versions:**
```
project_v1.0.tar.gz
project_v1.1.tar.gz
project_v2.0.tar.gz
project_v2.0_final.tar.gz
project_v2.0_final_FINAL.tar.gz  😅
```

**Use Quick Backup for iterations:**
```
document.txt
document_backup_2024-12-22_10-00-00.txt  (morning version)
document_backup_2024-12-22_15-00-00.txt  (afternoon version)
document_backup_2024-12-22_18-00-00.txt  (final version)
```

### Cleanup Old Backups

**Manual cleanup:**
```bash
# View backups sorted by date
ls -lt ~/Backups/

# Remove old ones
rm ~/Backups/*_2024-01-*
```

**Keep last N backups:**
```bash
# Keep only last 10 backups of a file
ls -t ~/Backups/report_backup_* | tail -n +11 | xargs rm
```

---

## Comparison

### vs. Terminal Commands

| Feature | Terminal `cp` | Nautilus Backup |
|---------|---------------|-----------------|
| **Ease of use** | ❌ Complex | ✅ Right-click |
| **Timestamps** | ❌ Manual | ✅ Automatic |
| **Folder compression** | ❌ Separate tar | ✅ Automatic |
| **Visual feedback** | ❌ None | ✅ Notifications |
| **Choose location** | ✅ Yes | ✅ GUI dialog |
| **Undo mistakes** | ❌ No | ✅ Easy restore |
| **Learning curve** | ❌ High | ✅ Zero |

### vs. Backup Software

| Feature | Timeshift/Déjà Dup | Nautilus Backup |
|---------|-------------------|-----------------|
| **Quick single file** | ❌ Overkill | ✅ Perfect |
| **System restore** | ✅ Yes | ❌ Not designed for |
| **Manual control** | ⚠️ Limited | ✅ Full control |
| **Instant backup** | ❌ Scheduled | ✅ On-demand |
| **Same folder** | ❌ No | ✅ Yes |
| **Setup time** | ⚠️ 15 min | ✅ 2 min |

### vs. Cloud Storage

| Feature | Dropbox/Google Drive | Nautilus Backup |
|---------|---------------------|-----------------|
| **Offline** | ❌ Needs internet | ✅ Works offline |
| **Speed** | ⚠️ Upload time | ✅ Instant |
| **Privacy** | ⚠️ Cloud stored | ✅ Local only |
| **Cost** | ⚠️ Subscription | ✅ Free |
| **Versioning** | ✅ Auto | ✅ Manual |
| **Access anywhere** | ✅ Yes | ❌ Local only |

### vs. Git Version Control

| Feature | Git | Nautilus Backup |
|---------|-----|-----------------|
| **For code** | ✅ Perfect | ⚠️ Works but basic |
| **For documents** | ⚠️ Overkill | ✅ Perfect |
| **Learning curve** | ❌ High | ✅ Zero |
| **Single files** | ⚠️ Commit needed | ✅ One click |
| **Diff/merge** | ✅ Advanced | ❌ No |
| **Quick backup** | ❌ Ceremony | ✅ Instant |

**Best of both worlds:** Use Git for code, Nautilus Backup for documents/configs!

---

## FAQ

### Q: Where are my backups stored?

**A:** By default in `~/Backups/`. Change this in Settings.

Quick Backup saves to the same folder as the original.

---

### Q: Can I restore from backup?

**A:** Yes! Just:
1. Find your backup file
2. Copy it over the current file
3. Or rename the backup to remove `_backup_timestamp`

Future version will have "Restore" right-click option!

---

### Q: What about large files/folders?

**A:** Folders are automatically compressed (tar.gz), saving space.

For very large folders (>10GB), compression takes time but works fine.

---

### Q: Can I backup to external drive/USB?

**A:** Yes! Use "Backup As..." and select your external drive location.

Or change default backup folder in Settings to your external drive.

---

### Q: Does it work with network drives?

**A:** Yes! Works with any location Nautilus can access:
- SMB/CIFS shares
- NFS mounts
- SSHFS
- Cloud storage mounts (rclone, etc.)

---

### Q: How do I backup multiple files at once?

**A:** 
1. Select all files (Ctrl+Click or Ctrl+A)
2. Right-click
3. Choose backup option
4. All selected files backed up!

---

### Q: What's the timestamp format?

**A:** `YYYY-MM-DD_HH-MM-SS`

Example: `2024-12-22_14-30-00`

This sorts chronologically and avoids file name conflicts.

---

### Q: Can I customize the timestamp format?

**A:** Currently no, but it's on the roadmap! (v1.1.0)

Current format is internationally standard and sorts properly.

---

### Q: Does it preserve file permissions?

**A:** Yes! Uses Python's `shutil.copy2` which preserves:
- Permissions
- Timestamps
- Metadata

For folders, `tar` preserves everything.

---

### Q: What if backup already exists?

**A:** Timestamps prevent conflicts. Each backup gets unique timestamp.

If backing up twice in same second, system handles it (rarely happens).

---

### Q: Can I schedule automatic backups?

**A:** Not yet. This is for on-demand backups.

For scheduled backups, use:
- Timeshift (system)
- Déjà Dup (files)
- Cron + rsync (custom)

Or wait for v1.2.0 which will have scheduling!

---

### Q: Does it work on other file managers?

**A:** Currently only Nautilus (GNOME Files).

Potential future support:
- Nemo (Cinnamon) - Easy port
- Caja (MATE) - Easy port
- Thunar (XFCE) - Different system
- Dolphin (KDE) - Different system

Want it for your file manager? Open a feature request!

---

### Q: Is it safe?

**A:** Yes! The extension:
- ✓ Only reads/copies files (never modifies originals)
- ✓ Shows confirmation for destructive operations
- ✓ Uses standard Python libraries
- ✓ Open source (audit the code!)

---

### Q: Why not just use `cp`?

**A:** You can! But this is much faster and easier:

**Terminal way:**
```bash
cp important.txt important_backup_$(date +%Y-%m-%d_%H-%M-%S).txt
```

**This way:**
```
Right-click → Quick Backup
```

No comparison! 😊

---

### Q: Can I integrate with my backup script?

**A:** Yes! The extension uses standard file operations.

Your scripts can work alongside it. Example:
```bash
#!/bin/bash
# Your automated backup script
rsync -av ~/Documents/ ~/Backups/automated/

# Manual backups via extension go to ~/Backups/
# No conflict!
```

---

### Q: What about symbolic links?

**A:** Symbolic links are preserved by default.

For folders, `tar` includes the links (not dereferenced).

---

### Q: Maximum file size?

**A:** No artificial limit. Limited only by:
- Available disk space
- File system limits
- Time (large files take time to copy)

---

### Q: Does it work on Wayland?

**A:** Yes! Tested on both X11 and Wayland.

Notifications work on both.

---

### Q: How do I uninstall?

**A:**
```bash
./uninstall.sh
```

Or manually:
```bash
rm ~/.local/share/nautilus-python/extensions/nautilus-backup.py
nautilus -q
```

Your backup files remain untouched.

---

## Tips & Tricks

### Keyboard Shortcut Flow

```
1. Right-click (or Menu key)
2. Press 'B' (highlights Backup)
3. Press '→' (opens submenu)
4. Press 'Q' (Quick Backup)

Total: 4 keystrokes!
```

### Batch Backup Before Changes

```bash
# Select all configs
Ctrl+A in ~/.config/app/

# Backup all
Right-click → Quick Backup

# Now safely edit
```

### USB Backup Workflow

```
1. Plug in USB
2. Mount it (auto-mounts usually)
3. Right-click files → Backup As...
4. Choose USB location
5. Done! Safe external backup
```

### Git + Nautilus Backup

```
Project workflow:
1. Work in progress → Nautilus Quick Backup
2. Feature complete → Git commit
3. Release ready → Nautilus Backup As v1.0
```

---

## Troubleshooting Extended

### Extension loaded but menu not showing

**Check Nautilus extensions:**
```bash
python3 << EOF
import gi
gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus
EOF
```

If error → reinstall python3-nautilus

---

### Backup fails silently

**Check permissions:**
```bash
# Can you write to destination?
touch ~/Backups/test.txt
rm ~/Backups/test.txt

# Can you read source?
cat /path/to/file > /dev/null
```

---

### Notifications not showing

**Check notification daemon:**
```bash
notify-send "Test" "Testing notifications"
```

If nothing shows → notification system issue (not extension).

---

### Folder backup very slow

**Large folder?**
```bash
du -sh /path/to/folder
```

If >5GB → Takes time to compress. This is normal.

Consider excluding large files or using Backup As to uncompressed location.

---

## Support

**Issues?** Check:
1. This guide
2. README.md
3. GitHub Issues
4. Ask the community

**Feature requests?** Open a GitHub issue!

**Contributing?** PRs welcome!

---

**Happy backing up!** 🚀📦

*Remember: The best backup is the one you actually do!*

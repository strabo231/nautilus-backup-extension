# Quick Start Guide

Get up and running in 2 minutes! ⚡

## Install

```bash
# 1. Clone
git clone https://github.com/strabo231/nautilus-backup-extension.git
cd nautilus-backup-extension

# 2. Install
./install.sh

# 3. Done!
```

## Use

**Right-click any file** → Look for **🔄 Backup**

### Three Options:

1. **⚡ Quick Backup**
   - Creates: `file_backup_2024-12-22_14-30-00.ext`
   - Location: Same folder
   - Use for: Quick safety copies

2. **💾 Backup As...**
   - Choose name and location
   - Use for: Organized archiving

3. **🗂️ Backup to ~/Backups**
   - Auto-organized folder
   - Use for: Central backup storage

## Examples

### Before Editing
```
1. Right-click report.docx
2. Quick Backup
3. Edit safely!
```

### Make Archive
```
1. Right-click project/
2. Backup As...
3. Save to USB: project_final.tar.gz
```

### Regular Backups
```
1. Right-click important.txt
2. Backup to ~/Backups
3. Find all backups in one place
```

## Tips

- **Folders** → Automatic `.tar.gz` compression
- **Multiple files** → Select all, backup once
- **Settings** → Right-click → Backup → Backup Settings

## Troubleshooting

Menu not showing?
```bash
nautilus -q
nautilus &
```

Still not working?
```bash
sudo apt install python3-nautilus
./install.sh
```

## Uninstall

```bash
./uninstall.sh
```

Your backup files stay safe in `~/Backups`!

---

**That's it! Enjoy easy backups!** 🚀

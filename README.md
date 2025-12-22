<div align="center">

# 🔄 Nautilus Backup Extension

### Easy Right-Click Backups for Ubuntu & Linux

**Never lose files again. Just right-click → Backup. No terminal needed!**

[![Test Status](https://github.com/strabo231/nautilus-backup-extension/actions/workflows/test.yml/badge.svg)](https://github.com/strabo231/nautilus-backup-extension/actions/workflows/test.yml)
[![Version](https://img.shields.io/badge/version-1.0.1-blue)](https://github.com/strabo231/nautilus-backup-extension/releases)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04%20|%2022.04%20|%2024.04-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![GNOME](https://img.shields.io/badge/GNOME-Nautilus-4A86CF?logo=gnome&logoColor=white)](https://wiki.gnome.org/Apps/Files)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Sponsor](https://img.shields.io/github/sponsors/strabo231?label=Sponsor&logo=github&color=ff69b4)](https://github.com/sponsors/strabo231)

![GitHub stars](https://img.shields.io/github/stars/strabo231/nautilus-backup-extension?style=social)
![GitHub forks](https://img.shields.io/github/forks/strabo231/nautilus-backup-extension?style=social)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

</div>

## ✨ What's New in v1.0.1

- 🎯 **Full Ubuntu 24.04 LTS support** - Works with latest Nautilus 46!
- 🐛 **Critical bug fixes** - Config persistence and stability improvements
- ⚡ **Better multi-file backups** - Enhanced handling for batch operations
- 📚 **Updated documentation** - Comprehensive guides for all Ubuntu LTS versions

---

## 🎯 The Problem

On Linux, backing up files is unnecessarily complicated:

<table>
<tr>
<td>

**❌ The Old Way**
- Open terminal
- Remember `cp` command syntax  
- Type out full paths
- Add timestamps manually
- Create archives for folders

</td>
<td>

**✅ The New Way**
- Right-click file
- Select "Backup"
- Done! ✨

</td>
</tr>
</table>

---

## 🚀 Features

<table>
<tr>
<td width="50%">

### ⚡ Quick Backup
Creates timestamped backup in the same folder

```
document.pdf
  ↓
document_backup_2024-12-22_14-30-00.pdf
```

Perfect for quick "save before editing"

</td>
<td width="50%">

### 💾 Backup As...
Choose custom name and location

- Full file chooser dialog
- Rename on backup
- Save anywhere you want
- Just like "Save As"

</td>
</tr>
<tr>
<td>

### 🗂️ Backup to ~/Backups
Organized backup folder

- All backups in one place
- Easy to find later
- Timestamped automatically
- Opens from settings

</td>
<td>

### 📁 Folder Support
Automatic `.tar.gz` compression

```
project/
  ↓
project_backup_2024-12-22.tar.gz
```

Preserves all permissions & structure

</td>
</tr>
</table>

### More Features

- 🔔 **Desktop Notifications** - Visual feedback for every action
- ⚙️ **Settings Panel** - Configure backup folder and preferences
- 🎨 **Native GNOME Integration** - Beautiful, consistent UI
- 🚀 **Fast & Lightweight** - Instant backups, no performance impact
- 🔒 **Safe & Reliable** - Preserves file permissions and metadata

---

## 📦 Installation

### Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/strabo231/nautilus-backup-extension.git
cd nautilus-backup-extension

# Run installer (automatically detects your Nautilus version)
./install.sh
```

**That's it!** The installer handles everything:
- ✅ Detects Ubuntu 20.04, 22.04, or 24.04
- ✅ Checks for Nautilus 3.x or 4.x
- ✅ Installs dependencies if needed
- ✅ Sets up the extension
- ✅ Restarts Nautilus

### Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

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

</details>

### Verify Installation

Right-click any file in Nautilus. You should see **🔄 Backup** in the menu!

---

## 🎮 Usage

### Basic Usage

1. **Right-click** any file or folder in Nautilus
2. Look for **🔄 Backup** in the context menu
3. Choose your option:
   - **⚡ Quick Backup** - Instant timestamped backup
   - **💾 Backup As...** - Choose name/location
   - **🗂️ Backup to ~/Backups** - Organized storage

### Real-World Examples

<details>
<summary><b>Before Editing Important Files</b></summary>

```
Scenario: About to edit a config file

1. Right-click /etc/nginx/nginx.conf
2. Backup → Quick Backup
3. Edit safely! Original is backed up as:
   nginx.conf.backup_2024-12-22_14-30-00
```

</details>

<details>
<summary><b>Creating Project Archives</b></summary>

```
Scenario: Archiving a project folder

1. Right-click ~/Projects/myapp/
2. Backup → Backup As...
3. Choose: ~/Archive/myapp_v1.0.tar.gz
4. Share or store the compressed archive
```

</details>

<details>
<summary><b>Regular Backup Routine</b></summary>

```
Scenario: Daily backup of important files

1. Select multiple files (Ctrl+Click)
2. Right-click → Backup → Backup to ~/Backups
3. All files backed up with timestamps
4. Check ~/Backups anytime to find them
```

</details>

---

## 💻 System Requirements

<table>
<tr>
<td width="50%">

### ✅ Supported Systems

**Ubuntu LTS (Officially Tested):**
- 🟢 **Ubuntu 24.04 LTS (Noble)** - Nautilus 46
- 🟢 **Ubuntu 22.04 LTS (Jammy)** - Nautilus 42  
- 🟢 **Ubuntu 20.04 LTS (Focal)** - Nautilus 3.36

**Other Distros** (Should work):
- Debian 11+
- Fedora 35+
- Pop!_OS 22.04+
- Linux Mint 20+
- Arch Linux (current)

</td>
<td width="50%">

### 🔧 Requirements

**Software:**
- Python 3.8 or higher
- Nautilus 3.x or 4.x
- python3-nautilus package
- GTK 3.24+ or GTK 4.x

**Desktop:**
- GNOME (with Nautilus/Files)
- Any GNOME-based environment

**Hardware:**
- Minimal (runs on any system that runs Nautilus)

</td>
</tr>
</table>

---

## 📸 Screenshots

<details>
<summary><b>Right-Click Menu</b></summary>

```
┌─────────────────────────┐
│ Open                    │
│ Open With...            │
│ ────────────────        │
│ Cut                     │
│ Copy                    │
│ Paste                   │
│ ────────────────        │
│ 🔄 Backup             ▶ │ ┌──────────────────────────────┐
│ ────────────────        │ │ ⚡ Quick Backup (Same Folder) │
│ Properties              │ │ 💾 Backup As...               │
└─────────────────────────┘ │ 🗂️ Backup to ~/Backups       │
                             │ ──────────────────────────    │
                             │ ⚙️ Backup Settings            │
                             └──────────────────────────────┘
```

</details>

<details>
<summary><b>Backup As Dialog</b></summary>

```
╔═══════════════════════════════════╗
║         Backup As...               ║
╠═══════════════════════════════════╣
║                                   ║
║  Save in: /home/user/Documents  ▼ ║
║                                   ║
║  Name: report_backup_2024-12-...  ║
║                                   ║
║  ┌─────────────────────────────┐ ║
║  │ document.pdf                │ ║
║  │ image.png                   │ ║
║  │ report.docx                 │ ║
║  └─────────────────────────────┘ ║
║                                   ║
║          [Cancel]  [Save]         ║
╚═══════════════════════════════════╝
```

</details>

<details>
<summary><b>Settings Panel</b></summary>

```
╔════════════════════════════════════╗
║       Backup Settings              ║
╠════════════════════════════════════╣
║                                    ║
║  Backup Folder:                    ║
║  /home/user/Backups         [📁]   ║
║                                    ║
║  Features:                         ║
║   ⚡ Quick Backup - Timestamped    ║
║   💾 Backup As - Custom location   ║
║   🗂️ Backup to ~/Backups           ║
║   📁 Folder support (.tar.gz)      ║
║   🔔 Desktop notifications         ║
║                                    ║
║   [Open Backups Folder]  [Close]   ║
╚════════════════════════════════════╝
```

</details>

---

## 🎯 Use Cases

| Scenario | Solution |
|----------|----------|
| 📝 **Before editing config files** | Quick Backup → Edit safely |
| 💼 **Version control for documents** | Backup As → `document_v1.docx`, `document_v2.docx` |
| 📦 **Project archiving** | Backup folder → Auto-compressed `.tar.gz` |
| 🔄 **Regular backups** | Backup to ~/Backups → All in one place |
| 🚀 **Before system updates** | Backup configs → Restore if needed |
| 📤 **Sharing with USB/cloud** | Backup As to USB/Dropbox folder |

---

## 🔧 Troubleshooting

<details>
<summary><b>Menu Not Appearing?</b></summary>

**1. Check dependencies:**
```bash
python3 -c "import gi; gi.require_version('Nautilus', '3.0')"
# Or for Nautilus 4.x:
python3 -c "import gi; gi.require_version('Nautilus', '4.0')"
```

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

</details>

<details>
<summary><b>Extension Not Loading?</b></summary>

**Check Nautilus logs:**
```bash
nautilus -q
NAUTILUS_EXTENSION_DEBUG=1 nautilus 2>&1 | grep -i backup
```

**Verify Python path:**
```bash
python3 -c "import sys; print('\n'.join(sys.path))"
```

</details>

<details>
<summary><b>Backup Fails?</b></summary>

**Common causes:**
- ❌ Permission denied → Try backing up to ~/Backups
- ❌ No space left → Check disk: `df -h`
- ❌ Folder too large → May take time to compress

**Check logs:**
```bash
journalctl -xe | grep -i backup
```

</details>

### Still Having Issues?

[Open an issue](https://github.com/strabo231/nautilus-backup-extension/issues) with:
- Your Ubuntu version (`lsb_release -a`)
- Nautilus version (`nautilus --version`)
- Python version (`python3 --version`)
- Error messages from logs

---

## 📚 Documentation

- [📖 Quick Start Guide](QUICKSTART.md) - Get started in 2 minutes
- [📘 User Guide](USER_GUIDE.md) - Comprehensive usage guide
- [✨ Features](FEATURES.md) - Detailed feature documentation
- [🤝 Contributing](CONTRIBUTING.md) - How to contribute
- [📋 Changelog](CHANGELOG.md) - Version history

---

## 🗑️ Uninstallation

```bash
./uninstall.sh
```

Your backup files in `~/Backups` are **NOT deleted** - only the extension is removed.

### Manual Uninstall

```bash
rm ~/.local/share/nautilus-python/extensions/nautilus-backup.py
rm -rf ~/.config/nautilus-backup
nautilus -q
```

---

## 🤝 Contributing

Contributions are welcome! We'd love help with:

- [ ] Restore from backup feature
- [ ] Compare file with backup (diff view)
- [ ] Auto-cleanup old backups (keep last N)
- [ ] Backup scheduling
- [ ] Progress bars for large operations
- [ ] Cloud storage integration (Dropbox, Google Drive)

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🌟 Show Your Support

If this extension makes your life easier:

- ⭐ **Star this repo** - Helps others discover it!
- 🐛 **Report bugs** - Help make it better
- 💡 **Suggest features** - Tell us what you need
- 📢 **Share it** - Tell your Linux friends
- ☕ **[Sponsor](https://github.com/sponsors/strabo231)** - Support development

---

## 📊 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/strabo231/nautilus-backup-extension)
![GitHub code size](https://img.shields.io/github/languages/code-size/strabo231/nautilus-backup-extension)
![GitHub issues](https://img.shields.io/github/issues/strabo231/nautilus-backup-extension)
![GitHub pull requests](https://img.shields.io/github/issues-pr/strabo231/nautilus-backup-extension)
![GitHub last commit](https://img.shields.io/github/last-commit/strabo231/nautilus-backup-extension)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/strabo231/nautilus-backup-extension)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### What This Means

✅ **You can:**
- Use it commercially
- Modify the code
- Distribute it
- Use it privately

❌ **You must:**
- Include the license
- Include copyright notice

❌ **No warranty** - Provided "as is"

---

## 💖 Acknowledgments

- **Nautilus Python Extension Framework** - For making extensions possible
- **GNOME Community** - For excellent documentation
- **All Contributors** - Thank you for making this better!
- **Linux Community** - For feedback and support

Special thanks to everyone who:
- Reported bugs
- Suggested features  
- Starred the repo
- Shared with others

---

## 🔮 Roadmap

### v1.1.0 (Planned)
- ✨ Restore from backup
- 📊 Backup history view
- 🗑️ Auto-cleanup options

### v1.2.0 (Future)
- 📅 Scheduled backups
- ☁️ Cloud storage integration
- 🔄 Incremental backups

### v2.0.0 (Ideas)
- 🎨 Theme customization
- 🌐 Multi-language support
- 🔌 Plugin system

---

## 💬 Community

- **Issues:** [GitHub Issues](https://github.com/strabo231/nautilus-backup-extension/issues)
- **Discussions:** [GitHub Discussions](https://github.com/strabo231/nautilus-backup-extension/discussions)
- **Reddit:** [r/Ubuntu](https://reddit.com/r/Ubuntu)
- **Discord:** *Coming soon*

---

## 📞 Contact

- **GitHub:** [@strabo231](https://github.com/strabo231)
- **Issues:** [Report a bug](https://github.com/strabo231/nautilus-backup-extension/issues/new)
- **Email:** *Via GitHub profile*

---

<div align="center">

### ⭐ Star Us on GitHub!

If you find this extension useful, please consider giving it a star.  
It helps others discover the project and motivates continued development!

[![GitHub stars](https://img.shields.io/github/stars/strabo231/nautilus-backup-extension?style=social)](https://github.com/strabo231/nautilus-backup-extension)

**Made with ❤️ for the Linux community**

[🔝 Back to Top](#-nautilus-backup-extension)

</div>

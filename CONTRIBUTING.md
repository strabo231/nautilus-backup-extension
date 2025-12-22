# Contributing to Nautilus Backup Extension

Thank you for your interest in contributing! 🎉

## How to Contribute

### 🐛 Reporting Bugs

**Before submitting:**
- Check existing issues to avoid duplicates
- Test with the latest version
- Gather system information

**Bug report should include:**
- OS and version (`lsb_release -a`)
- Nautilus version (`nautilus --version`)
- Python version (`python3 --version`)
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs
- Screenshots if relevant

**Template:**
```markdown
**Environment:**
- OS: Ubuntu 22.04
- Nautilus: 42.2
- Python: 3.10.6

**Steps to reproduce:**
1. Right-click file
2. Select Backup → Quick Backup
3. ...

**Expected:** File should be backed up
**Actual:** Error notification appears

**Error message:**
```
[Paste error here]
```

**Screenshots:** [If applicable]
```

### ✨ Suggesting Features

**Good feature requests include:**
- Clear use case
- Expected behavior
- Why it's valuable
- Potential implementation ideas

**Examples of good requests:**
- "Add restore from backup option for easy recovery"
- "Support backup scheduling for automatic backups"
- "Add option to keep only last N backups (auto-cleanup)"

### 🔧 Pull Requests

**Before you start:**
1. Open an issue to discuss the change
2. Fork the repository
3. Create a feature branch
4. Make your changes
5. Test thoroughly
6. Submit PR

**PR Guidelines:**

#### Code Style
```python
# Follow PEP 8
# Use descriptive variable names
# Add docstrings to functions

def backup_file(source_path, dest_path):
    """
    Create backup of a file.
    
    Args:
        source_path: Path to source file
        dest_path: Path to backup destination
        
    Returns:
        tuple: (success: bool, error: str or None)
    """
    pass
```

#### Testing
- Test on Ubuntu 22.04 and 20.04 if possible
- Test with files and folders
- Test error cases (permissions, disk space)
- Verify notifications work

#### Commit Messages
```bash
# Good commit messages
git commit -m "Add restore from backup feature"
git commit -m "Fix: Handle permission errors gracefully"
git commit -m "Docs: Update README with new feature"

# Bad commit messages
git commit -m "fix bug"
git commit -m "updates"
git commit -m "asdf"
```

**Commit prefixes:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style/formatting
- `refactor:` Code refactoring
- `test:` Add/update tests
- `chore:` Maintenance

### 📝 Development Setup

**1. Fork and clone:**
```bash
git clone https://github.com/YOUR-USERNAME/nautilus-backup-extension.git
cd nautilus-backup-extension
```

**2. Install dependencies:**
```bash
sudo apt install python3-nautilus python3-gi
```

**3. Install for development:**
```bash
./install.sh
```

**4. Make changes:**
```bash
# Edit nautilus-backup.py
nano nautilus-backup.py

# Restart Nautilus to test
nautilus -q
nautilus &
```

**5. Test your changes:**
```bash
# Run tests
python3 -m py_compile nautilus-backup.py

# Test manually in Nautilus
# Try all features
```

### 🧪 Testing Checklist

Before submitting PR, verify:

**Functionality:**
- [ ] Quick Backup works
- [ ] Backup As works
- [ ] Backup to ~/Backups works
- [ ] Settings dialog works
- [ ] Single file backup works
- [ ] Folder backup works
- [ ] Multiple file backup works

**Error Handling:**
- [ ] Permission denied handled
- [ ] Disk full handled
- [ ] Invalid path handled
- [ ] Large file/folder works
- [ ] Special characters in filename work

**UI/UX:**
- [ ] Notifications appear
- [ ] Error messages are clear
- [ ] Progress indication (if applicable)
- [ ] Settings save properly

**Compatibility:**
- [ ] Works on Ubuntu 22.04
- [ ] Works on Ubuntu 20.04
- [ ] Python 3.8+ compatible
- [ ] Nautilus 3.x compatible
- [ ] Nautilus 4.x compatible

### 📚 Documentation

**Update docs when:**
- Adding new features
- Changing behavior
- Fixing bugs that need clarification
- Adding configuration options

**Files to update:**
- `README.md` - Main documentation
- `QUICKSTART.md` - If installation changes
- `USER_GUIDE.md` - If adding features/FAQs
- `FEATURES.md` - If adding features

### 🎯 Priority Areas

**High Priority:**
- Bug fixes
- Performance improvements
- Better error handling
- Documentation improvements

**Medium Priority:**
- New features
- UI/UX enhancements
- Additional file manager support

**Low Priority:**
- Code refactoring (without behavior change)
- Style improvements

### 🚀 Feature Ideas (Help Wanted)

**Easy:**
- [ ] Add "Open Backup Folder" after successful backup
- [ ] Remember last "Backup As" location
- [ ] Add backup counter in settings
- [ ] Sound notification option

**Medium:**
- [ ] Restore from backup option
- [ ] Compare file with backup (diff)
- [ ] Auto-cleanup old backups (keep last N)
- [ ] Progress bar for large backups
- [ ] Backup history view

**Hard:**
- [ ] Scheduled backups
- [ ] Incremental backups
- [ ] Cloud storage integration
- [ ] Port to other file managers (Nemo, Caja)
- [ ] Compression level options

### 🔍 Code Review Process

**What we look for:**
- Code quality and clarity
- Proper error handling
- User experience
- Documentation
- Test coverage
- Performance impact

**Review timeline:**
- Initial review: Within 1 week
- Follow-up: Within 3 days
- Merge: When approved by maintainer

### 📋 Coding Standards

**Python:**
```python
# Use type hints (Python 3.8+)
def create_backup(source: Path, dest: Path) -> tuple[bool, str]:
    pass

# Use pathlib for paths
from pathlib import Path
path = Path("/home/user/file.txt")

# Handle errors explicitly
try:
    shutil.copy2(source, dest)
except PermissionError:
    return False, "Permission denied"
except Exception as e:
    return False, str(e)

# Use descriptive names
backup_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# Not: ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
```

**Shell scripts:**
```bash
# Use set -e
set -e

# Check commands exist
if ! command -v nautilus &> /dev/null; then
    echo "Error: Nautilus not found"
    exit 1
fi

# Use descriptive variables
INSTALL_DIR="$HOME/.local/share/nautilus-python/extensions"
# Not: DIR="$HOME/.local/share/nautilus-python/extensions"
```

### 🐛 Debug Tips

**Enable Nautilus debug output:**
```bash
nautilus -q
NAUTILUS_EXTENSION_DEBUG=1 nautilus 2>&1 | grep -i backup
```

**Test extension loading:**
```bash
python3 << EOF
import sys
sys.path.insert(0, '$HOME/.local/share/nautilus-python/extensions')
import nautilus_backup
print("Extension loaded successfully!")
EOF
```

**Check logs:**
```bash
# System logs
journalctl -xe | grep -i nautilus

# Notification logs
journalctl -xe | grep -i notify
```

### 📞 Getting Help

**Questions?**
- Open a GitHub Discussion
- Comment on relevant issue
- Check existing documentation

**Need clarification?**
- Tag maintainers in issue
- Be specific about what's unclear
- Provide context

### 🎓 Resources

**Nautilus Python Extension:**
- [Nautilus Python Docs](https://projects.gnome.org/nautilus-python/)
- [PyGObject Docs](https://pygobject.readthedocs.io/)

**Python:**
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Python Docs](https://docs.python.org/3/)

**Git:**
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

### ✅ PR Checklist

Before submitting, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] Screenshots for UI changes (if applicable)

### 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

### 🙏 Thank You!

Every contribution helps make this extension better for everyone!

**Contributors will be:**
- Listed in README
- Credited in release notes
- Forever appreciated! 🎉

---

**Questions about contributing?** Open an issue with the `question` label!

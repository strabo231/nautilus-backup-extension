#!/bin/bash

# Nautilus Backup Extension Installer
# Installs right-click backup functionality to Nautilus file manager

set -e

VERSION="1.0.0"
EXTENSION_NAME="nautilus-backup.py"
INSTALL_DIR="$HOME/.local/share/nautilus-python/extensions"
CONFIG_DIR="$HOME/.config/nautilus-backup"
BACKUP_DIR="$HOME/Backups"

echo "============================================================"
echo "     Nautilus Backup Extension Installer v${VERSION}     "
echo "============================================================"
echo ""

# Check if running on supported system
if ! command -v nautilus &> /dev/null; then
    echo "[ERROR] Nautilus file manager not found"
    echo "        This extension requires Nautilus (GNOME Files)"
    exit 1
fi

echo "[OK] Nautilus found"

# Check for python-nautilus
echo ""
echo "[INFO] Checking dependencies..."

MISSING_DEPS=()

if ! python3 -c "import gi; gi.require_version('Nautilus', '4.0')" 2>/dev/null; then
    if ! python3 -c "import gi; gi.require_version('Nautilus', '3.0')" 2>/dev/null; then
        MISSING_DEPS+=("python3-nautilus")
    fi
fi

if [ "${#MISSING_DEPS[@]}" -ne 0 ]; then
    echo ""
    echo "[WARNING] Missing dependencies detected!"
    echo ""
    echo "The following packages need to be installed:"
    for dep in "${MISSING_DEPS[@]}"; do
        echo "  * $dep"
    done
    echo ""
    
    # Detect package manager
    if command -v apt &> /dev/null; then
        PKG_MANAGER="apt"
        INSTALL_CMD="sudo apt install -y python3-nautilus"
    elif command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
        INSTALL_CMD="sudo dnf install -y nautilus-python"
    elif command -v pacman &> /dev/null; then
        PKG_MANAGER="pacman"
        INSTALL_CMD="sudo pacman -S python-nautilus"
    else
        echo "[ERROR] Could not detect package manager"
        echo "        Please install python3-nautilus manually"
        exit 1
    fi
    
    echo "Would you like to install them now? (requires sudo)"
    read -p "Install dependencies? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "[INFO] Installing dependencies..."
        eval "$INSTALL_CMD"
        echo "[OK] Dependencies installed"
    else
        echo ""
        echo "Installation cancelled. Please install dependencies manually:"
        echo "  $INSTALL_CMD"
        exit 1
    fi
else
    echo "[OK] All dependencies satisfied"
fi

# Create directories
echo ""
echo "[INFO] Creating directories..."

mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$BACKUP_DIR"

echo "[OK] Directories created"

# Copy extension file
echo ""
echo "[INFO] Installing extension..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if extension file exists in current directory or script directory
if [ -f "$EXTENSION_NAME" ]; then
    cp "$EXTENSION_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$EXTENSION_NAME"
    echo "[OK] Extension installed to: $INSTALL_DIR"
elif [ -f "$SCRIPT_DIR/$EXTENSION_NAME" ]; then
    cp "$SCRIPT_DIR/$EXTENSION_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$EXTENSION_NAME"
    echo "[OK] Extension installed to: $INSTALL_DIR"
else
    echo "[ERROR] $EXTENSION_NAME not found"
    echo "        Looked in:"
    echo "          * Current directory: $(pwd)"
    echo "          * Script directory: $SCRIPT_DIR"
    echo "        Please run this script from the extension directory"
    exit 1
fi

# Create default config
echo ""
echo "[INFO] Creating configuration..."

echo "$BACKUP_DIR" > "$CONFIG_DIR/config.txt"

echo "[OK] Configuration created"

# Restart Nautilus
echo ""
echo "[INFO] Restarting Nautilus..."

# Kill nautilus gracefully
nautilus -q 2>/dev/null || true
sleep 1

# Restart nautilus
nohup nautilus > /dev/null 2>&1 &

echo "[OK] Nautilus restarted"

# Success message
echo ""
echo "============================================================"
echo "                 Installation Complete!                     "
echo "============================================================"
echo ""
echo "Nautilus Backup Extension is now installed!"
echo ""
echo "How to use:"
echo "  1. Right-click any file or folder in Nautilus"
echo "  2. Look for the 'Backup' menu"
echo "  3. Choose your backup option:"
echo "     * Quick Backup (Same Folder)"
echo "     * Backup As..."
echo "     * Backup to ~/Backups"
echo ""
echo "Your backups folder: $BACKUP_DIR"
echo ""
echo "Tips:"
echo "  * Quick Backup creates: filename_backup_2024-12-22_14-30-00.ext"
echo "  * Folders are backed up as .tar.gz archives"
echo "  * Desktop notifications show backup status"
echo ""
echo "Settings: Right-click -> Backup -> Backup Settings"
echo ""
echo "If you don't see the menu, try:"
echo "  1. Close all Nautilus windows"
echo "  2. Run: nautilus -q"
echo "  3. Open Nautilus again"
echo ""
echo "Enjoy hassle-free backups!"
echo ""

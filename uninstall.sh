#!/bin/bash

# Nautilus Backup Extension Uninstaller

set -e

EXTENSION_NAME="nautilus-backup.py"
INSTALL_DIR="$HOME/.local/share/nautilus-python/extensions"
CONFIG_DIR="$HOME/.config/nautilus-backup"

echo "╔════════════════════════════════════════════════════════╗"
echo "║      Nautilus Backup Extension Uninstaller           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

if [ ! -f "$INSTALL_DIR/$EXTENSION_NAME" ]; then
    echo "❌ Extension not found. Nothing to uninstall."
    exit 0
fi

echo "⚠️  This will remove the Nautilus Backup Extension"
echo "   Your backup files will NOT be deleted"
echo ""
read -p "Continue with uninstallation? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "🗑️  Removing extension..."

# Remove extension file
rm -f "$INSTALL_DIR/$EXTENSION_NAME"

echo "✓ Extension removed"

# Ask about config
echo ""
read -p "Remove configuration files? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$CONFIG_DIR"
    echo "✓ Configuration removed"
else
    echo "ℹ️  Configuration preserved at: $CONFIG_DIR"
fi

# Restart Nautilus
echo ""
echo "🔄 Restarting Nautilus..."

nautilus -q 2>/dev/null || true
sleep 1
nohup nautilus > /dev/null 2>&1 &

echo "✓ Nautilus restarted"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║          ✅ Uninstallation Complete!                  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "The Nautilus Backup Extension has been removed."
echo "Your backup files remain untouched in ~/Backups"
echo ""

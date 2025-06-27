#!/bin/bash
# dashtrash installer script

set -e

echo "🗑️ Installing dashtrash..."

# Check if Python 3.8+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ is required. You have Python $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install via pip
echo "📦 Installing dashtrash via pip..."
python3 -m pip install --user dashtrash

# Verify installation
if command -v dashtrash &> /dev/null; then
    echo "✅ dashtrash installed successfully!"
    echo ""
    echo "🚀 Quick start:"
    echo "   dashtrash                    # Run with default config"
    echo "   dashtrash --create-config    # Create custom config"
    echo "   dashtrash --help             # Show all options"
    echo ""
    echo "📖 Documentation: https://github.com/turancannb02/dashtrash"
else
    echo "⚠️  dashtrash was installed but not found in PATH."
    echo "You may need to add ~/.local/bin to your PATH:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Or run with: python3 -m dashtrash"
fi

echo ""
echo "Real-time dashboards. Questionable aesthetics. 🗑️✨" 
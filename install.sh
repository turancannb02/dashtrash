#!/bin/bash
# dashtrash installation script
# Usage: curl -sSL https://raw.githubusercontent.com/turancannb02/dashtrash/main/install.sh | bash

set -e

echo "🗑️  Installing dashtrash - Terminal Dashboard"
echo "============================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.9+ and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" 2>/dev/null; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. You have $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Install dashtrash
echo "📦 Installing dashtrash..."

# Try pip3 first, then pip
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "❌ pip is not available. Please install pip and try again."
    exit 1
fi

# Install from source (since not on PyPI yet)
echo "📥 Cloning dashtrash repository..."
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

if command -v git &> /dev/null; then
    git clone https://github.com/turancannb02/dashtrash.git
    cd dashtrash
    echo "🔧 Installing dashtrash..."
    $PIP_CMD install -e . --user
else
    echo "❌ git is required but not installed."
    echo "Please install git or use manual installation:"
    echo "  git clone https://github.com/turancannb02/dashtrash.git"
    echo "  cd dashtrash"
    echo "  pip3 install -e ."
    exit 1
fi

# Clean up
cd ~
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 dashtrash installed successfully!"
echo ""
echo "📋 Quick Start:"
echo "  dashtrash                    # Run with default config"
echo "  dashtrash --help             # Show help"
echo "  dashtrash --create-config    # Create default config file"
echo ""
echo "🔧 Configuration:"
echo "  Edit dashboard.yml to customize panels and settings"
echo ""
echo "📚 Documentation:"
echo "  https://github.com/turancannb02/dashtrash"
echo ""
echo "🗑️✨ Real-time dashboards. Questionable aesthetics." 
#!/bin/bash
# dashtrash installation script using pipx
# Usage: curl -sSL https://raw.githubusercontent.com/turancannb02/dashtrash/main/install-pipx.sh | bash

set -e

echo "🗑️  Installing dashtrash via pipx - Terminal Dashboard"
echo "====================================================="

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

# Install pipx if not available
if ! command -v pipx &> /dev/null; then
    echo "📦 Installing pipx..."
    if command -v brew &> /dev/null; then
        brew install pipx
        pipx ensurepath
    elif command -v pip3 &> /dev/null; then
        pip3 install --user pipx
        python3 -m pipx ensurepath
    else
        echo "❌ Cannot install pipx. Please install it manually:"
        echo "  brew install pipx  # On macOS"
        echo "  pip3 install --user pipx  # On other systems"
        exit 1
    fi
    
    # Reload PATH
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "✅ pipx is available"

# Install dashtrash using pipx
echo "📦 Installing dashtrash..."
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

if command -v git &> /dev/null; then
    git clone https://github.com/turancannb02/dashtrash.git
    cd dashtrash
    echo "🔧 Installing dashtrash via pipx..."
    pipx install .
    echo "✅ dashtrash installed successfully!"
else
    echo "❌ git is required but not installed."
    echo "Please install git and try again."
    exit 1
fi

# Clean up
cd ~
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 dashtrash is ready to use!"
echo ""
echo "⚡ To use dashtrash in your current shell, run:"
echo "  source ~/.zshrc    # if using zsh"
echo "  source ~/.bashrc   # if using bash" 
echo "  # OR simply open a new terminal window"
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
echo "💡 pipx benefits:"
echo "  - Isolated environment (no conflicts)"
echo "  - Automatic PATH management"
echo "  - Easy updates: pipx upgrade dashtrash"
echo "  - Easy removal: pipx uninstall dashtrash"
echo ""
echo "🗑️✨ Real-time dashboards. Questionable aesthetics." 
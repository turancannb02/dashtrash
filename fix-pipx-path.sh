#!/bin/bash
# Quick fix for pipx PATH issue

echo "🔧 Fixing pipx PATH for dashtrash..."

# Ensure pipx path is added
pipx ensurepath

# Add to current shell
export PATH="$HOME/.local/bin:$PATH"

# Test if dashtrash is now available
if command -v dashtrash &> /dev/null; then
    echo "✅ dashtrash is now available!"
    echo "📋 You can now run:"
    echo "  dashtrash --help"
    echo "  dashtrash --create-config"
    echo "  dashtrash"
else
    echo "❌ dashtrash still not found. Checking pipx status..."
    pipx list
    echo ""
    echo "💡 Try running:"
    echo "  source ~/.zshrc"
    echo "  # or open a new terminal window"
fi 
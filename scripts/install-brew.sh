#!/bin/bash
# Script to install dashtrash via Homebrew

set -e

echo "🍺 Installing dashtrash via Homebrew..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed."
    echo "Install Homebrew first: https://brew.sh"
    exit 1
fi

echo "✅ Homebrew detected"

# Add tap (replace with your actual tap)
echo "📦 Adding dashtrash tap..."
brew tap turancannb02/dashtrash

# Install dashtrash
echo "📦 Installing dashtrash..."
brew install dashtrash

# Verify installation
if command -v dashtrash &> /dev/null; then
    echo "✅ dashtrash installed successfully!"
    echo ""
    echo "🚀 Quick start:"
    echo "   dashtrash                    # Run with default config"
    echo "   dashtrash --create-config    # Create custom config"
    echo "   dashtrash --help             # Show all options"
    echo ""
    dashtrash --version
else
    echo "❌ Installation failed"
    exit 1
fi

echo ""
echo "Real-time dashboards. Questionable aesthetics. 🗑️✨" 
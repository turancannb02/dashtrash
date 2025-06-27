#!/bin/bash
# Script to set up Homebrew tap for dashtrash

set -e

echo "🍺 Setting up Homebrew tap for dashtrash..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Please run this script from the dashtrash project root"
    exit 1
fi

# Create homebrew-dashtrash repository structure
echo "📁 Creating tap structure..."
TAP_DIR="../homebrew-dashtrash"

if [ -d "$TAP_DIR" ]; then
    echo "⚠️  Tap directory already exists. Removing..."
    rm -rf "$TAP_DIR"
fi

mkdir -p "$TAP_DIR/Formula"

# Copy the formula
echo "📋 Copying formula..."
cp Formula/dashtrash.rb "$TAP_DIR/Formula/"

# Create README for the tap
cat > "$TAP_DIR/README.md" << 'EOF'
# Homebrew Tap for dashtrash

This is the official Homebrew tap for [dashtrash](https://github.com/turancannb02/dashtrash).

## Installation

```bash
brew tap turancannb02/dashtrash
brew install dashtrash
```

## Usage

```bash
dashtrash --help
```

For more information, visit: https://github.com/turancannb02/dashtrash
EOF

# Initialize git repository
echo "🔧 Setting up git repository..."
cd "$TAP_DIR"
git init
git add .
git commit -m "Initial commit: Add dashtrash formula"

echo "✅ Homebrew tap structure created in $TAP_DIR"
echo ""
echo "Next steps:"
echo "1. Create a GitHub repository named 'homebrew-dashtrash'"
echo "2. Push this tap to GitHub:"
echo "   cd $TAP_DIR"
echo "   git remote add origin https://github.com/turancannb02/homebrew-dashtrash.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo "3. Update the SHA256 in Formula/dashtrash.rb when you publish to PyPI"
echo ""
echo "Then users can install with: brew tap turancannb02/dashtrash && brew install dashtrash" 
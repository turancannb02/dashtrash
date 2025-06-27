#!/bin/bash
# Release script for dashtrash

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 0.2.0"
    exit 1
fi

VERSION=$1
echo "🚀 Preparing release v$VERSION"

# Check if we're on main branch
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
    echo "❌ Must be on main branch for release. Currently on: $BRANCH"
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Working directory is not clean. Please commit all changes."
    exit 1
fi

# Update version in pyproject.toml
echo "📝 Updating version in pyproject.toml..."
sed -i.bak "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml
rm pyproject.toml.bak

# Update version in main.py
echo "📝 Updating version in main.py..."
sed -i.bak "s/version='dashtrash .*/version='dashtrash $VERSION'/" dashtrash/main.py
rm dashtrash/main.py.bak

# Update version in main.py (root)
echo "📝 Updating version in root main.py..."
sed -i.bak "s/version='dashtrash .*/version='dashtrash $VERSION'/" main.py
rm main.py.bak

# Build package
echo "📦 Building package..."
python3 -m build

# Create git tag
echo "🏷️  Creating git tag..."
git add pyproject.toml dashtrash/main.py main.py
git commit -m "Bump version to $VERSION"
git tag -a "v$VERSION" -m "Release version $VERSION"

echo "✅ Release v$VERSION prepared!"
echo ""
echo "Next steps:"
echo "1. Push changes: git push origin main --tags"
echo "2. Create GitHub release from tag v$VERSION"
echo "3. GitHub Actions will automatically publish to PyPI"
echo "4. Update Homebrew formula with new SHA256"
echo ""
echo "To calculate SHA256 for Homebrew:"
echo "  shasum -a 256 dist/dashtrash-$VERSION.tar.gz" 
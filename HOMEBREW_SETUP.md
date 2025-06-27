# 🍺 Homebrew Setup Guide for dashtrash

This guide will help you set up `brew install dashtrash` for your users.

## 📋 **Prerequisites**

1. **GitHub account** with access to create repositories
2. **Git** installed and configured
3. **dashtrash repository** with a tagged release

## 🚀 **Step-by-Step Setup**

### **1. Create GitHub Repository for Homebrew Tap**

1. Go to [GitHub](https://github.com/new)
2. Create a new repository named: `homebrew-dashtrash`
3. Make it **public**
4. Don't initialize with README (we'll push our own)

### **2. Push the Tap to GitHub**

The tap structure has already been created in `../homebrew-dashtrash`. Now push it:

```bash
cd ../homebrew-dashtrash

# Add GitHub remote
git remote add origin https://github.com/turancannb02/homebrew-dashtrash.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### **3. Create a GitHub Release**

You need to create a tagged release for Homebrew to download:

```bash
cd ../dashtrash

# Create and push a tag
git tag -a v0.1.0 -m "Release v0.1.0: Real-time terminal dashboard"
git push origin v0.1.0
```

Then on GitHub:
1. Go to `https://github.com/turancannb02/dashtrash/releases`
2. Click "Create a new release"
3. Choose tag: `v0.1.0`
4. Title: `dashtrash v0.1.0`
5. Description: Your release notes
6. Click "Publish release"

### **4. Update SHA256 Hash (if needed)**

If the release SHA256 doesn't match, update it:

```bash
# Download the release tarball
curl -L https://github.com/turancannb02/dashtrash/archive/refs/tags/v0.1.0.tar.gz -o v0.1.0.tar.gz

# Get SHA256
shasum -a 256 v0.1.0.tar.gz

# Update Formula/dashtrash.rb with the new hash
# Then commit and push to homebrew-dashtrash
```

## ✅ **Testing the Installation**

Once everything is set up, test it:

```bash
# Add the tap
brew tap turancannb02/dashtrash

# Install dashtrash
brew install dashtrash

# Test it works
dashtrash --help
```

## 🎯 **User Instructions**

After setup, users can install dashtrash with:

```bash
# Add the tap and install
brew tap turancannb02/dashtrash
brew install dashtrash

# Or in one command
brew install turancannb02/dashtrash/dashtrash
```

## 🔄 **Updating the Formula**

When you release new versions:

1. **Update dashtrash version** in `pyproject.toml`
2. **Create new GitHub release** with new tag
3. **Update Homebrew formula**:
   ```bash
   cd ../homebrew-dashtrash
   
   # Update Formula/dashtrash.rb with:
   # - New version number in URL
   # - New SHA256 hash
   
   git add Formula/dashtrash.rb
   git commit -m "Update dashtrash to v0.2.0"
   git push
   ```

## 📚 **Homebrew Formula Explanation**

```ruby
class Dashtrash < Formula
  include Language::Python::Virtualenv  # Python app support

  desc "Terminal-based dashboard for real-time monitoring"
  homepage "https://github.com/turancannb02/dashtrash"
  url "https://github.com/turancannb02/dashtrash/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "YOUR_RELEASE_SHA256_HERE"
  license "MIT"

  depends_on "python@3.11"  # Requires Python 3.11+

  # Python dependencies as resources
  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-14.0.0.tar.gz"
    sha256 "RICH_SHA256_HERE"
  end
  # ... other resources

  def install
    virtualenv_install_with_resources  # Install in isolated environment
  end

  test do
    system bin/"dashtrash", "--help"    # Test the installation
  end
end
```

## 🎉 **Benefits of Homebrew Installation**

- ✅ **Easy installation**: `brew install dashtrash`
- ✅ **Automatic updates**: `brew upgrade dashtrash`
- ✅ **Dependency management**: Homebrew handles Python and dependencies
- ✅ **Clean removal**: `brew uninstall dashtrash`
- ✅ **System integration**: Automatically adds to PATH

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **SHA256 mismatch**: Download the release tarball and recalculate
2. **Python version**: Ensure you're using Python 3.11+ in the formula
3. **Resource SHA256s**: Use `brew fetch --retry` to get correct hashes
4. **Formula syntax**: Test with `brew install --build-from-source`

### **Testing Commands:**

```bash
# Test formula syntax
brew audit --strict Formula/dashtrash.rb

# Test installation from source
brew install --build-from-source dashtrash

# Test with verbose output
brew install --verbose dashtrash
```

## 📝 **Next Steps**

1. ✅ Create `homebrew-dashtrash` repository on GitHub
2. ✅ Push the tap structure
3. ✅ Create v0.1.0 release on GitHub
4. ✅ Test the installation
5. ✅ Update documentation with Homebrew instructions

After completing these steps, users will be able to install dashtrash with:

```bash
brew install turancannb02/dashtrash/dashtrash
```

🍺✨ **Happy brewing!** 
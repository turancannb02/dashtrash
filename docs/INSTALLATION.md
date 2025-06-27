# 📦 Installation Guide

This guide covers all the ways to install **dashtrash** on different systems.

## 🚀 Quick Install (Recommended)

### pip (All platforms)
```bash
pip install dashtrash
```

### One-liner (Unix/macOS)
```bash
curl -sSL https://raw.githubusercontent.com/turancannb02/dashtrash/main/install.sh | bash
```

### Homebrew (macOS/Linux)
```bash
brew tap yourusername/dashtrash
brew install dashtrash
```

---

## 📋 Detailed Installation Options

### 1. PyPI (Python Package Index)

**Global installation:**
```bash
pip install dashtrash
```

**User-only installation:**
```bash
pip install --user dashtrash
```

**Specific version:**
```bash
pip install dashtrash==0.1.0
```

**With development dependencies:**
```bash
pip install dashtrash[dev]
```

### 2. From Source

**Latest stable:**
```bash
git clone https://github.com/turancannb02/dashtrash.git
cd dashtrash
pip install .
```

**Development mode:**
```bash
git clone https://github.com/turancannb02/dashtrash.git
cd dashtrash
pip install -e .
```

**From specific tag:**
```bash
git clone --branch v0.1.0 https://github.com/turancannb02/dashtrash.git
cd dashtrash
pip install .
```

### 3. Package Managers

#### Homebrew (macOS/Linux)
```bash
# Add tap
brew tap turancannb02/dashtrash

# Install
brew install dashtrash

# Update
brew upgrade dashtrash
```

#### APT (Ubuntu/Debian) - Coming Soon
```bash
# Add repository
curl -fsSL https://repo.dashtrash.dev/gpg | sudo gpg --dearmor -o /usr/share/keyrings/dashtrash.gpg
echo "deb [signed-by=/usr/share/keyrings/dashtrash.gpg] https://repo.dashtrash.dev/apt stable main" | sudo tee /etc/apt/sources.list.d/dashtrash.list

# Install
sudo apt update
sudo apt install dashtrash
```

#### Snap (Universal Linux) - Coming Soon
```bash
sudo snap install dashtrash
```

#### Arch User Repository (AUR) - Coming Soon
```bash
yay -S dashtrash
# or
paru -S dashtrash
```

### 4. Container Images

#### Docker
```bash
# Run directly
docker run --rm -it ghcr.io/turancannb02/dashtrash:latest

# With config volume
docker run --rm -it -v $(pwd)/dashboard.yml:/app/dashboard.yml ghcr.io/turancannb02/dashtrash:latest
```

#### Podman
```bash
podman run --rm -it ghcr.io/turancannb02/dashtrash:latest
```

---

## ✅ Verification

After installation, verify dashtrash is working:

```bash
# Check version
dashtrash --version

# Show help
dashtrash --help

# Create config
dashtrash --create-config

# Validate config
dashtrash --validate

# Run dashboard
dashtrash
```

---

## 🔧 Requirements

- **Python**: 3.8 or higher
- **OS**: Linux, macOS, Windows
- **Terminal**: Any terminal with color support

### Python Dependencies
- `rich>=13.0.0` - Terminal UI framework
- `psutil>=5.9.0` - System metrics
- `pyfiglet>=0.8.0` - ASCII art
- `PyYAML>=6.0` - Configuration parsing
- `textual>=0.41.0` - Advanced TUI components

---

## 🐛 Troubleshooting

### Command not found after pip install
```bash
# Check if ~/.local/bin is in PATH
echo $PATH | grep -q "$HOME/.local/bin" && echo "✅ Found" || echo "❌ Missing"

# Add to PATH (bash/zsh)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or ~/.zshrc

# Alternative: run with python module
python -m dashtrash
```

### Permission denied on macOS/Linux
```bash
# Install for user only
pip install --user dashtrash

# Or use virtual environment
python -m venv dashtrash-env
source dashtrash-env/bin/activate
pip install dashtrash
```

### Python version too old
```bash
# Check version
python --version

# Install newer Python (macOS)
brew install python@3.11

# Install newer Python (Ubuntu)
sudo apt update
sudo apt install python3.11 python3.11-pip
```

### Windows PATH issues
```powershell
# Check PATH
echo $env:PATH

# Add to PATH permanently
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$env:LOCALAPPDATA\Programs\Python\Python311\Scripts", "User")
```

---

## 🔄 Updates

### pip
```bash
pip install --upgrade dashtrash
```

### Homebrew
```bash
brew upgrade dashtrash
```

### Docker
```bash
docker pull ghcr.io/turancannb02/dashtrash:latest
```

---

## 🗑️ Uninstallation

### pip
```bash
pip uninstall dashtrash
```

### Homebrew
```bash
brew uninstall dashtrash
brew untap turancannb02/dashtrash
```

### Snap
```bash
sudo snap remove dashtrash
```

---

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/turancannb02/dashtrash/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/turancannb02/dashtrash/discussions)
- 📖 **Documentation**: [README](../README.md) 
# 🗑️ dashtrash

<div align="center">

![dashtrash-banner](https://img.shields.io/badge/dashtrash-Terminal%20Dashboard-blue?style=for-the-badge&logo=terminal&logoColor=white)

[![PyPI version](https://img.shields.io/pypi/v/dashtrash?style=flat-square&color=blue)](https://pypi.org/project/dashtrash/)
[![Python versions](https://img.shields.io/pypi/pyversions/dashtrash?style=flat-square)](https://pypi.org/project/dashtrash/)
[![License](https://img.shields.io/github/license/turancannb02/dashtrash?style=flat-square)](https://github.com/turancannb02/dashtrash/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/turancannb02/dashtrash?style=flat-square)](https://github.com/turancannb02/dashtrash/stargazers)
[![Downloads](https://img.shields.io/pypi/dm/dashtrash?style=flat-square&color=green)](https://pypi.org/project/dashtrash/)

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/turancannb02/dashtrash/test.yml?style=flat-square&label=tests)](https://github.com/turancannb02/dashtrash/actions)
[![Homebrew](https://img.shields.io/badge/Homebrew-Available-orange?style=flat-square&logo=homebrew)](https://github.com/turancannb02/dashtrash)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)](https://github.com/turancannb02/dashtrash/pkgs/container/dashtrash)

</div>

---

<div align="center">

## **Real-time dashboards. Questionable aesthetics.** 🗑️✨

*A terminal-based dashboard UI built entirely in the command line for real-time monitoring of system metrics, logs, and custom data sources — without relying on external SaaS dashboards or heavy GUI tools.*

</div>

## ✨ Features

- 📊 **Real-time system monitoring** (CPU, Memory, Disk, Network)
- 📁 **Live log viewer** with filters and highlighting
- 🔌 **Plugin support** for Docker, APIs, databases, etc.
- ⚙️ **YAML-based configuration** for easy customization
- 🖼️ **ASCII banner** and terminal art on startup
- 🧩 **Modular and extensible** - easy to add custom panels

## 🚀 Quick Start

### Option 1: Install via pip (Recommended)

```bash
# Install globally
pip install dashtrash

# Or install for current user only
pip install --user dashtrash

# Run it!
dashtrash
```

### Option 2: One-liner install script

```bash
curl -sSL https://raw.githubusercontent.com/turancannb02/dashtrash/main/install.sh | bash
```

### Option 3: Install via Homebrew (macOS/Linux)

```bash
brew tap turancannb02/dashtrash
brew install dashtrash
```

### Option 4: Development setup

```bash
git clone https://github.com/turancannb02/dashtrash.git
cd dashtrash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run it!
dashtrash
```

### Quick Commands

```bash
# Run with default configuration
dashtrash

# Create and customize your config
dashtrash --create-config
dashtrash --validate

# Run with custom config
dashtrash -c my-dashboard.yml

# Show help
dashtrash --help
```

### 3. Exit the Dashboard

Press `Ctrl+C` to exit the dashboard gracefully.

## ⚙️ Configuration

dashtrash uses a simple YAML configuration file (`dashboard.yml`):

```yaml
panels:
  - type: system
    position: top
    refresh_interval: 2
  - type: logs
    file: ~/.zsh_history
    filters: ["python", "git", "cd"]
    max_lines: 20
    position: bottom

banner:
  text: "DashTrash"
  font: "ANSI Shadow"
  tagline: "Real-time dashboards. Questionable aesthetics."

refresh_rate: 1.0
```

### Panel Types

#### System Panel
Monitors CPU, memory, disk, and network usage:
```yaml
- type: system
  refresh_interval: 2
  position: top
```

#### Logs Panel
Live log monitoring with filtering:
```yaml
- type: logs
  file: /var/log/syslog
  filters: ["ERROR", "WARNING", "INFO"]
  max_lines: 20
  position: bottom
```

#### Plugin Panel
Custom plugins for extended functionality:
```yaml
- type: plugin
  plugin_name: demo
  refresh_interval: 5
  position: right
```

## 🔌 Plugin Development

Create custom plugins by adding Python files to `dashboard/plugins/`:

```python
# dashboard/plugins/my_plugin.py

def fetch():
    """Fetch data for your plugin"""
    return {
        "status": "online",
        "users": 42,
        "uptime": "5 days"
    }

def render(data):
    """Render the data"""
    from rich.text import Text
    content = Text()
    content.append(f"Status: {data['status']}\n", style="green")
    content.append(f"Users: {data['users']}\n", style="blue")
    content.append(f"Uptime: {data['uptime']}", style="yellow")
    return content

def initialize(config):
    """Optional: Initialize with config"""
    return True

def cleanup():
    """Optional: Cleanup resources"""
    pass
```

Then add it to your `dashboard.yml`:
```yaml
- type: plugin
  plugin_name: my_plugin
  refresh_interval: 10
```

## 📁 Project Structure

```
dashtrash/
├── .github/workflows/     # GitHub Actions (CI/CD)
│   ├── publish.yml        # PyPI publishing
│   └── test.yml          # Multi-platform testing
├── dashtrash/            # Main package
│   ├── __init__.py       # Package initialization
│   ├── banner.py         # ASCII art and startup display
│   ├── config.py         # YAML configuration handling
│   ├── core.py           # Main dashboard engine
│   ├── main.py           # CLI entry point
│   ├── panels/
│   │   ├── __init__.py   # Panels package
│   │   ├── system.py     # System metrics panel
│   │   └── logs.py       # Log viewer panel
│   └── plugins/
│       ├── __init__.py   # Plugin management
│       └── demo.py       # Example plugin
├── docs/                 # Documentation
│   └── INSTALLATION.md   # Detailed install guide
├── scripts/              # Utility scripts
│   ├── install-brew.sh   # Homebrew installer
│   └── release.sh        # Release automation
├── snap/                 # Snap package config
│   └── snapcraft.yaml    # Snap build configuration
├── dashboard.yml         # Default configuration
├── main.py              # Development entry point
├── pyproject.toml       # Python package configuration
├── requirements.txt     # Dependencies
├── install.sh           # One-liner installer
├── Dockerfile           # Container image
├── Brewfile            # Homebrew formula
├── LICENSE             # MIT license
└── README.md           # This file
```

## 🛠️ CLI Commands

```bash
# Show help
dashtrash --help

# Create default configuration
dashtrash --create-config

# Validate configuration
dashtrash --validate

# Run with custom config
dashtrash -c custom.yml

# Show version
dashtrash --version
```

## 🎨 Customization

### ASCII Banner
Customize the startup banner in `dashboard.yml`:
```yaml
banner:
  text: "MyDash"
  font: "ansi_shadow"  # or "standard", "big", etc.
  tagline: "My custom dashboard"
```

### Panel Positioning
Control where panels appear:
- `top` - Upper area
- `bottom` - Lower area
- `left` - Left side (multi-panel layouts)
- `right` - Right side (multi-panel layouts)

### Colors and Styling
Panels automatically color-code based on status:
- 🟢 Green: Normal/Good (< 50% usage)
- 🟡 Yellow: Warning (50-80% usage)
- 🔴 Red: Critical (> 80% usage)

## 🧭 Why dashtrash?

Because not every monitoring tool should:
- ❌ Require a web server or database
- ❌ Send data to the cloud
- ❌ Make you open 4 different terminal tabs
- ❌ Cost money for basic monitoring

dashtrash gives you:
- ✅ **Terminal-first design** - Stay in the CLI
- ✅ **Zero dependencies** beyond Python packages
- ✅ **Highly configurable** with simple YAML
- ✅ **Modular & pluggable** - Extend easily
- ✅ **No telemetry, no SaaS, no bloat**

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **⭐ Star the repository** if you find it useful
2. **🐛 Report bugs** via [GitHub Issues](https://github.com/turancannb02/dashtrash/issues)
3. **💡 Suggest features** via [GitHub Discussions](https://github.com/turancannb02/dashtrash/discussions)
4. **🔧 Submit improvements**:
   ```bash
   # Fork the repository
   git clone https://github.com/turancannb02/dashtrash.git
   cd dashtrash
   
   # Create feature branch
   git checkout -b feature/amazing-feature
   
   # Make changes and commit
   git commit -m 'Add amazing feature'
   
   # Push and create Pull Request
   git push origin feature/amazing-feature
   ```

<div align="center">

### 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/turancannb02/dashtrash?style=social)
![GitHub forks](https://img.shields.io/github/forks/turancannb02/dashtrash?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/turancannb02/dashtrash?style=social)

[![GitHub issues](https://img.shields.io/github/issues/turancannb02/dashtrash?style=flat-square)](https://github.com/turancannb02/dashtrash/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/turancannb02/dashtrash?style=flat-square)](https://github.com/turancannb02/dashtrash/pulls)
[![GitHub contributors](https://img.shields.io/github/contributors/turancannb02/dashtrash?style=flat-square)](https://github.com/turancannb02/dashtrash/graphs/contributors)

</div>

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🌟 Show Your Support

If dashtrash helps you monitor your systems better, consider:

[![Star this repository](https://img.shields.io/badge/⭐-Star%20this%20repository-yellow?style=for-the-badge)](https://github.com/turancannb02/dashtrash/stargazers)
[![Follow @turancannb02](https://img.shields.io/badge/Follow-%40turancannb02-blue?style=for-the-badge&logo=github)](https://github.com/turancannb02)

**Real-time dashboards. Questionable aesthetics.** 🗑️✨

*Made with ❤️ for the terminal enthusiasts*

</div> 
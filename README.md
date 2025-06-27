# 🗑️ dashtrash

### *Real-time dashboards. Questionable aesthetics.*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/turancannb02/dashtrash?style=social)](https://github.com/turancannb02/dashtrash/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/turancannb02/dashtrash?style=social)](https://github.com/turancannb02/dashtrash/network)

**A beautiful terminal-based dashboard for real-time system monitoring**

[🚀 Quick Start](#-quick-start) • [📸 Screenshots](#-screenshots) • [✨ Features](#-features) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

---

## 📸 Screenshots

<div align="center">
  <img src="Screenshot 2025-06-27 at 13.21.55.png" alt="dashtrash Terminal Dashboard" width="100%">
  <p><em>Real-time system monitoring with beautiful ASCII charts and color-coded metrics</em></p>
</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📊 **Real-time Monitoring**
- **CPU Usage** with frequency display
- **Memory Usage** with detailed breakdown  
- **Disk Usage** with free space tracking
- **Network Activity** with speed indicators
- **System Uptime** and load averages

</td>
<td width="50%">

### 🎨 **Beautiful Visualization**
- **ASCII Charts** with historical data
- **Progress Bars** with color coding
- **Smart Log Filtering** with syntax highlighting
- **Responsive Layout** that adapts to terminal size
- **Professional UI** with headers and status info

</td>
</tr>
</table>

### 🔧 **Technical Features**
- ⚡ **High Performance** - Minimal resource usage
- 🔌 **Plugin System** - Extensible architecture for custom panels
- 📝 **YAML Configuration** - Easy customization
- 🖥️ **Cross-platform** - Works on macOS, Linux (Windows coming soon)
- 🎯 **Zero Dependencies** - No external services required

---

## 🚀 Quick Start

### Option 1: One-liner Install (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/turancannb02/dashtrash/main/install.sh | bash
```

### Option 2: Install from Source

```bash
git clone https://github.com/turancannb02/dashtrash.git
cd dashtrash
pip install -e .
```

### Option 3: Install via pip (Coming Soon)

```bash
pip install dashtrash
```

### 🎯 **Run dashtrash**

```bash
# Start with default configuration
dashtrash

# Create custom configuration
dashtrash --create-config

# Validate configuration
dashtrash --validate

# Show help
dashtrash --help
```

---

## 📖 Configuration

dashtrash uses a simple YAML configuration file:

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

### 🎛️ **Available Panels**
- **`system`** - CPU, Memory, Disk, Network monitoring
- **`logs`** - Real-time log file viewer with filtering
- **`plugin`** - Custom plugin support

---

## 🔌 Plugin Development

Create custom panels with the plugin system:

```python
# plugins/my_custom_panel.py
def fetch():
    return {"status": "healthy", "uptime": "2d 14h"}

def render(data):
    return f"Service Status: {data['status']} | Uptime: {data['uptime']}"
```

Add to your configuration:
```yaml
panels:
  - type: plugin
    plugin_name: my_custom_panel
    refresh_interval: 5
```

---

## 🛠️ Requirements

- **Python 3.9+**
- **Terminal with color support**
- **Unix-like system** (macOS, Linux)

### Dependencies
- `rich` - Terminal formatting and colors
- `psutil` - System metrics collection
- `pyfiglet` - ASCII art generation
- `PyYAML` - Configuration parsing
- `textual` - Terminal UI framework

---

## 📊 System Metrics

| Metric | Description | Visualization |
|--------|-------------|---------------|
| **CPU** | Usage percentage, frequency, core count | Progress bar + mini-chart |
| **Memory** | Used/total RAM, percentage | Progress bar + mini-chart |
| **Disk** | Used/free space, percentage | Progress bar + mini-chart |
| **Network** | Upload/download speeds, total transfer | Activity indicator + speeds |

---

## 🎨 Color Coding

dashtrash uses intelligent color coding for better readability:

- 🟢 **Green** (0-50%) - Normal usage
- 🟡 **Yellow** (50-80%) - Moderate usage  
- 🔴 **Red** (80-100%) - High usage
- 🔵 **Blue** - Information messages
- 🟣 **Purple** - Python-related logs
- 🟦 **Cyan** - Git-related logs

---

## 🚀 Roadmap

- [ ] **Windows Support** - Full compatibility with Windows terminals
- [ ] **Docker Plugin** - Container monitoring and stats
- [ ] **Database Plugin** - MySQL, PostgreSQL, Redis monitoring
- [ ] **API Plugin** - REST API health checks
- [ ] **Kubernetes Plugin** - Pod and cluster monitoring
- [ ] **Custom Themes** - User-defined color schemes
- [ ] **Export Data** - Save metrics to CSV/JSON
- [ ] **Alert System** - Notifications for threshold breaches

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 🐛 **Bug Reports**
Found a bug? [Open an issue](https://github.com/turancannb02/dashtrash/issues) with:
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Screenshots if applicable

### 💡 **Feature Requests**
Have an idea? [Start a discussion](https://github.com/turancannb02/dashtrash/discussions) or open an issue!

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Rich](https://github.com/Textualize/rich)** - For beautiful terminal formatting
- **[psutil](https://github.com/giampaolo/psutil)** - For cross-platform system metrics
- **[Textual](https://github.com/Textualize/textual)** - For terminal UI framework
- **Community** - For feedback and contributions

---

<div align="center">

### 🌟 **Star this repo if you find it useful!**

[![GitHub stars](https://img.shields.io/github/stars/turancannb02/dashtrash?style=social)](https://github.com/turancannb02/dashtrash/stargazers)

**Made with ❤️ for the terminal enthusiasts**

[🏠 Homepage](https://github.com/turancannb02/dashtrash) • [📚 Documentation](https://github.com/turancannb02/dashtrash#readme) • [🐛 Issues](https://github.com/turancannb02/dashtrash/issues) • [💬 Discussions](https://github.com/turancannb02/dashtrash/discussions)

---

*"Real-time dashboards. Questionable aesthetics."* 🗑️✨

</div> 
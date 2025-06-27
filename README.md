# dashtrash

> **Real-time terminal dashboard for system monitoring**

A lightweight, terminal-based dashboard tool for monitoring system metrics in real-time. Built for developers, sysadmins, and anyone who prefers to stay in the terminal.

## Features

- 📊 **Real-time system monitoring** - CPU, memory, disk, and network usage
- 🎨 **ASCII charts and progress bars** - Visual data representation in terminal
- ⚡ **Lightweight and fast** - No web server, no database, just pure terminal
- 🔧 **Configurable panels** - Customize layout and refresh rates
- 🌐 **Cross-platform** - Works on macOS, Linux, and other Unix systems

## Installation

### Homebrew (Recommended)

```bash
brew tap turancannb02/dashtrash
brew install dashtrash
```

### pipx

```bash
pipx install dashtrash
```

### Manual Installation

```bash
git clone https://github.com/turancannb02/dashtrash.git
cd dashtrash
pip install .
```

## Quick Start

```bash
# Create default configuration
dashtrash --create-config

# Run dashboard
dashtrash

# Run with custom config
dashtrash -c custom.yml
```

## Configuration

Edit `dashboard.yml` to customize your dashboard:

```yaml
panels:
  - type: system
    position: top
    refresh_interval: 2

banner:
  text: "DashTrash"
  font: "ANSI Shadow" 
  tagline: "Real-time dashboards. Questionable aesthetics."

refresh_rate: 1.0
```

### Available Panel Types

- **system** - CPU, memory, disk, and network monitoring
- **logs** - File monitoring with filtering
- **plugin** - Custom plugin support

## Screenshots

The dashboard displays real-time system metrics with ASCII charts:

```
╭─────────────────────────────────── 📊 System Metrics ───────────────────────────────────╮
│  Metric    Usage                    Chart                 Details                        │
│  🖥️  CPU    ███░░░░░░░░░░░░░░░░░     ▁▁▁▁▁█▂▆▁▁▁▁▂▁▂▅    8 cores @ 4056MHz              │
│           17.9%                                                                          │
│  🧠 RAM    ██████████████░░░░░░     ▁▁▁▁▁▅▁▂▁▁▁▃▃▁▁▅    7.1 GB / 16.0 GB               │
│           70.1%                                                                          │
│  💾 Disk   █░░░░░░░░░░░░░░░░░░░      ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁    30.3 GB free                   │
│           5.1%                                                                           │
│  🌐 Net    ↑ 1.2 KB/s ↓ 856 B/s    🟢 ██████████       Total: 2.7 GB                  │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

## Command Line Options

```
dashtrash [-h] [-c CONFIG] [--validate] [--create-config] [--version]

Options:
  -h, --help           Show help message
  -c, --config CONFIG  Path to configuration file (default: dashboard.yml)
  --validate           Validate configuration file and exit
  --create-config      Create a default configuration file
  --version            Show version number
```

## Development

### Requirements

- Python 3.9+
- Dependencies: rich, psutil, pyfiglet, PyYAML, textual

### Running from Source

```bash
git clone https://github.com/turancannb02/dashtrash.git
cd dashtrash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m dashtrash.main
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

*Real-time dashboards. Questionable aesthetics.* 
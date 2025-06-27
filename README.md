# 🗑️ dashtrash

### *Real-time dashboards. Questionable aesthetics.*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/turancannb02/dashtrash?style=social)](https://github.com/turancannb02/dashtrash/stargazers)
[![Homebrew](https://img.shields.io/badge/Homebrew-Available-orange.svg)](https://github.com/turancannb02/homebrew-dashtrash)

**A beautifully ugly terminal dashboard for people who live in the command line**

> "Because monitoring your system shouldn't require leaving your terminal or opening 47 browser tabs"

[🚀 Quick Start](#-quick-start) • [📸 Screenshots](#-screenshots) • [✨ Features](#-features) • [🤔 Why?](#-why) • [🤝 Contributing](#-contributing)

---

## 📸 Screenshots

```
╭───────────────────────────────── Welcome to ─────────────────────────────────╮
│                                                                              │
│               ____            _   _____              _                       │
│              |  _ \  __ _ ___| |_|_   _| __ __ _ ___| |__                    │
│              | | | |/ _` / __| '_ \| || '__/ _` / __| '_ \                   │
│              | |_| | (_| \__ \ | | | || | | (_| \__ \ | | |                  │
│              |____/ \__,_|___/_| |_|_||_|  \__,_|___/_| |_|                  │
│                                                                              │
│              > "Real-time dashboards. Questionable aesthetics."              │
╰──────────────────────────────────────────────────────────────────────────────╯

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

*Real-time system metrics with ASCII charts that actually look good in a terminal*

---

## 🤔 Why?

Because every other monitoring solution wants to:
- 📈 **Send your data to the cloud** (we keep it local, like your embarrassing browser history)
- 💰 **Charge you monthly** (we're free, like pizza at a tech meetup)
- 🌐 **Run in a browser** (we live in the terminal, where real work happens)
- 🎨 **Look "professional"** (we embrace the beautiful chaos of ASCII art)

**dashtrash** is for people who:
- ✨ Love the terminal more than their family
- 🎯 Want monitoring without the enterprise bloat
- 🎪 Appreciate questionable design choices
- 🚀 Believe ASCII art is the highest form of data visualization

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📊 **Real-time Monitoring**
- **CPU Usage** with frequency and core count
- **Memory Usage** with visual progress bars  
- **Disk Usage** with free space tracking
- **Network Activity** with upload/download speeds
- **System Load** and uptime display

</td>
<td width="50%">

### 🎨 **Beautiful ASCII Art**
- **Mini Charts** with historical data
- **Progress Bars** with color coding
- **ASCII Banner** on startup (obviously)
- **Responsive Layout** that doesn't break
- **Color-coded Everything** because why not

</td>
</tr>
</table>

### 🔧 **Technical Features**
- ⚡ **Lightweight** - Uses less RAM than your Slack app
- 🔌 **Extensible** - Plugin system for custom panels
- 📝 **Configurable** - YAML config because JSON is for quitters
- 🖥️ **Cross-platform** - macOS, Linux (Windows users, we see you)
- 🎯 **Zero Cloud** - Your data stays on your machine, like it should

---

## 🚀 Quick Start

### One-liner Install (For the Impatient)

```bash
# Homebrew (Recommended - because we're fancy now)
brew tap turancannb02/dashtrash
brew install dashtrash

# Or via pipx (For Python purists)
pipx install git+https://github.com/turancannb02/dashtrash.git

# Or the old-fashioned way
curl -sSL https://raw.githubusercontent.com/turancannb02/dashtrash/main/install.sh | bash
```

### Run It

```bash
# Create a config (or don't, we have defaults)
dashtrash --create-config

# Start the magic ✨
dashtrash

# Get help (we won't judge)
dashtrash --help
```

---

## 📖 Configuration

Create a `dashboard.yml` file or let us create one for you:

```yaml
panels:
  - type: system
    position: top
    refresh_interval: 2  # How often to update (seconds)

banner:
  text: "DashTrash"
  font: "ANSI Shadow"
  tagline: "Real-time dashboards. Questionable aesthetics."

refresh_rate: 1.0  # Global refresh rate
```

### 🎛️ Panel Types
- **`system`** - The main event (CPU, RAM, disk, network)
- **`logs`** - Tail files like it's 1999
- **`plugin`** - Roll your own (see Plugin Development below)

---

## 🔌 Plugin Development

Want to add your own panel? It's easier than explaining why you need another terminal dashboard:

```python
# plugins/my_awesome_panel.py
def fetch():
    return {
        "coffee_level": "dangerously_low",
        "bugs_fixed": 42,
        "bugs_created": 43
    }

def render(data):
    return f"☕ Coffee: {data['coffee_level']} | 🐛 Bug Ratio: {data['bugs_created']}/{data['bugs_fixed']}"
```

Add to your config:
```yaml
panels:
  - type: plugin
    plugin_name: my_awesome_panel
    refresh_interval: 30  # Check coffee level every 30 seconds
```

---

## 🛠️ Development

### Requirements
- Python 3.9+ (because we're not animals)
- A terminal that supports colors (most do nowadays)
- Patience for ASCII art loading times

### Dependencies
```bash
pip install rich psutil pyfiglet PyYAML textual
```

### Run from Source
```bash
git clone https://github.com/turancannb02/dashtrash.git
cd dashtrash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m dashtrash.main  # Watch the magic happen
```

---

## 🎨 Color Coding

We use a sophisticated color system (aka we picked colors that looked nice):

- 🟢 **Green** (0-50%) - Everything is fine, go back to coding
- 🟡 **Yellow** (50-80%) - Pay attention, but don't panic
- 🔴 **Red** (80-100%) - Time to close some Chrome tabs
- 🔵 **Blue** - Information (the color of calm)
- 🟣 **Purple** - Special events (very fancy)

---

## 🚀 Roadmap

Future features we'll probably implement when we get around to it:

- [ ] **Docker Integration** - Because everything runs in containers now
- [ ] **Custom Themes** - Make it even more questionable
- [ ] **Sound Effects** - ASCII beeps for alerts
- [ ] **AI Integration** - Just kidding, we're not that desperate
- [ ] **Windows Support** - For our Windows friends (we love you too)
- [ ] **Mobile App** - Also kidding, this is a terminal app
- [ ] **Blockchain Dashboard** - We said we were kidding about AI, not this

---

## 🤝 Contributing

We welcome contributions! Here's how to join the chaos:

1. **Fork** the repo (the GitHub way)
2. **Clone** your fork (git clone, you know the drill)
3. **Create** a branch (`git checkout -b my-awesome-feature`)
4. **Code** something amazing (or just fix a typo, we appreciate both)
5. **Test** it works (please don't break things)
6. **Commit** with a good message (`git commit -m "Add coffee level monitoring"`)
7. **Push** to your fork (`git push origin my-awesome-feature`)
8. **Open** a Pull Request (and wait for our witty review comments)

### 🐛 Bug Reports

Found a bug? Great! Here's what we need:
- What you were doing when it broke
- What you expected to happen
- What actually happened (probably something weird)
- Your OS, Python version, and terminal emulator
- Screenshots if it's visual (ASCII art screenshots are the best screenshots)

### 💡 Feature Requests

Have an idea? We love ideas! Open an issue and tell us:
- What you want
- Why you want it
- How it fits with our "questionable aesthetics" philosophy

---

## 📄 License

MIT License - basically do whatever you want, just don't blame us if your terminal catches fire.

---

## 🙏 Acknowledgments

- **[Rich](https://github.com/Textualize/rich)** - For making terminals beautiful
- **[psutil](https://github.com/giampaolo/psutil)** - For telling us what the computer is actually doing
- **[Textual](https://github.com/Textualize/textual)** - For the TUI framework that doesn't make us cry
- **Coffee** - For making this project possible
- **The Terminal Gods** - For blessing us with monospaced fonts

---

<div align="center">

### 🌟 Star this repo if you love questionable aesthetics! 🌟

[![GitHub stars](https://img.shields.io/github/stars/turancannb02/dashtrash?style=social)](https://github.com/turancannb02/dashtrash/stargazers)

**Made with ❤️ and way too much coffee**

[🏠 Home](https://github.com/turancannb02/dashtrash) • [🐛 Issues](https://github.com/turancannb02/dashtrash/issues) • [💬 Discussions](https://github.com/turancannb02/dashtrash/discussions) • [☕ Buy me coffee](https://github.com/sponsors/turancannb02)

---

*"Real-time dashboards. Questionable aesthetics."* 🗑️✨

*Because your terminal deserves better than `htop`*

</div> 
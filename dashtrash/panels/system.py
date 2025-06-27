"""
System panel for dashtrash - monitors CPU, memory, disk, and network metrics
"""

import psutil
import time
from typing import Dict, Any, List
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.text import Text
from rich.console import Console, Group
from rich.columns import Columns
from rich.align import Align


class SystemPanel:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.refresh_interval = self.config.get('refresh_interval', 2)
        self.console = Console()
        self._last_net_io = None
        self._last_time = None
        
        # History for mini charts (keep last 20 readings)
        self._cpu_history = []
        self._memory_history = []
        self._disk_history = []

    def fetch_data(self) -> Dict[str, Any]:
        """Fetch current system metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage (root partition)
            disk = psutil.disk_usage('/')
            
            # Network I/O
            net_io = psutil.net_io_counters()
            net_speed = self._calculate_network_speed(net_io)
            
            # Load average (Unix-like systems)
            try:
                load_avg = psutil.getloadavg()
            except AttributeError:
                # Windows doesn't have load average
                load_avg = (0, 0, 0)
            
            # Update history
            self._update_history(cpu_percent, memory.percent, (disk.used / disk.total) * 100)
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'frequency': cpu_freq.current if cpu_freq else 0,
                    'load_avg': load_avg,
                    'history': self._cpu_history.copy()
                },
                'memory': {
                    'total': memory.total,
                    'used': memory.used,
                    'percent': memory.percent,
                    'available': memory.available,
                    'history': self._memory_history.copy()
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100,
                    'history': self._disk_history.copy()
                },
                'network': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'speed': net_speed
                }
            }
        except Exception as e:
            return {'error': str(e)}

    def _update_history(self, cpu_percent: float, memory_percent: float, disk_percent: float):
        """Update historical data for mini charts"""
        max_history = 20
        
        self._cpu_history.append(cpu_percent)
        self._memory_history.append(memory_percent)
        self._disk_history.append(disk_percent)
        
        # Keep only last N readings
        if len(self._cpu_history) > max_history:
            self._cpu_history = self._cpu_history[-max_history:]
        if len(self._memory_history) > max_history:
            self._memory_history = self._memory_history[-max_history:]
        if len(self._disk_history) > max_history:
            self._disk_history = self._disk_history[-max_history:]

    def _calculate_network_speed(self, current_net_io) -> Dict[str, float]:
        """Calculate network speed in bytes per second"""
        current_time = time.time()
        
        if self._last_net_io and self._last_time:
            time_diff = current_time - self._last_time
            if time_diff > 0:
                sent_speed = (current_net_io.bytes_sent - self._last_net_io.bytes_sent) / time_diff
                recv_speed = (current_net_io.bytes_recv - self._last_net_io.bytes_recv) / time_diff
            else:
                sent_speed = recv_speed = 0
        else:
            sent_speed = recv_speed = 0
        
        self._last_net_io = current_net_io
        self._last_time = current_time
        
        return {'sent': sent_speed, 'recv': recv_speed}

    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    def _get_status_color(self, percent: float) -> str:
        """Get color based on usage percentage"""
        if percent < 50:
            return "green"
        elif percent < 80:
            return "yellow"
        else:
            return "red"

    def _create_mini_chart(self, data: List[float], max_width: int = 20) -> str:
        """Create a simple ASCII mini chart"""
        if not data or len(data) < 2:
            return "─" * max_width
        
        # Normalize data to chart height (0-8 levels)
        max_val = max(data) if max(data) > 0 else 1
        min_val = min(data)
        
        chart = ""
        for value in data[-max_width:]:
            # Normalize to 0-8 range
            normalized = int((value - min_val) / (max_val - min_val) * 8) if max_val > min_val else 0
            
            # Use block characters for different levels
            if normalized <= 1:
                chart += "▁"
            elif normalized <= 2:
                chart += "▂"
            elif normalized <= 3:
                chart += "▃"
            elif normalized <= 4:
                chart += "▄"
            elif normalized <= 5:
                chart += "▅"
            elif normalized <= 6:
                chart += "▆"
            elif normalized <= 7:
                chart += "▇"
            else:
                chart += "█"
        
        return chart

    def _create_progress_bar(self, percent: float, width: int = 20) -> str:
        """Create a visual progress bar"""
        filled = int((percent / 100) * width)
        empty = width - filled
        color = self._get_status_color(percent)
        
        bar = "█" * filled + "░" * empty
        return f"[{color}]{bar}[/{color}] {percent:.1f}%"

    def render(self, data: Dict[str, Any]) -> Panel:
        """Render the system metrics panel with real-time charts"""
        if 'error' in data:
            return Panel(f"[red]Error: {data['error']}[/red]", title="[bold red]System Metrics - Error[/bold red]")

        # Create main metrics table
        table = Table(show_header=True, header_style="bold blue", box=None, padding=(0, 1))
        table.add_column("Metric", style="cyan", width=10)
        table.add_column("Usage", width=25)
        table.add_column("Chart", width=22)
        table.add_column("Details", style="dim", width=25)

        # CPU Row
        cpu_color = self._get_status_color(data['cpu']['percent'])
        cpu_chart = self._create_mini_chart(data['cpu']['history'])
        cpu_bar = self._create_progress_bar(data['cpu']['percent'])
        cpu_icon = "🔥" if data['cpu']['percent'] > 80 else "⚡" if data['cpu']['percent'] > 50 else "💻"
        table.add_row(
            f"{cpu_icon} CPU",
            cpu_bar,
            f"[{cpu_color}]{cpu_chart}[/{cpu_color}]",
            f"{data['cpu']['count']} cores @ {data['cpu']['frequency']:.0f}MHz"
        )

        # Memory Row
        mem_color = self._get_status_color(data['memory']['percent'])
        mem_chart = self._create_mini_chart(data['memory']['history'])
        mem_bar = self._create_progress_bar(data['memory']['percent'])
        mem_icon = "🚨" if data['memory']['percent'] > 90 else "⚠️" if data['memory']['percent'] > 75 else "🧠"
        table.add_row(
            f"{mem_icon} RAM",
            mem_bar,
            f"[{mem_color}]{mem_chart}[/{mem_color}]",
            f"{self._format_bytes(data['memory']['used'])} / {self._format_bytes(data['memory']['total'])}"
        )

        # Disk Row
        disk_color = self._get_status_color(data['disk']['percent'])
        disk_chart = self._create_mini_chart(data['disk']['history'])
        disk_bar = self._create_progress_bar(data['disk']['percent'])
        disk_icon = "⛔" if data['disk']['percent'] > 90 else "⚠️" if data['disk']['percent'] > 80 else "💾"
        table.add_row(
            f"{disk_icon} Disk",
            disk_bar,
            f"[{disk_color}]{disk_chart}[/{disk_color}]",
            f"{self._format_bytes(data['disk']['free'])} free"
        )

        # Network Row
        net_sent_speed = self._format_bytes(data['network']['speed']['sent'])
        net_recv_speed = self._format_bytes(data['network']['speed']['recv'])
        total_speed = data['network']['speed']['sent'] + data['network']['speed']['recv']
        net_icon = "🚀" if total_speed > 1048576 else "📡" if total_speed > 10240 else "🌐"  # >1MB, >10KB, default
        net_activity = "🔴" if total_speed > 1024 else "🟢"
        table.add_row(
            f"{net_icon} Net",
            f"↑ {net_sent_speed}/s ↓ {net_recv_speed}/s",
            f"{net_activity} {'█' * int(min(total_speed / 1024, 10))}{'░' * (10 - int(min(total_speed / 1024, 10)))}",
            f"Total: {self._format_bytes(data['network']['bytes_sent'] + data['network']['bytes_recv'])}"
        )

        # Create system info footer with enhanced styling
        load_info = f"Load: {data['cpu']['load_avg'][0]:.2f}" if data['cpu']['load_avg'][0] > 0 else "Load: N/A"
        footer_text = Text()
        footer_text.append("⚡ ", style="yellow")
        footer_text.append(load_info, style="bold cyan")
        footer_text.append(" | ", style="dim")
        footer_text.append("🕐 Uptime: ", style="dim")
        footer_text.append(f"{self._get_uptime()}", style="bold green")
        footer_text.append(" | ", style="dim")
        footer_text.append("🔄 Refreshing...", style="dim italic")
        
        # Combine table and footer
        content = Group(table, "", Align.center(footer_text))
        
        return Panel(
            content, 
            title="[bold green]📊 System Metrics[/bold green]", 
            border_style="green",
            padding=(1, 2)
        )

    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            if days > 0:
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        except:
            return "Unknown" 
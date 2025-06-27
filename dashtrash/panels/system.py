"""
System panel for dashtrash - monitors CPU, memory, disk, and network metrics
"""

import psutil
import time
from typing import Dict, Any
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.console import Console


class SystemPanel:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.refresh_interval = self.config.get('refresh_interval', 2)
        self.console = Console()
        self._last_net_io = None
        self._last_time = None

    def fetch_data(self) -> Dict[str, Any]:
        """Fetch current system metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            
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
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'load_avg': load_avg
                },
                'memory': {
                    'total': memory.total,
                    'used': memory.used,
                    'percent': memory.percent,
                    'available': memory.available
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                },
                'network': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'speed': net_speed
                }
            }
        except Exception as e:
            return {'error': str(e)}

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

    def render(self, data: Dict[str, Any]) -> Panel:
        """Render the system metrics panel"""
        if 'error' in data:
            return Panel(f"[red]Error: {data['error']}[/red]", title="[bold red]System Metrics - Error[/bold red]")

        # Create table for system metrics
        table = Table(show_header=True, header_style="bold blue", box=None)
        table.add_column("Metric", style="cyan", width=15)
        table.add_column("Usage", width=20)
        table.add_column("Details", style="dim")

        # CPU
        cpu_color = self._get_status_color(data['cpu']['percent'])
        table.add_row(
            "CPU",
            f"[{cpu_color}]{data['cpu']['percent']:.1f}%[/{cpu_color}]",
            f"{data['cpu']['count']} cores | Load: {data['cpu']['load_avg'][0]:.2f}"
        )

        # Memory
        mem_color = self._get_status_color(data['memory']['percent'])
        table.add_row(
            "Memory",
            f"[{mem_color}]{data['memory']['percent']:.1f}%[/{mem_color}]",
            f"{self._format_bytes(data['memory']['used'])} / {self._format_bytes(data['memory']['total'])}"
        )

        # Disk
        disk_color = self._get_status_color(data['disk']['percent'])
        table.add_row(
            "Disk",
            f"[{disk_color}]{data['disk']['percent']:.1f}%[/{disk_color}]",
            f"{self._format_bytes(data['disk']['used'])} / {self._format_bytes(data['disk']['total'])}"
        )

        # Network
        net_sent_speed = self._format_bytes(data['network']['speed']['sent'])
        net_recv_speed = self._format_bytes(data['network']['speed']['recv'])
        table.add_row(
            "Network",
            f"↑ {net_sent_speed}/s\n↓ {net_recv_speed}/s",
            f"Total: ↑ {self._format_bytes(data['network']['bytes_sent'])} ↓ {self._format_bytes(data['network']['bytes_recv'])}"
        )

        return Panel(table, title="[bold green]System Metrics[/bold green]", border_style="green") 
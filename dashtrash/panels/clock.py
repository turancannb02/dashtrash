"""
Clock panel for dashtrash - displays time, date, and timezone info
"""

import time
import datetime
from typing import Dict, Any
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Group
from rich.align import Align
import pyfiglet


class ClockPanel:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.show_timezone = self.config.get('show_timezone', True)
        self.show_uptime = self.config.get('show_uptime', True)
        self.time_format = self.config.get('time_format', '24h')  # '12h' or '24h'
        
    def fetch_data(self) -> Dict[str, Any]:
        """Fetch current time and date information"""
        try:
            now = datetime.datetime.now()
            
            # Format time based on preference
            if self.time_format == '12h':
                time_str = now.strftime("%I:%M:%S %p")
            else:
                time_str = now.strftime("%H:%M:%S")
            
            # Get timezone info
            timezone_name = time.tzname[0] if time.tzname else "Unknown"
            
            # Calculate uptime (basic estimation)
            try:
                import psutil
                boot_time = psutil.boot_time()
                uptime_seconds = time.time() - boot_time
                uptime_str = self._format_uptime(uptime_seconds)
            except:
                uptime_str = "Unknown"
            
            return {
                'time': time_str,
                'date': now.strftime("%A, %B %d, %Y"),
                'timezone': timezone_name,
                'uptime': uptime_str,
                'timestamp': now.timestamp(),
                'weekday': now.strftime("%A"),
                'month': now.strftime("%B"),
                'day': now.day,
                'year': now.year
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime in human readable format"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def _get_time_emoji(self, hour: int) -> str:
        """Get appropriate emoji for time of day"""
        if 5 <= hour < 12:
            return "🌅"  # Morning
        elif 12 <= hour < 17:
            return "☀️"   # Afternoon
        elif 17 <= hour < 21:
            return "🌆"  # Evening
        else:
            return "🌙"  # Night
    
    def _create_ascii_time(self, time_str: str) -> str:
        """Create ASCII art for time (smaller version)"""
        try:
            return pyfiglet.figlet_format(time_str, font="small")
        except:
            return pyfiglet.figlet_format(time_str, font="standard")
    
    def render(self, data: Dict[str, Any]) -> Panel:
        """Render the clock panel"""
        if 'error' in data:
            return Panel(
                f"[red]Clock error: {data['error']}[/red]",
                title="[bold red]⏰ Clock[/bold red]"
            )
        
        # Get current hour for emoji
        current_hour = datetime.datetime.now().hour
        time_emoji = self._get_time_emoji(current_hour)
        
        # Create main time display
        time_ascii = self._create_ascii_time(data['time'])
        
        # Create info table
        info_table = Table(show_header=False, box=None, padding=(0, 2))
        info_table.add_column("Label", style="dim", width=10)
        info_table.add_column("Value", style="bold", width=20)
        
        info_table.add_row("📅 Date:", data['date'])
        
        if self.show_timezone:
            info_table.add_row("🌍 Zone:", data['timezone'])
        
        if self.show_uptime:
            info_table.add_row("⏳ Uptime:", data['uptime'])
        
        # Create a fun day indicator
        weekday = data['weekday']
        day_indicators = {
            'Monday': '😴 Monday Blues',
            'Tuesday': '💪 Tuesday Grind',
            'Wednesday': '🐪 Hump Day',
            'Thursday': '🚀 Almost There',
            'Friday': '🎉 FRIDAY!',
            'Saturday': '🌮 Weekend Vibes',
            'Sunday': '☕ Sunday Chill'
        }
        
        day_vibe = day_indicators.get(weekday, f"✨ {weekday}")
        info_table.add_row("✨ Vibe:", day_vibe)
        
        # Time zone indicator
        time_text = Text()
        time_text.append(f"{time_emoji} ", style="bold")
        time_text.append(data['time'], style="bold cyan")
        
        # Combine ASCII time with info
        content = Group(
            Text(time_ascii, style="bold green"),
            "",
            Align.center(time_text),
            "",
            info_table
        )
        
        return Panel(
            content,
            title="[bold cyan]⏰ Current Time[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        ) 
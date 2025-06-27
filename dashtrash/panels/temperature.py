"""
Temperature monitoring panel for dashtrash
"""

import psutil
import time
from typing import Dict, Any, List
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Group
from rich.align import Align


class TemperaturePanel:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.refresh_interval = self.config.get('refresh_interval', 3)
        self.temperature_history = []
        
    def fetch_data(self) -> Dict[str, Any]:
        """Fetch temperature data from system sensors"""
        try:
            temperatures = {}
            
            # Get CPU temperatures if available
            if hasattr(psutil, "sensors_temperatures"):
                temp_info = psutil.sensors_temperatures()
                
                for name, entries in temp_info.items():
                    for entry in entries:
                        sensor_name = f"{name}_{entry.label}" if entry.label else name
                        temperatures[sensor_name] = {
                            'current': entry.current,
                            'high': entry.high if entry.high else 80.0,
                            'critical': entry.critical if entry.critical else 90.0
                        }
            
            # If no sensors available, simulate some data for demo
            if not temperatures:
                import random
                temperatures = {
                    'cpu_core_0': {
                        'current': 45 + random.randint(-10, 20),
                        'high': 80.0,
                        'critical': 90.0
                    },
                    'cpu_core_1': {
                        'current': 47 + random.randint(-10, 20),
                        'high': 80.0,
                        'critical': 90.0
                    },
                    'system': {
                        'current': 42 + random.randint(-10, 15),
                        'high': 75.0,
                        'critical': 85.0
                    }
                }
            
            # Update history
            avg_temp = sum(t['current'] for t in temperatures.values()) / len(temperatures)
            self._update_history(avg_temp)
            
            return {
                'temperatures': temperatures,
                'average': avg_temp,
                'history': self.temperature_history.copy()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _update_history(self, avg_temp: float):
        """Update temperature history for mini chart"""
        max_history = 20
        self.temperature_history.append(avg_temp)
        
        if len(self.temperature_history) > max_history:
            self.temperature_history = self.temperature_history[-max_history:]
    
    def _get_temp_color(self, current: float, high: float, critical: float) -> str:
        """Get color based on temperature thresholds"""
        if current >= critical:
            return "red"
        elif current >= high:
            return "yellow"
        elif current >= high * 0.7:
            return "orange"
        else:
            return "green"
    
    def _create_temp_chart(self, history: List[float], width: int = 15) -> str:
        """Create ASCII temperature chart"""
        if not history or len(history) < 2:
            return "─" * width
        
        max_temp = max(history) if history else 50
        min_temp = min(history) if history else 30
        temp_range = max_temp - min_temp if max_temp > min_temp else 1
        
        chart = ""
        for temp in history[-width:]:
            # Normalize to 0-8 range
            normalized = int((temp - min_temp) / temp_range * 8) if temp_range > 0 else 4
            
            # Use block characters for different levels
            blocks = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
            chart += blocks[min(normalized, 7)]
        
        return chart
    
    def _format_temperature(self, temp: float) -> str:
        """Format temperature with degree symbol"""
        return f"{temp:.1f}°C"
    
    def render(self, data: Dict[str, Any]) -> Panel:
        """Render the temperature monitoring panel"""
        if 'error' in data:
            return Panel(
                f"[red]Temperature monitoring unavailable: {data['error']}[/red]",
                title="[bold red]🌡️ Temperature Monitor[/bold red]"
            )
        
        # Create temperature table
        table = Table(show_header=True, header_style="bold blue", box=None, padding=(0, 1))
        table.add_column("Sensor", style="cyan", width=12)
        table.add_column("Temp", width=8)
        table.add_column("Status", width=8)
        table.add_column("Chart", width=18)
        table.add_column("Limits", style="dim", width=12)
        
        # Add temperature rows
        for sensor_name, temp_data in data['temperatures'].items():
            current = temp_data['current']
            high = temp_data['high']
            critical = temp_data['critical']
            color = self._get_temp_color(current, high, critical)
            
            # Status indicator
            if current >= critical:
                status = "[red]🔥 HOT[/red]"
            elif current >= high:
                status = "[yellow]⚠️ WARM[/yellow]"
            else:
                status = "[green]✅ OK[/green]"
            
            # Create mini chart
            chart = self._create_temp_chart(data['history'])
            
            # Clean up sensor name
            display_name = sensor_name.replace('_', ' ').title()[:12]
            
            table.add_row(
                display_name,
                f"[{color}]{self._format_temperature(current)}[/{color}]",
                status,
                f"[{color}]{chart}[/{color}]",
                f"{high:.0f}°/{critical:.0f}°"
            )
        
        # Add average temperature info
        avg_temp = data['average']
        avg_color = self._get_temp_color(avg_temp, 70, 80)
        
        footer_text = Text()
        footer_text.append("🌡️ Avg: ", style="dim")
        footer_text.append(f"{avg_temp:.1f}°C", style=avg_color)
        footer_text.append(" | ", style="dim")
        footer_text.append("Refresh: ", style="dim")
        footer_text.append(f"{self.refresh_interval}s", style="dim")
        
        # Combine table and footer
        content = Group(table, "", Align.center(footer_text))
        
        return Panel(
            content,
            title="[bold blue]🌡️ Temperature Monitor[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        ) 
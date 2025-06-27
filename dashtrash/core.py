"""
Core dashboard engine for dashtrash - orchestrates panels and rendering
"""

import asyncio
import time
import signal
import sys
from typing import Dict, Any, List
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from .config import Config
from .banner import Banner
from .panels import SystemPanel, LogsPanel
from .plugins import PluginManager


class Dashboard:
    def __init__(self, config_path: str = "dashboard.yml"):
        self.config = Config(config_path)
        self.console = Console()
        self.banner = Banner(**self.config.get_banner_config())
        self.plugin_manager = PluginManager()
        self.panels = {}
        self.running = False
        self.refresh_rate = self.config.get_refresh_rate()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self._initialize_panels()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.running = False
        self.console.print("\n[yellow]Shutting down dashtrash...[/yellow]")

    def _initialize_panels(self):
        """Initialize all configured panels"""
        panel_configs = self.config.get_panels()
        
        for panel_config in panel_configs:
            panel_type = panel_config.get('type')
            
            if panel_type == 'system':
                self.panels['system'] = SystemPanel(panel_config)
            elif panel_type == 'logs':
                self.panels['logs'] = LogsPanel(panel_config)
            elif panel_type == 'plugin':
                plugin_name = panel_config.get('plugin_name')
                if plugin_name:
                    self.panels[f'plugin_{plugin_name}'] = {
                        'type': 'plugin',
                        'name': plugin_name,
                        'config': panel_config
                    }

    def _create_layout(self) -> Layout:
        """Create the main dashboard layout"""
        layout = Layout()
        
        panel_configs = self.config.get_panels()
        
        if len(panel_configs) == 1:
            # Single panel layout
            layout.add_split(Layout(name="main"))
        elif len(panel_configs) == 2:
            # Two panel layout (top/bottom or left/right)
            layout.split_column(
                Layout(name="top"),
                Layout(name="bottom")
            )
        else:
            # Multi-panel layout
            layout.split_column(
                Layout(name="top"),
                Layout(name="middle", ratio=2),
                Layout(name="bottom")
            )
            layout["middle"].split_row(
                Layout(name="left"),
                Layout(name="right")
            )
        
        return layout

    def _update_layout(self, layout: Layout):
        """Update layout with current panel data"""
        panel_configs = self.config.get_panels()
        
        for i, panel_config in enumerate(panel_configs):
            panel_type = panel_config.get('type')
            position = panel_config.get('position', 'main')
            
            try:
                if panel_type == 'system' and 'system' in self.panels:
                    data = self.panels['system'].fetch_data()
                    panel = self.panels['system'].render(data)
                    
                elif panel_type == 'logs' and 'logs' in self.panels:
                    data = self.panels['logs'].fetch_data()
                    panel = self.panels['logs'].render(data)
                    
                elif panel_type == 'plugin':
                    plugin_name = panel_config.get('plugin_name')
                    panel = self._render_plugin_panel(plugin_name, panel_config)
                    
                else:
                    panel = Panel(f"[red]Unknown panel type: {panel_type}[/red]", 
                                title="[bold red]Error[/bold red]")
                
                # Place panel in layout
                if position in layout:
                    layout[position].update(panel)
                elif len(panel_configs) == 1:
                    layout["main"].update(panel)
                elif i == 0 and "top" in layout:
                    layout["top"].update(panel)
                elif i == 1 and "bottom" in layout:
                    layout["bottom"].update(panel)
                else:
                    # Fallback positioning
                    available_positions = ["top", "bottom", "left", "right", "middle"]
                    for pos in available_positions:
                        if pos in layout:
                            layout[pos].update(panel)
                            break
                            
            except Exception as e:
                error_panel = Panel(f"[red]Error in {panel_type} panel: {str(e)}[/red]", 
                                  title="[bold red]Panel Error[/bold red]")
                if position in layout:
                    layout[position].update(error_panel)

    def _render_plugin_panel(self, plugin_name: str, config: Dict[str, Any]) -> Panel:
        """Render a plugin panel"""
        try:
            plugin = self.plugin_manager.load_plugin(plugin_name)
            if not plugin:
                return Panel(f"[red]Plugin '{plugin_name}' not found[/red]", 
                           title="[bold red]Plugin Error[/bold red]")
            
            # Fetch data from plugin
            if hasattr(plugin, 'fetch'):
                data = plugin.fetch()
            else:
                data = {}
            
            # Render data
            if hasattr(plugin, 'render'):
                content = plugin.render(data)
            else:
                content = str(data)
            
            return Panel(content, title=f"[bold green]{plugin_name}[/bold green]", 
                        border_style="green")
            
        except Exception as e:
            return Panel(f"[red]Plugin error: {str(e)}[/red]", 
                        title="[bold red]Plugin Error[/bold red]")

    def _create_status_footer(self) -> Panel:
        """Create status footer with dashboard info"""
        current_time = time.strftime("%H:%M:%S")
        panel_count = len(self.config.get_panels())
        
        status_text = Text()
        status_text.append(f"Time: {current_time} | ", style="dim")
        status_text.append(f"Panels: {panel_count} | ", style="dim")
        status_text.append(f"Refresh: {self.refresh_rate}s | ", style="dim")
        status_text.append("Press Ctrl+C to quit", style="bold yellow")
        
        return Panel(status_text, height=3, border_style="dim")

    async def run(self):
        """Run the dashboard main loop"""
        if not self.config.validate_config():
            self.console.print("[red]Invalid configuration. Exiting.[/red]")
            return
        
        # Show banner
        self.banner.show()
        
        # Create layout
        layout = self._create_layout()
        self.running = True
        
        with Live(layout, console=self.console, refresh_per_second=1/self.refresh_rate) as live:
            try:
                while self.running:
                    # Update all panels
                    self._update_layout(layout)
                    
                    # Add status footer if there's space
                    try:
                        main_layout = Layout()
                        main_layout.split_column(
                            Layout(layout, ratio=4),
                            Layout(self._create_status_footer(), size=3)
                        )
                        live.update(main_layout)
                    except Exception:
                        # Fallback to just the main layout
                        live.update(layout)
                    
                    await asyncio.sleep(self.refresh_rate)
                    
            except KeyboardInterrupt:
                pass
            except Exception as e:
                self.console.print(f"[red]Dashboard error: {e}[/red]")
            finally:
                self.running = False

    def start(self):
        """Start the dashboard (entry point)"""
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            pass
        finally:
            self.console.print("[green]Dashboard stopped.[/green]") 
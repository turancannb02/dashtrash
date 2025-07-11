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
from rich.align import Align

from .config import Config
from .banner import Banner
from .panels import SystemPanel, LogsPanel, TemperaturePanel, ClockPanel
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
            elif panel_type == 'temperature':
                self.panels['temperature'] = TemperaturePanel(panel_config)
            elif panel_type == 'clock':
                self.panels['clock'] = ClockPanel(panel_config)
            elif panel_type == 'plugin':
                plugin_name = panel_config.get('plugin_name')
                if plugin_name:
                    self.panels[f'plugin_{plugin_name}'] = {
                        'type': 'plugin',
                        'name': plugin_name,
                        'config': panel_config
                    }

    def _create_layout(self) -> Layout:
        """Create the main dashboard layout based on configured positions"""
        layout = Layout()
        
        panel_configs = self.config.get_panels()
        
        # Collect all configured positions
        positions = set()
        for panel_config in panel_configs:
            pos = panel_config.get('position')
            if pos:
                positions.add(pos)
        
        # Create layout based on actual positions used
        if len(positions) <= 1:
            # Single position layout
            layout.add_split(Layout(name=next(iter(positions)) if positions else "main"))
        elif positions == {"left", "right"}:
            # Two panel side-by-side layout
            layout.split_row(
                Layout(name="left", ratio=1),
                Layout(name="right", ratio=1)
            )
        elif "top" in positions and len(positions) == 3:
            # Three panel layout with top, left, right
            layout.split_column(
                Layout(name="top", ratio=1),
                Layout(name="bottom_row", ratio=1)
            )
            layout["bottom_row"].split_row(
                Layout(name="left"),
                Layout(name="right")
            )
        elif "top" in positions and "bottom" in positions:
            # Four panel layout: top, left, right, bottom
            layout.split_column(
                Layout(name="top", ratio=1),
                Layout(name="middle", ratio=1),
                Layout(name="bottom", ratio=1)
            )
            layout["middle"].split_row(
                Layout(name="left"),
                Layout(name="right")
            )
        else:
            # Default layout based on number of panels
            num_panels = len(panel_configs)
            if num_panels == 1:
                layout.add_split(Layout(name="main"))
            elif num_panels == 2:
                layout.split_row(
                    Layout(name="left", ratio=1),
                    Layout(name="right", ratio=1)
                )
            else:
                # Multi-panel default layout
                layout.split_column(
                    Layout(name="top", ratio=1),
                    Layout(name="middle", ratio=1)
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
            position = panel_config.get('position', None)
            
            try:
                # Generate panel content
                if panel_type == 'system' and 'system' in self.panels:
                    data = self.panels['system'].fetch_data()
                    panel = self.panels['system'].render(data)
                    
                elif panel_type == 'logs' and 'logs' in self.panels:
                    data = self.panels['logs'].fetch_data()
                    panel = self.panels['logs'].render(data)
                    
                elif panel_type == 'temperature' and 'temperature' in self.panels:
                    data = self.panels['temperature'].fetch_data()
                    panel = self.panels['temperature'].render(data)
                    
                elif panel_type == 'clock' and 'clock' in self.panels:
                    data = self.panels['clock'].fetch_data()
                    panel = self.panels['clock'].render(data)
                    
                elif panel_type == 'plugin':
                    plugin_name = panel_config.get('plugin_name')
                    panel = self._render_plugin_panel(plugin_name, panel_config)
                    
                else:
                    panel = Panel(f"[red]Unknown panel type: {panel_type}[/red]", 
                                title="[bold red]Error[/bold red]")
                
                # Place panel in correct layout position
                target_position = self._get_panel_position(i, position, layout)
                try:
                    layout[target_position].update(panel)
                except KeyError:
                    # If position doesn't exist, create a simple fallback
                    self.console.print(f"[yellow]Warning: Layout position '{target_position}' not found[/yellow]")
                    # Try to update the first available position or create a basic layout
                    if hasattr(layout, 'children') and layout.children:
                        layout.children[0].update(panel)
                    else:
                        # Create a basic layout if none exists
                        layout.add_split(Layout(name="main"))
                        layout["main"].update(panel)
                    
            except Exception as e:
                error_panel = Panel(f"[red]Error in {panel_type} panel: {str(e)}[/red]", 
                                  title="[bold red]Panel Error[/bold red]")
                target_position = self._get_panel_position(i, position, layout)
                if target_position and target_position in layout:
                    layout[target_position].update(error_panel)

    def _get_panel_position(self, panel_index: int, configured_position: str, layout: Layout) -> str:
        """Determine where to place a panel in the layout"""
        # If position is explicitly configured, use it if it exists
        if configured_position:
            try:
                # Test if the position exists by trying to access it
                _ = layout[configured_position]
                return configured_position
            except KeyError:
                # Position doesn't exist in current layout, continue to fallback logic
                pass
        
        # Get panel configurations to understand layout structure
        panel_configs = self.config.get_panels()
        positions = set()
        for panel_config in panel_configs:
            pos = panel_config.get('position')
            if pos:
                positions.add(pos)
        
        # Fallback logic based on actual layout structure created
        if len(positions) <= 1:
            return "main"
        elif positions == {"left", "right"}:
            return ["left", "right"][panel_index % 2]
        elif "top" in positions and len(positions) == 3:
            # Layout: top, bottom_row with left/right
            if configured_position == "top":
                return "top"
            elif configured_position in ["left", "right"]:
                return configured_position
            else:
                # Fallback for panels without specific position
                return ["top", "left", "right"][panel_index % 3]
        elif "top" in positions and "bottom" in positions:
            # Layout: top, middle (left/right), bottom
            if configured_position in ["top", "bottom"]:
                return configured_position
            elif configured_position in ["left", "right"]:
                return configured_position
            else:
                # Fallback
                return ["top", "left", "right", "bottom"][panel_index % 4]
        else:
            # Default multi-panel layout: top, middle (left/right)
            num_panels = len(panel_configs)
            if num_panels == 1:
                return "main"
            elif num_panels == 2:
                return ["left", "right"][panel_index % 2]
            else:
                # Map to: top, left, right for 3+ panels
                return ["top", "left", "right"][panel_index % 3]

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

    def _create_header(self) -> Panel:
        """Create header with dashboard title and time"""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        header_text = Text()
        header_text.append("📊 ", style="bold blue")
        header_text.append("dashtrash", style="bold green")
        header_text.append(" | ", style="dim")
        header_text.append(f"{current_time}", style="bold white")
        header_text.append(" | ", style="dim")
        header_text.append("Press Ctrl+C to quit", style="yellow")
        
        return Panel(Align.center(header_text), height=3, border_style="blue")

    async def run(self):
        """Run the dashboard main loop"""
        if not self.config.validate_config():
            self.console.print("[red]Invalid configuration. Exiting.[/red]")
            return
        
        # Show banner
        self.banner.show()
        
        # Create main layout with header
        main_layout = Layout()
        main_layout.split_column(
            Layout(name="header", size=3),
            Layout(name="content")
        )
        
        # Create content layout for panels
        content_layout = self._create_layout()
        main_layout["content"].update(content_layout)
        
        self.running = True
        
        with Live(main_layout, console=self.console, refresh_per_second=2) as live:
            try:
                while self.running:
                    # Update header
                    main_layout["header"].update(self._create_header())
                    
                    # Update all panels
                    self._update_layout(content_layout)
                    
                    # Wait for next refresh
                    await asyncio.sleep(self.refresh_rate)
                    
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                self.console.print(f"[red]Dashboard error: {str(e)}[/red]")
                self.running = False
        
        self.console.print("[green]Dashboard stopped.[/green]")

    def start(self):
        """Start the dashboard (blocking)"""
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Dashboard interrupted by user[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Dashboard error: {str(e)}[/red]")
            sys.exit(1) 
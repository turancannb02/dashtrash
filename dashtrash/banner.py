"""
Banner module for dashtrash - handles ASCII art and startup display
"""

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align


class Banner:
    def __init__(self, text="DashTrash", font="ansi_shadow", tagline="Real-time dashboards. Questionable aesthetics."):
        self.text = text
        self.font = font
        self.tagline = tagline
        self.console = Console()

    def render(self):
        """Render the banner with ASCII art and tagline"""
        try:
            # Generate ASCII art
            ascii_art = pyfiglet.figlet_format(self.text, font=self.font)
        except Exception:
            # Fallback to basic font if the specified font isn't available
            ascii_art = pyfiglet.figlet_format(self.text, font="standard")
        
        # Create styled text
        banner_text = Text(ascii_art, style="bold cyan")
        tagline_text = Text(f'> "{self.tagline}"', style="italic yellow")
        author_text = Text("Made by Turan Buyukkamaci", style="dim white")
        
        # Combine banner, tagline, and author
        content = Text()
        content.append(banner_text)
        content.append("\n")
        content.append(tagline_text)
        content.append("\n\n")
        content.append(author_text)
        
        # Create panel
        panel = Panel(
            Align.center(content),
            title="[bold green]Welcome to[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        
        return panel

    def show(self):
        """Display the banner"""
        self.console.print(self.render())
        self.console.print() 
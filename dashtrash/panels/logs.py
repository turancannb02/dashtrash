"""
Logs panel for dashtrash - displays real-time log files with filtering
"""

import os
import time
from typing import Dict, Any, List
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich.syntax import Syntax


class LogsPanel:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.log_file = self.config.get('file', '/var/log/system.log')
        self.max_lines = self.config.get('max_lines', 15)
        self.filters = self.config.get('filters', [])
        self.last_position = 0
        self.console = Console()

    def fetch_data(self) -> Dict[str, Any]:
        """Fetch recent log entries"""
        try:
            # Expand user path
            log_file = os.path.expanduser(self.log_file)
            
            if not os.path.exists(log_file):
                return {'error': f'Log file not found: {log_file}'}
            
            # Read file from last position
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
            
            # If no new lines, get the last few lines for display
            if not new_lines:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    all_lines = f.readlines()
                    new_lines = all_lines[-self.max_lines:] if all_lines else []
            
            # Filter lines if filters are specified
            if self.filters:
                filtered_lines = []
                for line in new_lines:
                    for filter_term in self.filters:
                        if filter_term.lower() in line.lower():
                            filtered_lines.append(line)
                            break
                new_lines = filtered_lines
            
            # Keep only the most recent lines
            recent_lines = new_lines[-self.max_lines:] if new_lines else []
            
            return {
                'lines': [line.rstrip() for line in recent_lines],
                'file': log_file,
                'total_lines': len(recent_lines),
                'filters_active': len(self.filters) > 0
            }
            
        except Exception as e:
            return {'error': str(e)}

    def _colorize_log_line(self, line: str) -> Text:
        """Add colors to log lines based on content"""
        text = Text()
        
        # Color coding based on log level/content
        line_lower = line.lower()
        
        if any(word in line_lower for word in ['error', 'err', 'failed', 'failure']):
            text.append(line, style="bold red")
        elif any(word in line_lower for word in ['warning', 'warn', 'deprecated']):
            text.append(line, style="bold yellow")
        elif any(word in line_lower for word in ['info', 'information']):
            text.append(line, style="bold blue")
        elif any(word in line_lower for word in ['debug', 'trace']):
            text.append(line, style="dim")
        elif any(word in line_lower for word in ['success', 'completed', 'ok']):
            text.append(line, style="bold green")
        elif 'python' in line_lower:
            text.append(line, style="bold magenta")
        elif 'git' in line_lower:
            text.append(line, style="bold cyan")
        else:
            text.append(line, style="white")
        
        return text

    def _create_log_entry(self, line: str, index: int) -> str:
        """Format a single log entry with timestamp and styling"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Truncate long lines
        if len(line) > 80:
            line = line[:77] + "..."
        
        return f"[dim]{timestamp}[/dim] {line}"

    def render(self, data: Dict[str, Any]) -> Panel:
        """Render the logs panel"""
        if 'error' in data:
            return Panel(f"[red]Error: {data['error']}[/red]", title="[bold red]Logs - Error[/bold red]")

        lines = data.get('lines', [])
        
        if not lines:
            content = Text("No log entries found", style="dim italic")
        else:
            content_lines = []
            
            for i, line in enumerate(lines):
                if line.strip():  # Skip empty lines
                    colored_line = self._colorize_log_line(line)
                    content_lines.append(colored_line)
            
            # Join lines with newlines
            content = Text()
            for i, line in enumerate(content_lines):
                content.append_text(line)
                if i < len(content_lines) - 1:
                    content.append("\n")

        # Create title with file info
        file_name = os.path.basename(data.get('file', 'unknown'))
        filter_info = f" | Filtered" if data.get('filters_active') else ""
        title = f"[bold green]📜 Logs: {file_name}[/bold green][dim]{filter_info}[/dim]"
        
        # Add footer with stats
        stats_text = Text()
        stats_text.append(f"📊 {data.get('total_lines', 0)} lines", style="dim")
        if self.filters:
            stats_text.append(f" | Filters: {', '.join(self.filters)}", style="dim yellow")

        # Combine content and stats
        full_content = Text()
        full_content.append_text(content)
        full_content.append("\n\n")
        full_content.append_text(stats_text)

        return Panel(
            full_content,
            title=title,
            border_style="green",
            padding=(1, 2),
            height=self.max_lines + 6  # Extra space for padding and stats
        ) 
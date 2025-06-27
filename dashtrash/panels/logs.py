"""
Logs panel for dashtrash - live log viewer with filters and highlighting
"""

import os
import re
from typing import Dict, Any, List
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from pathlib import Path


class LogsPanel:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.log_file = self.config.get('file', '/var/log/system.log')
        self.filters = self.config.get('filters', ['ERROR', 'WARNING', 'INFO'])
        self.max_lines = self.config.get('max_lines', 20)
        self.refresh_interval = self.config.get('refresh_interval', 1)
        self._last_position = 0

    def fetch_data(self) -> Dict[str, Any]:
        """Fetch recent log entries"""
        try:
            if not os.path.exists(self.log_file):
                return {
                    'lines': [],
                    'error': f"Log file not found: {self.log_file}",
                    'file_info': {'exists': False, 'size': 0}
                }
            
            file_stat = os.stat(self.log_file)
            file_size = file_stat.st_size
            
            # If file was truncated, reset position
            if file_size < self._last_position:
                self._last_position = 0
            
            lines = []
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                # Seek to last position or start from end if first read
                if self._last_position == 0:
                    # For first read, start from end and read last N lines
                    lines = self._get_tail_lines(f, self.max_lines)
                else:
                    f.seek(self._last_position)
                    new_lines = f.readlines()
                    lines = [line.rstrip('\n\r') for line in new_lines]
                
                self._last_position = f.tell()
            
            # Filter lines based on configured filters
            filtered_lines = self._filter_lines(lines)
            
            # Keep only the most recent lines
            if len(filtered_lines) > self.max_lines:
                filtered_lines = filtered_lines[-self.max_lines:]
            
            return {
                'lines': filtered_lines,
                'file_info': {
                    'path': self.log_file,
                    'exists': True,
                    'size': file_size,
                    'lines_count': len(filtered_lines)
                }
            }
            
        except Exception as e:
            return {
                'lines': [],
                'error': str(e),
                'file_info': {'exists': False, 'size': 0}
            }

    def _get_tail_lines(self, file_obj, num_lines: int) -> List[str]:
        """Get the last N lines from a file efficiently"""
        try:
            file_obj.seek(0, 2)  # Go to end of file
            file_size = file_obj.tell()
            
            # If file is empty
            if file_size == 0:
                return []
            
            # Start from end and work backwards
            lines = []
            buffer_size = 8192
            position = file_size
            
            while len(lines) < num_lines and position > 0:
                # Calculate how much to read
                read_size = min(buffer_size, position)
                position -= read_size
                
                file_obj.seek(position)
                chunk = file_obj.read(read_size)
                
                # Split into lines and prepend to our list
                chunk_lines = chunk.split('\n')
                
                # Handle partial line at the beginning
                if position > 0:
                    chunk_lines = chunk_lines[1:]  # Remove incomplete first line
                
                # Reverse and add to beginning of lines list
                chunk_lines.reverse()
                lines = chunk_lines + lines
            
            # Clean up and return requested number of lines
            lines = [line.rstrip('\r') for line in lines if line.strip()]
            return lines[-num_lines:] if len(lines) > num_lines else lines
            
        except Exception:
            # Fallback: read entire file and get last lines
            file_obj.seek(0)
            all_lines = file_obj.readlines()
            return [line.rstrip('\n\r') for line in all_lines[-num_lines:]]

    def _filter_lines(self, lines: List[str]) -> List[str]:
        """Filter log lines based on configured filters"""
        if not self.filters:
            return lines
        
        filtered = []
        filter_pattern = '|'.join(re.escape(f) for f in self.filters)
        
        for line in lines:
            if re.search(filter_pattern, line, re.IGNORECASE):
                filtered.append(line)
        
        return filtered

    def _highlight_line(self, line: str) -> Text:
        """Apply syntax highlighting to log lines"""
        text = Text(line)
        
        # Color coding based on log level
        line_upper = line.upper()
        if 'ERROR' in line_upper or 'FATAL' in line_upper:
            text.stylize("bold red")
        elif 'WARNING' in line_upper or 'WARN' in line_upper:
            text.stylize("bold yellow")
        elif 'INFO' in line_upper:
            text.stylize("bold blue")
        elif 'DEBUG' in line_upper:
            text.stylize("dim cyan")
        else:
            text.stylize("white")
        
        return text

    def render(self, data: Dict[str, Any]) -> Panel:
        """Render the logs panel"""
        if 'error' in data:
            error_text = Text()
            error_text.append(f"Error reading logs: {data['error']}\n", style="bold red")
            error_text.append(f"File: {self.log_file}", style="dim")
            return Panel(error_text, title="[bold red]Logs - Error[/bold red]", border_style="red")
        
        # Create content
        content = Text()
        
        if not data['lines']:
            content.append("No log entries found matching filters", style="dim yellow")
        else:
            for i, line in enumerate(data['lines']):
                if i > 0:
                    content.append("\n")
                highlighted_line = self._highlight_line(line)
                content.append(highlighted_line)
        
        # Create title with file info
        file_info = data.get('file_info', {})
        title_parts = ["[bold green]Logs[/bold green]"]
        
        if file_info.get('exists'):
            title_parts.append(f" - {Path(self.log_file).name}")
            if 'lines_count' in file_info:
                title_parts.append(f" ({file_info['lines_count']} lines)")
        
        title = "".join(title_parts)
        
        return Panel(
            content,
            title=title,
            border_style="green",
            subtitle=f"Filters: {', '.join(self.filters)}" if self.filters else None
        ) 
"""
Demo plugin for dashtrash - shows current time and random stats
"""

import time
import random
from datetime import datetime
from rich.text import Text


def fetch():
    """Fetch demo data"""
    return {
        'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'random_number': random.randint(1, 100),
        'cpu_temp': random.uniform(30.0, 70.0),
        'network_requests': random.randint(10, 500),
        'active_connections': random.randint(5, 50)
    }


def render(data):
    """Render demo data"""
    content = Text()
    
    content.append(f"🕐 Current Time: {data['current_time']}\n", style="bold blue")
    content.append(f"🎲 Random Number: {data['random_number']}\n", style="yellow")
    content.append(f"🌡️  CPU Temp: {data['cpu_temp']:.1f}°C\n", style="red" if data['cpu_temp'] > 60 else "green")
    content.append(f"📡 Network Requests: {data['network_requests']}\n", style="cyan")
    content.append(f"🔗 Active Connections: {data['active_connections']}", style="magenta")
    
    return content


def initialize(config):
    """Initialize the demo plugin"""
    print("Demo plugin initialized")
    return True


def cleanup():
    """Cleanup resources"""
    print("Demo plugin cleaned up") 
"""
Panels package for dashtrash - contains all dashboard panel implementations
"""

from .system import SystemPanel
from .logs import LogsPanel
from .temperature import TemperaturePanel
from .clock import ClockPanel

__all__ = ['SystemPanel', 'LogsPanel', 'TemperaturePanel', 'ClockPanel'] 
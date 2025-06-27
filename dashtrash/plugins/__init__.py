"""
Plugins package for dashtrash - extensible plugin system for custom panels
"""

import importlib
import os
from typing import Dict, Any, Optional


class PluginManager:
    def __init__(self, plugins_dir: str = "dashtrash/plugins"):
        self.plugins_dir = plugins_dir
        self.loaded_plugins = {}

    def load_plugin(self, plugin_name: str) -> Optional[Any]:
        """Load a plugin by name"""
        try:
            if plugin_name in self.loaded_plugins:
                return self.loaded_plugins[plugin_name]
            
            # Try to import the plugin module
            module_path = f"dashtrash.plugins.{plugin_name}"
            plugin_module = importlib.import_module(module_path)
            
            self.loaded_plugins[plugin_name] = plugin_module
            return plugin_module
            
        except ImportError:
            print(f"Plugin '{plugin_name}' not found")
            return None
        except Exception as e:
            print(f"Error loading plugin '{plugin_name}': {e}")
            return None

    def get_available_plugins(self) -> list:
        """Get list of available plugins"""
        plugins = []
        if os.path.exists(self.plugins_dir):
            for file in os.listdir(self.plugins_dir):
                if file.endswith('.py') and file != '__init__.py':
                    plugins.append(file[:-3])  # Remove .py extension
        return plugins

    def call_plugin_method(self, plugin_name: str, method_name: str, *args, **kwargs) -> Any:
        """Call a method from a loaded plugin"""
        plugin = self.load_plugin(plugin_name)
        if plugin and hasattr(plugin, method_name):
            method = getattr(plugin, method_name)
            return method(*args, **kwargs)
        return None


# Plugin interface documentation
"""
Plugin Interface:

Each plugin should implement the following methods:

def fetch() -> Dict[str, Any]:
    '''Fetch data for the plugin panel'''
    return {"key": "value"}

def render(data: Dict[str, Any]) -> str:
    '''Render the data into a displayable format'''
    return "formatted output"

Optional methods:
def initialize(config: Dict[str, Any]) -> bool:
    '''Initialize the plugin with configuration'''
    return True

def cleanup():
    '''Cleanup resources when shutting down'''
    pass
""" 
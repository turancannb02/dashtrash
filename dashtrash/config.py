"""
Configuration module for dashtrash - handles YAML parsing and validation
"""

import yaml
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class Config:
    def __init__(self, config_path: str = "dashboard.yml"):
        self.config_path = config_path
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load and parse the YAML configuration file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as file:
                    self.config = yaml.safe_load(file) or {}
            else:
                # Use default configuration
                self.config = self._get_default_config()
                self._create_default_config_file()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'panels': [
                {
                    'type': 'system',
                    'position': 'top',
                    'refresh_interval': 2
                },
                {
                    'type': 'logs',
                    'file': '/var/log/system.log',
                    'filters': ['ERROR', 'WARNING', 'INFO'],
                    'max_lines': 20,
                    'position': 'bottom'
                }
            ],
            'banner': {
                'text': 'DashTrash',
                'font': 'ansi_shadow',
                'tagline': 'Real-time dashboards. Questionable aesthetics.'
            },
            'refresh_rate': 1.0
        }

    def _create_default_config_file(self):
        """Create a default configuration file if it doesn't exist"""
        try:
            with open(self.config_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False, indent=2)
        except Exception as e:
            print(f"Warning: Could not create default config file: {e}")

    def get_panels(self) -> List[Dict[str, Any]]:
        """Get panel configurations"""
        return self.config.get('panels', [])

    def get_banner_config(self) -> Dict[str, str]:
        """Get banner configuration"""
        return self.config.get('banner', {
            'text': 'DashTrash',
            'font': 'ansi_shadow',
            'tagline': 'Real-time dashboards. Questionable aesthetics.'
        })

    def get_refresh_rate(self) -> float:
        """Get global refresh rate"""
        return self.config.get('refresh_rate', 1.0)

    def get_panel_config(self, panel_type: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific panel type"""
        for panel in self.get_panels():
            if panel.get('type') == panel_type:
                return panel
        return None

    def validate_config(self) -> bool:
        """Validate the configuration structure"""
        required_keys = ['panels']
        for key in required_keys:
            if key not in self.config:
                print(f"Missing required configuration key: {key}")
                return False
        
        # Validate panels
        panels = self.get_panels()
        if not isinstance(panels, list):
            print("'panels' must be a list")
            return False
        
        for i, panel in enumerate(panels):
            if not isinstance(panel, dict):
                print(f"Panel {i} must be a dictionary")
                return False
            if 'type' not in panel:
                print(f"Panel {i} missing required 'type' field")
                return False
        
        return True 
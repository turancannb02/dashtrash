#!/usr/bin/env python3
"""
dashtrash - Terminal-based dashboard for real-time monitoring

A lightweight, hackable, and visually engaging dashboard UI running in your terminal
for monitoring system metrics, logs, and custom data sources.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from dashtrash.core import Dashboard
from dashtrash.config import Config


def main():
    """Main entry point for dashtrash"""
    parser = argparse.ArgumentParser(
        description="dashtrash - Terminal-based dashboard for real-time monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run with default config (dashboard.yml)
  %(prog)s -c custom.yml      # Run with custom config file
  %(prog)s --validate         # Validate configuration only
  %(prog)s --create-config    # Create default configuration file

Real-time dashboards. Questionable aesthetics.
        """
    )
    
    parser.add_argument(
        '-c', '--config',
        default='dashboard.yml',
        help='Path to configuration file (default: dashboard.yml)'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate configuration file and exit'
    )
    
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create a default configuration file and exit'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='dashtrash 0.1.0'
    )
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.create_config:
        create_default_config(args.config)
        return
    
    if args.validate:
        validate_config(args.config)
        return
    
    # Check if config file exists
    if not os.path.exists(args.config):
        print(f"Configuration file '{args.config}' not found.")
        print("Creating default configuration...")
        create_default_config(args.config)
        print(f"Default configuration created at '{args.config}'")
        print("You can now run dashtrash again or edit the configuration file.")
        return
    
    try:
        # Create and start dashboard
        dashboard = Dashboard(args.config)
        dashboard.start()
        
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
    except Exception as e:
        print(f"Error starting dashboard: {e}", file=sys.stderr)
        sys.exit(1)


def create_default_config(config_path: str):
    """Create a default configuration file"""
    try:
        config = Config(config_path)
        print(f"✅ Default configuration created at '{config_path}'")
        print("\n📝 You can edit this file to customize your dashboard:")
        print(f"   - Add more panels")
        print(f"   - Configure log file paths")
        print(f"   - Adjust refresh rates")
        print(f"   - Add custom plugins")
    except Exception as e:
        print(f"❌ Error creating configuration: {e}", file=sys.stderr)
        sys.exit(1)


def validate_config(config_path: str):
    """Validate configuration file"""
    try:
        if not os.path.exists(config_path):
            print(f"❌ Configuration file '{config_path}' not found")
            sys.exit(1)
        
        config = Config(config_path)
        if config.validate_config():
            print(f"✅ Configuration file '{config_path}' is valid")
            
            # Show summary
            panels = config.get_panels()
            print(f"\n📊 Dashboard Summary:")
            print(f"   - Refresh rate: {config.get_refresh_rate()}s")
            print(f"   - Panels configured: {len(panels)}")
            
            for i, panel in enumerate(panels, 1):
                panel_type = panel.get('type', 'unknown')
                print(f"     {i}. {panel_type.title()} Panel")
                if panel_type == 'logs':
                    log_file = panel.get('file', 'N/A')
                    print(f"        Log file: {log_file}")
                elif panel_type == 'plugin':
                    plugin_name = panel.get('plugin_name', 'N/A')
                    print(f"        Plugin: {plugin_name}")
        else:
            print(f"❌ Configuration file '{config_path}' has errors")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error validating configuration: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 
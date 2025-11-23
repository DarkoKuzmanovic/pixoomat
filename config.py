"""
Configuration management for Pixoomat
"""
import json
import os
import argparse
from dataclasses import dataclass, field
from typing import Optional
import datetime

from layout_manager import LayoutManager


@dataclass
class PixoomatConfig:
    """Configuration class for Pixoomat application"""

    # Device settings
    ip_address: Optional[str] = None
    port: int = 80
    screen_size: int = 64
    brightness: int = 80

    # Time settings
    time_format: str = "24"  # "12" or "24"
    update_interval: int = 60  # seconds

    # Display settings
    text_color: tuple[int, int, int] = field(default_factory=lambda: (255, 255, 255))
    background_color: tuple[int, int, int] = field(default_factory=lambda: (0, 0, 0))
    show_weather: bool = True
    weather_interval: int = 1800  # 30 minutes

    # Layout settings
    use_gui: bool = False
    layout_config: Optional[str] = None

    # Advanced settings
    debug: bool = False
    auto_discover: bool = False
    connection_retries: int = 5
    refresh_connection: bool = True

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> 'PixoomatConfig':
        """Create config from command line arguments"""
        config = cls()

        if args.ip:
            config.ip_address = args.ip
        if args.port:
            config.port = args.port
        if args.screen_size:
            config.screen_size = args.screen_size
        if args.brightness:
            config.brightness = args.brightness
        if args.format:
            config.time_format = args.format
        if args.interval:
            config.update_interval = args.interval
        if args.debug:
            config.debug = args.debug
        if args.no_weather:
            config.show_weather = False
        if args.discover:
            config.auto_discover = args.discover
        if args.use_gui:
            config.use_gui = args.use_gui
        if args.layout_config:
            config.layout_config = args.layout_config

        # Parse color if provided
        if args.color:
            try:
                color_values = tuple(map(int, args.color.split(',')))
                if len(color_values) != 3:
                    raise ValueError("Color must have exactly 3 values (R,G,B)")
                config.text_color = color_values
            except ValueError:
                raise ValueError("Color must be in format R,G,B (e.g., 255,255,255)")

        return config

    @classmethod
    def from_file(cls, filepath: str) -> 'PixoomatConfig':
        """Load config from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            config = cls()
            for key, value in data.items():
                if hasattr(config, key):
                    setattr(config, key, value)

            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")

    @classmethod
    def from_env(cls) -> 'PixoomatConfig':
        """Load config from environment variables"""
        config = cls()

        config.ip_address = os.getenv('PIXOO_IP')

        port_env = os.getenv('PIXOO_PORT')
        if port_env:
            config.port = int(port_env)

        screen_size_env = os.getenv('PIXOO_SCREEN_SIZE')
        if screen_size_env:
            config.screen_size = int(screen_size_env)

        brightness_env = os.getenv('PIXOO_BRIGHTNESS')
        if brightness_env:
            config.brightness = int(brightness_env)

        time_format_env = os.getenv('PIXOO_TIME_FORMAT')
        if time_format_env:
            config.time_format = time_format_env

        update_interval_env = os.getenv('PIXOO_UPDATE_INTERVAL')
        if update_interval_env:
            config.update_interval = int(update_interval_env)

        debug_env = os.getenv('PIXOO_DEBUG')
        if debug_env:
            config.debug = debug_env.lower() == 'true'

        show_weather_env = os.getenv('PIXOO_SHOW_WEATHER')
        if show_weather_env:
            config.show_weather = show_weather_env.lower() == 'true'

        return config

    def to_file(self, filepath: str) -> None:
        """Save config to JSON file"""
        data = {
            'ip_address': self.ip_address,
            'port': self.port,
            'screen_size': self.screen_size,
            'brightness': self.brightness,
            'time_format': self.time_format,
            'update_interval': self.update_interval,
            'text_color': list(self.text_color),
            'background_color': list(self.background_color),
            'use_gui': self.use_gui,
            'layout_config': self.layout_config,
            'show_weather': self.show_weather,
            'weather_interval': self.weather_interval,
            'debug': self.debug,
            'auto_discover': self.auto_discover,
            'connection_retries': self.connection_retries,
            'refresh_connection': self.refresh_connection
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors"""
        errors = []

        if not 1 <= self.port <= 65535:
            errors.append("port must be between 1 and 65535")

        if self.time_format not in ['12', '24']:
            errors.append("time_format must be '12' or '24'")

        if not 0 <= self.brightness <= 100:
            errors.append("brightness must be between 0 and 100")

        if self.update_interval < 1:
            errors.append("update_interval must be at least 1 second")

        if self.screen_size not in [16, 32, 64]:
            errors.append("screen_size must be 16, 32, or 64")

        if len(self.text_color) != 3 or any(not 0 <= c <= 255 for c in self.text_color):
            errors.append("text_color must be RGB values between 0 and 255")

        if len(self.background_color) != 3 or any(not 0 <= c <= 255 for c in self.background_color):
            errors.append("background_color must be RGB values between 0 and 255")

        return errors


def create_argument_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Pixoomat - Display time on Divoom Pixoo 64',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --ip 192.168.1.100
  python main.py --discover --format 24 --brightness 80
  python main.py --config config.json
        """
    )

    # Connection options
    parser.add_argument('--ip', help='IP address of Pixoo device')
    parser.add_argument('--port', type=int, help='Port of Pixoo device (default: 80)')
    parser.add_argument('--discover', action='store_true',
                     help='Auto-discover Pixoo devices on network')

    # Display options
    parser.add_argument('--format', choices=['12', '24'], default='24',
                     help='Time format: 12-hour or 24-hour (default: 24)')
    parser.add_argument('--brightness', type=int, choices=range(0, 101),
                     help='Screen brightness (0-100, default: 80)')
    parser.add_argument('--color', help='Text color as R,G,B (e.g., 255,255,255)')
    parser.add_argument('--screen-size', type=int, choices=[16, 32, 64],
                     help='Screen size (default: 64)')
    parser.add_argument('--no-weather', action='store_true',
                     help='Disable weather display')

    # Timing options
    parser.add_argument('--interval', type=int,
                     help='Update interval in seconds (default: 60)')

    # Other options
    parser.add_argument('--config', help='Path to configuration JSON file')
    parser.add_argument('--debug', action='store_true',
                     help='Enable debug output')
    parser.add_argument('--save-config', help='Save current settings to config file')
    parser.add_argument('--use-gui', action='store_true',
                     help='Launch Compact GUI for widget layout design')
    parser.add_argument('--layout-config', help='Path to widget layout configuration file')

    return parser
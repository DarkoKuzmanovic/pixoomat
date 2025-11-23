"""
Main application for Pixoomat - Time display for Divoom Pixoo 64
"""
import signal
import sys
import time
import datetime
import json
from typing import Optional, Dict, Any

from pixoo import Pixoo
from pixoo_client import CustomPixoo
from config import PixoomatConfig, create_argument_parser
from widgets import get_plugin_manager
from layout_manager import LayoutManager
from device_discovery import PixooDiscovery, test_connection
from weather_service import WeatherService
from widgets.plugins.weather_widget import WeatherWidget


# CustomPixoo class moved to pixoo_client.py

class PixoomatApp:
    """Main application class for Pixoomat"""

    def __init__(self, config: PixoomatConfig):
        self.config = config
        self.pixoo: Optional[Pixoo] = None
        self.layout_manager = LayoutManager(config.screen_size)
        self.weather_service = WeatherService(config.weather_interval) if config.show_weather else None
        self.last_update = datetime.datetime.min
        self.running = False

        # Initialize default widgets if no layout config provided
        if not config.layout_config:
            self._setup_default_widgets()
        else:
            self._load_layout(config.layout_config)

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _setup_default_widgets(self):
        """Setup default widgets for backward compatibility"""
        plugin_manager = get_plugin_manager()

        # Create clock widget
        clock_widget = plugin_manager.create_widget("Clock")
        if clock_widget:
            clock_widget.update_interval = self.config.update_interval
            clock_widget.set_property('time_format', self.config.time_format)
            clock_widget.set_property('text_color', self.config.text_color)

            # Center clock widget
            clock_x = self.config.screen_size // 2 - clock_widget.width // 2
            clock_y = self.config.screen_size // 2 - clock_widget.height // 2
            clock_widget.set_position(clock_x, clock_y)

            # Add to layout
            self.layout_manager.add_widget(clock_widget)

        # Create weather widget if enabled
        if self.config.show_weather and self.weather_service:
            weather_widget = plugin_manager.create_widget("Weather")
            if weather_widget:
                weather_widget.set_property('text_color', self.config.text_color)

                # Position weather widget at bottom right
                weather_x = self.config.screen_size - weather_widget.width - 2
                weather_y = self.config.screen_size - weather_widget.height - 2
                weather_widget.set_position(weather_x, weather_y)
                weather_widget.z_index = 1  # Place above clock if overlapping

                # Connect weather service to widget
                if isinstance(weather_widget, WeatherWidget):
                    weather_widget.get_weather_data = self.weather_service.get_weather

                # Add to layout
                self.layout_manager.add_widget(weather_widget)

        # Set background color
        self.layout_manager.background_color = self.config.background_color

    def _load_layout(self, layout_config_path: str):
        """Load layout from configuration file"""
        try:
            with open(layout_config_path, 'r') as f:
                layout_data = json.load(f)

            self.layout_manager = LayoutManager.from_dict(layout_data)

            # Connect weather service to weather widgets
            if self.weather_service:
                for widget in self.layout_manager.widgets:
                    if isinstance(widget, WeatherWidget):
                        widget.get_weather_data = self.weather_service.get_weather

            print(f"Loaded layout from {layout_config_path}")
        except Exception as e:
            print(f"ERROR: Failed to load layout config: {e}")
            print("Falling back to default widgets...")
            self._setup_default_widgets()

    def connect_to_device(self) -> bool:
        """Connect to Pixoo device with retry logic"""
        if not self.config.ip_address:
            print("ERROR: No IP address specified. Use --ip or --discover")
            return False

        print(f"Connecting to Pixoo at {self.config.ip_address}...")

        for attempt in range(self.config.connection_retries):
            try:
                self.pixoo = CustomPixoo(
                    self.config.ip_address,
                    size=self.config.screen_size,
                    debug=self.config.debug,
                    refresh_connection_automatically=self.config.refresh_connection,
                    port=self.config.port
                )

                # Test connection
                self.pixoo.fill((0, 0, 0))
                self.pixoo.set_brightness(self.config.brightness)
                self.pixoo.push()

                print(f"SUCCESS: Connected to Pixoo at {self.config.ip_address}:{self.config.port}")
                return True

            except Exception as e:
                print(f"ERROR: Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.config.connection_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)

        print(f"ERROR: Failed to connect after {self.config.connection_retries} attempts")
        return False

    def discover_and_connect(self) -> bool:
        """Auto-discover devices and connect to first available"""
        discovery = PixooDiscovery(timeout=self.config.connection_retries * 2)
        devices = discovery.discover()

        if not devices:
            print("ERROR: No Pixoo devices found on network")
            return False

        discovery.list_discovered_devices()

        # Try to connect to each device until one works
        for device in devices:
            ip = device.get('ip')
            if ip and test_connection(ip):
                self.config.ip_address = ip
                return self.connect_to_device()

        print("ERROR: Could not connect to any discovered device")
        return False

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        self.running = False

    def update_display(self):
        """Update display with current widget layout"""
        if not self.pixoo:
            return

        # Check if we need to update
        time_since_last = (datetime.datetime.now() - self.last_update).total_seconds()
        if time_since_last < self.config.update_interval:
            return

        try:
            # Clear screen with background color
            bg_r, bg_g, bg_b = self.config.background_color
            self.pixoo.fill((bg_r, bg_g, bg_b))

            # Update widgets that need refreshing
            updated_widgets = self.layout_manager.update_widgets()

            # Render each widget based on their render data
            for widget in self.layout_manager.widgets:
                if widget.visible:
                    render_data = widget.get_render_data()
                    self._render_widget_data(self.pixoo, render_data)

            # Push to device
            self.pixoo.push()
            self.last_update = datetime.datetime.now()

            if self.config.debug:
                print(f"DISPLAY: Updated display, {len(updated_widgets)} widgets updated")

        except Exception as e:
            print(f"ERROR: Failed to update display: {e}")

    def _render_widget_data(self, pixoo, render_data: Dict[str, Any]):
        """
        Render widget data to the pixoo device

        Args:
            pixoo: Pixoo device instance
            render_data: Widget render data dictionary
        """
        widget_type = render_data.get('type', 'text')

        if widget_type == 'text':
            text = render_data.get('text', '')
            x = render_data.get('x', 0)
            y = render_data.get('y', 0)
            color = render_data.get('color', (255, 255, 255))
            bg_color = render_data.get('background_color')

            # Draw background if specified
            if bg_color:
                # Estimate text size for background rectangle
                text_width = len(text) * 3  # Rough estimate
                text_height = 6  # Rough estimate
                pixoo.draw_filled_rectangle(x-1, y-1, x+text_width+1, y+text_height+1, *bg_color)

            # Draw text
            pixoo.draw_text(text, xy=(x, y), rgb=color)

        # Add other widget types as needed
        elif widget_type == 'rectangle':
            x1 = render_data.get('x', 0)
            y1 = render_data.get('y', 0)
            x2 = render_data.get('x2', x1)
            y2 = render_data.get('y2', y1)
            color = render_data.get('color', (255, 255, 255))
            filled = render_data.get('filled', False)

            if filled:
                pixoo.draw_filled_rectangle(x1, y1, x2, y2, *color)
            else:
                pixoo.draw_rectangle(x1, y1, x2, y2, *color)

        elif widget_type == 'circle':
            x = render_data.get('x', 0)
            y = render_data.get('y', 0)
            radius = render_data.get('radius', 5)
            color = render_data.get('color', (255, 255, 255))
            filled = render_data.get('filled', False)

            if filled:
                pixoo.draw_filled_circle(x, y, radius, *color)
            else:
                pixoo.draw_circle(x, y, radius, *color)

    def run(self) -> int:
        """Main application loop"""
        print("Starting Pixoomat...")

        # Validate configuration
        errors = self.config.validate()
        if errors:
            print("ERROR: Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return 1

        # Connect to device
        if self.config.auto_discover:
            if not self.discover_and_connect():
                return 1
        else:
            if not self.connect_to_device():
                return 1

        print("SUCCESS: Pixoomat is running. Press Ctrl+C to stop.")
        self.running = True

        try:
            while self.running:
                self.update_display()
                time.sleep(1)  # Check every second

        except KeyboardInterrupt:
            pass  # Handled by signal handler

        # Cleanup
        if self.pixoo:
            try:
                self.pixoo.fill((0, 0, 0))  # Clear screen
                self.pixoo.push()
                print("Cleared device display")
            except:
                pass

        print("Pixoomat stopped.")
        return 0


def load_config(args) -> Optional[PixoomatConfig]:
    """Load configuration from various sources"""
    config = PixoomatConfig()

    # Priority: CLI args > config file > environment > defaults

    if args.config:
        try:
            config = PixoomatConfig.from_file(args.config)
            print(f"CONFIG: Loaded config from {args.config}")
        except Exception as e:
            print(f"ERROR: Failed to load config file: {e}")
            return None

    # Override with environment variables
    env_config = PixoomatConfig.from_env()
    if any([env_config.ip_address, env_config.debug]):
        # Merge environment config
        for attr in ['ip_address', 'debug', 'brightness', 'time_format']:
            env_value = getattr(env_config, attr)
            if env_value is not None:
                setattr(config, attr, env_value)

    # Override with CLI arguments
    config = PixoomatConfig.from_args(args)

    return config


def main():
    """Main entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Handle special cases
    if args.save_config:
        config = load_config(args)
        if config:
            try:
                config.to_file(args.save_config)
                print(f"SAVED: Configuration saved to {args.save_config}")
                return 0
            except Exception as e:
                print(f"ERROR: Failed to save config: {e}")
                return 1

    # Check if GUI mode is requested first (before validation)
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.use_gui:
        # Load configuration for GUI (skip some validations)
        config = load_config(args)
        if not config:
            return 1

        try:
            from gui.main_window_compact import run_gui
            return run_gui(config)
        except ImportError:
            print("ERROR: GUI components not available. Install GUI dependencies first.")
            return 1

    # Load configuration for CLI mode
    config = load_config(args)
    if not config:
        return 1

    # Create and run app (CLI mode)
    app = PixoomatApp(config)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
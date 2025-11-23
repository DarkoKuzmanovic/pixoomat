# Pixoomat - Agent Guide

This guide provides essential information for agents working with the Pixoomat codebase, a Python application that displays the current time on Divoom Pixoo 64 devices via WiFi.

## 📖 Documentation

- **[README.md](../README.md)** - Main project documentation with quick start guide and configuration options
- **[WIDGET_DEVELOPMENT.md](./WIDGET_DEVELOPMENT.md)** - Comprehensive guide for creating custom widgets
- **[AGENTS.md](./AGENTS.md)** - This file - Agent-specific information and development patterns

## Project Overview

Pixoomat is a Python application that connects to Divoom Pixoo 64 devices and displays the current time with customizable formatting. It supports automatic device discovery, weather display, a compact GUI for widget layout design, and robust error handling.

## Essential Commands

### Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application with auto-discovery
python main.py --discover

# Run with specific IP
python main.py --ip 192.168.1.100

# Run with custom settings
python main.py --ip 192.168.1.100 --format 12 --brightness 90 --color 255,100,50

# Save current settings to config file
python main.py --ip 192.168.1.100 --save-config my-config.json

# Run with config file
python main.py --config my-config.json

# Enable debug mode
python main.py --debug

# Launch Compact GUI for widget layout design
python main.py --use-gui
```

### Testing

```bash
# Run basic functionality test
python tests/test_simulator.py

# Run widget system tests
python tests/test_widget_system.py

# Run plugin system tests
python tests/test_plugin_system.py

# Run new widget tests
python tests/test_new_widgets.py

# Run widget serialization tests
python tests/test_widget_serialization.py

# Run fixes validation tests
python tests/test_fixes_validation.py

# Run edge cases tests
python tests/test_edge_cases.py

# Run GUI tests
python tests/test_gui.py

# Run advanced GUI tests
python tests/test_gui_advanced.py
```

## Code Organization

```bash
pixoomat/
├── main.py              # Main application and entry point
├── config.py            # Configuration management
├── pixoo_client.py      # Custom Pixoo client wrapper
├── clock_display.py     # Time formatting and display logic
├── device_discovery.py  # Network device discovery
├── weather_service.py   # Weather data fetching
├── gui/                 # Compact GUI components
│   ├── main_window_compact.py    # Main GUI window
│   ├── device_panel_compact.py   # Device management panel
│   ├── property_panel_compact.py # Widget property editor
│   ├── widget_palette.py         # Widget selection palette
│   ├── toolbar.py                # GUI toolbar
│   ├── file_operations.py        # File operations
│   └── undo_manager.py           # Undo/redo system
├── widgets/             # Widget system
│   ├── base_widget.py           # Base widget class
│   ├── plugin_system.py         # Plugin management system
│   └── plugins/                 # Plugin widgets
│       ├── clock_widget.py      # Clock display widget
│       ├── weather_widget.py    # Weather display widget
│       ├── date_widget.py       # Date display widget
│       ├── countdown_widget.py  # Countdown timer widget
│       ├── progress_bar.py      # Progress bar widget
│       ├── simple_text.py       # Simple text widget
│       └── system_stats_widget.py # System monitoring widget
├── tests/
│   ├── test_simulator.py    # Basic functionality testing
│   ├── test_widget_system.py
│   ├── test_plugin_system.py
│   ├── test_widget_serialization.py
│   ├── test_fixes_validation.py
│   ├── test_edge_cases.py
│   ├── test_gui.py
│   └── test_gui_advanced.py
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

## Key Components

### Main Application (main.py)

- Entry point with `PixoomatApp` class that orchestrates the entire application
- Handles device connection with retry logic
- Manages the main update loop
- Implements graceful shutdown with signal handlers

### Pixoo Client (pixoo_client.py)

- `CustomPixoo` class to support non-standard ports and extend base functionality

### Configuration (config.py)

- `PixoomatConfig` dataclass manages all configuration options
- Supports multiple configuration sources with priority: CLI args > config file > environment > defaults
- Configuration validation with detailed error reporting
- JSON config file support
- Environment variable support

### Clock Display (clock_display.py)

- `ClockDisplay` class handles time formatting and display positioning
- Supports both 12-hour and 24-hour time formats
- Calculates centered text positions on the device screen
- Includes optional weather and seconds indicators

### Device Discovery (device_discovery.py)

- `PixooDiscovery` class implements device discovery using mDNS/Bonjour
- Fallback network scanning for device discovery
- Connection testing utilities
- Device listing and IP resolution

### Weather Service (weather_service.py)

- `WeatherService` class fetches weather data from Open-Meteo
- Location detection using IP-API
- Caching mechanism to reduce API calls

### Compact GUI

- `CompactPixoomatGUI` class provides the main GUI interface
- Three-pane layout with widget palette, canvas, and property panels
- Widget-based layout system for customizing device display
- Real-time preview and device connection testing
- File operations for saving/loading widget layouts
- Plugin system integration for automatic widget discovery

## Widget System

### Plugin Architecture

The widget system uses a plugin architecture that allows for dynamic loading of widgets:

- **BaseWidget**: Abstract base class that all widgets inherit from
- **WidgetPlugin**: Abstract base class for widget plugins
- **PluginManager**: Manages plugin registration, discovery, and widget creation
- **WidgetMetadata**: Dataclass containing plugin information (name, description, version, etc.)

### Plugin Discovery Mechanism

Widgets are automatically discovered through Python's import system:

1. **Directory Structure**: Plugins must be placed in `widgets/plugins/` directory
2. **File Naming**: Plugin files should follow `snake_case` naming convention
3. **Auto-Loading**: The `PluginManager` scans the directory on startup and registers all valid plugins
4. **Metadata Validation**: Each plugin provides metadata for categorization and versioning
5. **Dependency Management**: Plugins can declare dependencies that are checked at runtime

### Plugin Registration Process

```python
# Automatic registration happens when plugin files are imported
# PluginManager discovers and registers plugins during application startup
plugin_manager = PluginManager()
available_widgets = plugin_manager.get_available_widgets()
```

This architecture enables:
- **Hot-reloading**: Plugins can be added/removed without restarting the application
- **Versioning**: Multiple versions of the same plugin can coexist
- **Dependency Management**: Automatic resolution of plugin dependencies
- **Metadata-driven UI**: Property editors automatically adapt based on plugin schemas

### Available Widgets

1. **ClockWidget**: Displays current time in 12/24 hour formats
2. **WeatherWidget**: Shows current temperature with C/F support
3. **DateWidget**: Configurable date display with day of week
4. **CountdownWidget**: Countdown to specific date/time
5. **ProgressBarWidget**: Visual progress indicators
6. **SimpleTextWidget**: Custom text display
7. **SystemStatsWidget**: CPU, memory, and disk usage monitoring

### Widget Properties

All widgets support:
- Position (x, y) and size (width, height)
- Configurable properties via property schema
- Serialization/deserialization for layout saving
- Update intervals for dynamic content
- Validation of configuration

### Widget System Features

- **Dynamic Widget Loading**: Widgets are automatically discovered and loaded from the `widgets/plugins/` directory
- **Property Validation**: Each widget defines a schema for its configurable properties with validation
- **Layout Persistence**: Widget layouts can be saved to and loaded from JSON files
- **Real-time Updates**: Dynamic widgets support configurable update intervals
- **Error Handling**: Graceful error handling for invalid configurations and failed updates
- **Undo/Redo Support**: The GUI includes an undo/redo system for widget operations
- **Widget Interaction**: Widgets can be selected, moved, resized, and configured via the GUI

### Plugin Development

To create a new widget:
1. Inherit from `BaseWidget` and implement abstract methods
2. Create a plugin class inheriting from `WidgetPlugin`
3. Implement required methods: `metadata`, `create_widget`, `get_property_schema`
4. Place in `widgets/plugins/` directory for auto-discovery

## Naming Conventions and Style Patterns

### Code Style

- Python 3.8+ compatible
- Type hints used throughout the codebase
- Dataclasses for configuration objects
- Descriptive variable and function names
- Consistent use of docstrings for all classes and functions

### Naming Conventions

- Class names: PascalCase (e.g., `PixoomatApp`, `ClockDisplay`, `SystemStatsWidget`)
- Function names: snake_case (e.g., `connect_to_device`, `format_time`)
- Constants: UPPER_SNAKE_CASE (e.g., `SERVICE_TYPE`)
- Private methods: prefixed with underscore (e.g., `_signal_handler`)
- Widget files: snake_case with `_widget.py` suffix (e.g., `system_stats_widget.py`)
- Plugin classes: PascalCase with `Plugin` suffix (e.g., `SystemStatsWidgetPlugin`)

## Configuration Options

### Command Line Arguments

- `--ip`: IP address of Pixoo device
- `--port`: Port of Pixoo device (default: 80)
- `--discover`: Auto-discover devices on network
- `--format`: Time format: 12 or 24-hour (default: 24)
- `--brightness`: Screen brightness (0-100, default: 80)
- `--color`: Text color as R,G,B (e.g., 255,255,255)
- `--screen-size`: Screen size (16, 32, 64, default: 64)
- `--no-weather`: Disable weather display
- `--interval`: Update interval in seconds (default: 60)
- `--config`: Path to JSON config file
- `--debug`: Enable debug output
- `--save-config`: Save current settings to config file
- `--use-gui`: Launch Compact GUI for widget layout design
- `--layout-config`: Path to widget layout configuration file

### Configuration File

JSON format with the following keys:

- `ip_address`: IP address of device
- `port`: Port number (default: 80)
- `screen_size`: Screen size (16, 32, 64)
- `brightness`: Brightness level (0-100)
- `time_format`: "12" or "24"
- `update_interval`: Update interval in seconds
- `text_color`: RGB values as array [R, G, B]
- `background_color`: RGB values as array [R, G, B]
- `show_weather`: Boolean to enable/disable weather
- `weather_interval`: Weather update interval in seconds
- `use_gui`: Boolean to launch GUI
- `layout_config`: Path to widget layout configuration file
- `debug`: Enable debug output
- `auto_discover`: Enable auto-discovery
- `connection_retries`: Number of connection retries
- `refresh_connection`: Refresh connection automatically

### Environment Variables

- `PIXOO_IP`: IP address of device
- `PIXOO_PORT`: Port number
- `PIXOO_SCREEN_SIZE`: Screen size
- `PIXOO_BRIGHTNESS`: Brightness level
- `PIXOO_TIME_FORMAT`: Time format
- `PIXOO_UPDATE_INTERVAL`: Update interval
- `PIXOO_DEBUG`: Enable debug output
- `PIXOO_SHOW_WEATHER`: Enable weather display

## Testing Approach

### Current Testing

- Basic functionality testing with `tests/test_simulator.py`
- Widget system testing with `tests/test_widget_system.py`
- Plugin system testing with `tests/test_plugin_system.py`
- New widget testing with `tests/test_new_widgets.py`
- Widget serialization testing with `tests/test_widget_serialization.py`
- Fixes validation testing with `tests/test_fixes_validation.py`
- Edge cases testing with `tests/test_edge_cases.py`
- GUI testing with `tests/test_gui.py`
- Advanced GUI testing with `tests/test_gui_advanced.py`
- Manual testing by running the application with various configurations
- Connection testing utilities in `device_discovery.py`

### Testing Patterns

- Configuration validation with detailed error reporting
- Connection testing with retry logic
- Time formatting verification
- Device discovery simulation
- Widget plugin discovery and registration
- Widget property validation and serialization
- GUI layout and widget interaction testing
- Error handling and recovery scenarios

## Task Management with todo.md

When working with the `todo.md` file, agents should follow these practices:

### Todo.md Format
- The `todo.md` file contains task items formatted as markdown checkboxes: `- [ ]` for incomplete tasks, `- [x]` for completed tasks
- Tasks should be listed in priority order with the most important/urgent items first

### Best Practices
- **Checkmark completed tasks**: After successfully finishing any task listed in `todo.md`, immediately update the checkbox from `[ ]` to `[x]`
- **Update systematically**: Don't leave tasks partially completed - only mark as done when the work is fully finished and tested
- **Add new tasks**: When new actionable items are discovered during development, add them to the todo.md file with `[ ]` status
- **Maintain context**: Ensure todos are specific and actionable, not vague or overly broad

### Example
```markdown
- [x] Fix progress bar visibility issue
- [x] Resolve Simple Text widget error
- [ ] Implement visual color picker
- [ ] Refactor test directory structure
```

When a task is completed, update it to:
```markdown
- [x] Fix progress bar visibility issue
- [x] Resolve Simple Text widget error
- [x] Implement visual color picker
- [ ] Refactor test directory structure
```

## Important Gotchas and Non-Obvious Patterns

### Device Connection

- The application uses a custom `CustomPixoo` class to support non-standard ports
- Connection retry logic with exponential backoff
- Automatic connection refreshing to handle Pixoo firmware issues
- Graceful handling of connection failures

### Time Display

- Text positioning calculations based on estimated character widths
- Update interval checking to avoid excessive screen updates
- Support for both 12-hour and 24-hour time formats

### Device Discovery

- Primary method uses mDNS/Bonjour for device discovery
- Fallback network scanning when mDNS fails
- Device identification through HTTP response content checking

### Weather Integration

- Location detection using IP-API
- Weather data caching to reduce API calls
- Weather display positioned at bottom right of screen

### Configuration Management

- Multiple configuration sources with clear priority order
- Comprehensive validation with detailed error messages
- JSON serialization and deserialization for config files

## Dependencies

- **pixoo** (>=0.9.2): Core library for communicating with Pixoo devices
- **zeroconf** (>=0.112.0): mDNS/Bonjour device discovery
- **psutil** (>=5.8.0): System statistics monitoring for SystemStatsWidget
- **Pillow** (PIL): Image processing for widget rendering
- Standard library modules: argparse, datetime, json, os, signal, socket, time, urllib, dataclasses, typing

## Project Specific Context

### Architecture Decisions

- Separation of concerns with distinct modules for configuration, display, discovery, and weather
- Extensive use of classes to encapsulate functionality
- Robust error handling with graceful degradation
- Support for multiple configuration methods

### Known Limitations

- Weather display requires internet connectivity
- Device discovery may not work on all networks
- Pixoo firmware has known issues with frequent updates
- Limited error recovery for network interruptions

### Best Practices

- Use 60+ second update intervals to avoid firmware bugs
- Place Pixoo close to router for better connectivity
- Use USB power for stability
- Lower brightness extends device lifespan

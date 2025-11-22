# Pixoomat

## **Display current time on your Divoom Pixoo 64 via WiFi**

Pixoomat is a Python application that connects to your Divoom Pixoo 64 device and displays the current time. It supports automatic device discovery, multiple time formats, and robust error handling.

## ✨ Features

- 🕐 **Real-time Clock** - Displays current time with automatic updates
- 🔍 **Auto Discovery** - Automatically finds Pixoo devices on your network
- 🎨 **Customizable** - Configure colors, brightness, time format
- 🖥️ **Compact GUI** - Visual widget layout designer for custom displays
- 🔄 **Robust** - Handles disconnections and automatic reconnection
- 📱 **Cross-platform** - Works on Windows, macOS, and Linux
- 🛠️ **Easy Setup** - Simple CLI with multiple configuration options

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Divoom Pixoo 64 device connected to your WiFi network
- Python packages (install with `pip install -r requirements.txt`)

### Installation

1. **Clone or download** this repository
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

1. **Auto-discover and connect:**

   ```bash
   python main.py --discover
   ```

2. **Connect with known IP:**

   ```bash
   python main.py --ip 192.168.1.100
   ```

3. **Customize display:**

   ```bash
   python main.py --ip 192.168.1.100 --format 12 --brightness 90 --color 255,100,50
   ```

4. **Launch GUI for visual layout design:**

   ```bash
   python main.py --use-gui
   ```

## 📖 Configuration Options

### Command Line Arguments

| Argument          | Description                                 | Default       |
| ----------------- | ------------------------------------------- | ------------- |
| `--ip`            | IP address of Pixoo device                  | Auto-discover |
| `--discover`      | Auto-discover devices on network            | False         |
| `--format`        | Time format: 12 or 24-hour                  | 24            |
| `--brightness`    | Screen brightness (0-100)                   | 80            |
| `--color`         | Text color as R,G,B                         | 255,255,255   |
| `--screen-size`   | Screen size (16, 32, 64)                    | 64            |
| `--interval`      | Update interval in seconds                  | 60            |
| `--config`        | Path to JSON config file                    | None          |
| `--debug`         | Enable debug output                         | False         |
| `--save-config`   | Save settings to config file                | None          |
| `--use-gui`       | Launch Compact GUI for widget layout design | False         |
| `--layout-config` | Path to widget layout configuration file    | None          |

### Configuration File

Create a JSON file to save your settings:

```json
{
  "ip_address": "192.168.1.100",
  "screen_size": 64,
  "brightness": 80,
  "time_format": "24",
  "update_interval": 60,
  "text_color": [255, 255, 255],
  "background_color": [0, 0, 0],
  "use_gui": false,
  "layout_config": null,
  "show_weather": true,
  "weather_interval": 1800,
  "debug": false,
  "auto_discover": false,
  "connection_retries": 5,
  "refresh_connection": true
}
```

Use with: `python main.py --config my-config.json`

### Environment Variables

Set these environment variables for configuration:

```bash
export PIXOO_IP="192.168.1.100"
export PIXOO_BRIGHTNESS="80"
export PIXOO_TIME_FORMAT="24"
export PIXOO_DEBUG="true"
export PIXOO_SHOW_WEATHER="true"
```

## 🖥️ GUI Usage

Pixoomat includes a compact graphical user interface for designing custom widget layouts:

### Launching the GUI

```bash
python main.py --use-gui
```

### GUI Features

- **Widget Palette**: Add clock, weather, text, and progress bar widgets
- **Visual Canvas**: Drag and drop widgets to design your layout
- **Property Editor**: Customize widget appearance and behavior
- **Device Management**: Connect to and test your Pixoo device
- **File Operations**: Save and load widget layouts

### GUI Workflow

1. Launch the GUI with `python main.py --use-gui`
2. Connect to your Pixoo device using the device panel
3. Add widgets from the widget palette
4. Position and customize widgets on the canvas
5. Save your layout for use with the CLI

## 🔧 Advanced Usage

### Device Discovery

Pixoomat can discover devices using two methods:

1. **mDNS/Bonjour** (preferred):

   ```bash
   python main.py --discover
   ```

2. **Network Scan** (fallback):
   - Scans your local network for devices
   - Slower but more reliable

### Custom Colors

Specify colors using RGB values:

```bash
# White text
python main.py --color 255,255,255

# Red text
python main.py --color 255,0,0

# Blue text
python main.py --color 0,100,255
```

### Time Formats

- **24-hour**: `14:30` (default)
- **12-hour**: `2:30 PM`

## 🐛 Troubleshooting

### Connection Issues

1. **Device not found:**

   - Ensure Pixoo is on same WiFi network
   - Check if device is powered on
   - Try manual IP with `--ip` option

2. **Connection failures:**

   - Verify IP address is correct
   - Check network connectivity
   - Increase `connection_retries` in config

3. **Display stops updating:**
   - This is a known Pixoo firmware issue
   - Restart Pixoomat application
   - The app includes `refresh_connection_automatically=True` to mitigate

### Debug Mode

Enable debug output for troubleshooting:

```bash
python main.py --debug
```

Debug mode shows:

- Connection attempts
- Update timestamps
- Error details
- Seconds indicator (visual)

## 🏗️ Project Structure

```dash
pixoomat/
├── main.py              # Main application and entry point
├── config.py            # Configuration management
├── clock_display.py      # Time formatting and display logic
├── device_discovery.py   # Network device discovery
├── weather_service.py    # Weather data fetching
├── gui/                 # Compact GUI components
├── widgets/             # Widget system
├── requirements.txt      # Python dependencies
└── README.md           # This file
```

## 📚 Dependencies

- **pixoo** (>=0.9.2) - Core Pixoo device library
- **zeroconf** (>=0.112.0) - mDNS device discovery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [pixoo](https://github.com/SomethingWithComputers/pixoo) - Core Pixoo library
- [pixoo-rest](https://github.com/4ch1m/pixoo-rest) - REST API for Pixoo devices

## 💡 Tips

- **Update Interval**: Keep at 60+ seconds to avoid Pixoo firmware bugs
- **Network**: Place Pixoo close to router for better connectivity
- **Power**: Use USB power for stability vs battery
- **Brightness**: Lower brightness extends device lifespan

## 🆘 Support

If you encounter issues:

1. Check this README's troubleshooting section
2. Enable debug mode with `--debug`
3. Check the [pixoo library](https://github.com/SomethingWithComputers/pixoo) for known issues
4. Create an issue in this repository

---

**Enjoy displaying time on your Pixoo 64! 🕐✨**

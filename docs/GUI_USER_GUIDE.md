# Pixoomat GUI User Guide

This guide explains how to use the Pixoomat compact graphical user interface for designing custom layouts for your Pixoo device.

## Getting Started

### Launching the GUI

```bash
python main.py --use-gui
```

The compact GUI will open with a responsive, three-pane layout optimized for screen space and accessibility.

## Interface Layout

The compact GUI features a modern, space-efficient design with three main areas:

- **Horizontal Toolbar**: Quick access to frequently used functions
- **Three-Pane Layout**: Left panel, center canvas, and right panel with horizontal splitters
- **Status Bar**: Zoom controls and status information at the bottom

### Main Interface Components

- **Left Panel**: Collapsible widget palette with grid-based widget selection
- **Center**: Dynamic canvas with scrollbars and zoom controls
- **Right Panel**: Tabbed property editor and device management
- **Horizontal Toolbar**: Consolidated controls for common actions

## Adding Widgets

### Built-in Widgets

1. **Clock Widget**: Displays the current time

   - Supports 12/24 hour formats
   - Customizable colors and font size
   - Optional seconds display

2. **Weather Widget**: Shows weather information
   - Displays temperature and conditions
   - Automatic location detection
   - Celsius/Fahrenheit support

### Plugin Widgets

Additional widgets available through the plugin system:

1. **Simple Text Widget**: Display custom text

   - Configurable text content
   - Color and font size options
   - Background color support

2. **Progress Bar Widget**: Visual progress indicator
   - Adjustable progress value
   - Customizable colors
   - Optional percentage display

## Widget Palette

The widget palette features a compact grid layout with visual icons:

- **Grid Layout**: 3-column grid for efficient space usage
- **Visual Icons**: Each widget has an icon and descriptive name
- **Tooltips**: Hover over widgets for descriptions
- **Active Widget List**: Compact list showing widgets in current layout
- **Widget Controls**: Remove, Move Up, and Move Down buttons

### Adding Widgets

1. Click a widget button in the grid
2. The widget will appear at a random position on the canvas
3. Click and drag the widget to position it

## Property Panel

The property panel is organized into three tabs for better organization:

### Basic Tab

- Position (X, Y coordinates)
- Size (Width, Height)
- Widget-specific basic properties
- Visibility toggle

### Appearance Tab

- Text color with RGB sliders
- Background color
- Font size controls
- Visual styling options

### Advanced Tab

- Z-index layering
- Update intervals
- Widget-specific advanced options
- Performance settings

#### Compact Mode Toggle

- Switch between compact and full property layouts
- Compact mode: Position and size in a single row
- Full mode: Separate sections for each property group

## Device Panel

The device panel provides consolidated device management:

- **Device Selector**: Dropdown with discovered devices
- **Manual IP Entry**: Direct IP address input
- **Connection Status**: Visual indicator (green/orange/red)
- **Compact Toolbar**: Connection and apply controls

### Device Connection

#### Automatic Discovery

1. Click "🔍 Discover" button
2. Wait for device discovery
3. Select device from dropdown list
4. Click "🔌 Connect"

#### Manual Connection

1. Enter IP address in the manual entry field
2. Set port and screen size if needed
3. Click "🔌 Connect"

## Canvas and Navigation

### Dynamic Canvas

- **Responsive Sizing**: Canvas adapts to window size
- **Centered Display**: Device preview is centered in available space
- **Scrollbars**: Navigate large layouts with scrollbars
- **Zoom Controls**: Zoom in/out with controls or mouse wheel

### Widget Selection and Manipulation

1. **Select**: Click on a widget in the canvas
2. **Move**: Click and drag to reposition
3. **Context Menu**: Right-click for additional options
4. **Arrow Keys**: Move selected widget pixel by pixel

## Keyboard Shortcuts

### File Operations

- **Ctrl+N**: New Layout
- **Ctrl+O**: Open Layout
- **Ctrl+S**: Save Layout
- **Ctrl+Shift+S**: Save Layout As

### Edit Operations

- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+D**: Duplicate Widget
- **Delete**: Delete Selected Widget
- **Ctrl+Home**: Bring Widget to Front
- **Ctrl+End**: Send Widget to Back

### View Operations

- **Ctrl++**: Zoom In
- **Ctrl+-**: Zoom Out
- **Ctrl+0**: Reset Zoom
- **F9**: Toggle Left Panel
- **F10**: Toggle Right Panel

### Navigation

- **Arrow Keys**: Move Selected Widget (1 pixel)
- **Mouse Wheel**: Zoom In/Out
- **Right Click**: Context Menu

### Other

- **F5**: Preview Layout
- **F1**: Show Keyboard Shortcuts Help

## Accessibility Features

### High Contrast Theme

- Toggle high contrast mode from View menu
- Improves visibility for users with visual impairments
- Black background with high-contrast colors

### Keyboard Navigation

- Full keyboard control of all interface elements
- Tab navigation between panels
- Keyboard shortcuts for all common operations

### Context Menus

- Right-click context menus on canvas
- Quick access to common widget operations
- Add widgets directly from context menu

## File Operations

### Saving Layouts

1. Go to **File → Save Layout** or press **Ctrl+S**
2. Choose a location and filename
3. Layouts are saved as `.json` files

### Loading Layouts

1. Go to **File → Open Layout** or press **Ctrl+O**
2. Select a previously saved `.json` file
3. The layout will be loaded and displayed

### Creating New Layouts

1. Go to **File → New Layout** or press **Ctrl+N**
2. Confirm to clear the current canvas
3. Start designing a new layout

## Zoom Controls

### Zoom Methods

- **Toolbar Buttons**: Use Zoom In/Out/Reset buttons
- **Status Bar**: Zoom controls in the bottom right corner
- **Keyboard Shortcuts**: Ctrl++ / Ctrl+- / Ctrl+0
- **Mouse Wheel**: Scroll to zoom in/out

### Zoom Range

- **Minimum**: 50% (0.5x)
- **Maximum**: 300% (3x)
- **Default**: 100% (1x)

## Panel Management

### Collapsible Panels

- **Left Panel**: Toggle with F9 or View menu
- **Right Panel**: Toggle with F10 or View menu
- **Remembered State**: Panels maintain their previous size when toggled

### Panel Weights

- **Left Panel**: Weight 1 (narrowest)
- **Center Canvas**: Weight 3 (widest)
- **Right Panel**: Weight 2 (medium)

## Advanced Features

### Undo/Redo System

- **Full History**: Tracks all widget operations
- **Unlimited Levels**: No limit on undo/redo operations
- **Operation Names**: Descriptive names for each operation

### Widget Layering

- **Z-Index Control**: Set widget stacking order
- **Visual Feedback**: Selected widget highlighted in yellow
- **Bring to Front/Send to Back**: Quick layering controls

### RGB Color Editors

- **Compact Mode**: Horizontal RGB sliders
- **Full Mode**: RGB spinboxes
- **Real-time Preview**: Colors update immediately
- **Value Display**: Shows RGB values (0-255)

## Tips and Best Practices

### Layout Design

1. **Start Simple**: Add essential widgets first
2. **Use Grid**: Leverage the widget grid for organized layouts
3. **Check Boundaries**: Ensure widgets don't exceed screen edges
4. **Test on Device**: Preview on actual Pixoo hardware
5. **Use Compact Mode**: Save space with compact property panels

### Performance

1. **Limit Updates**: Don't set too frequent update intervals
2. **Optimize Layout**: Avoid overlapping transparent widgets
3. **Use Appropriate Sizes**: Match widget size to content
4. **Toggle Panels**: Hide unused panels for more canvas space

### Troubleshooting

#### Common Issues

1. **Widget Not Visible**

   - Check if widget is outside screen boundaries
   - Verify Z-index layering
   - Ensure widget is not hidden behind others
   - Check visibility toggle in property panel

2. **Connection Problems**

   - Verify device is on same WiFi network
   - Check IP address and port
   - Try device discovery
   - Check visual status indicator

3. **Layout Not Saving**

   - Check file permissions
   - Ensure directory exists
   - Verify filename is valid

4. **Zoom Issues**
   - Use reset zoom button (Ctrl+0)
   - Check zoom level in status bar
   - Try mouse wheel zoom

#### Error Messages

- **"Device Not Found"**: Check network connection and IP
- **"Widget Outside Bounds"**: Move widget within screen area
- **"Connection Failed"**: Verify device is powered and connected
- **"Invalid Property"**: Check property value ranges

## Integration with CLI

The GUI works alongside the command-line interface:

- Layouts created in GUI can be used with CLI
- CLI settings affect GUI defaults
- Both share the same configuration files
- Use `--layout-config` to load GUI layouts in CLI mode

## Extending Pixoomat

For developers interested in creating custom widgets, see the [Widget Development Guide](WIDGET_DEVELOPMENT.md).

The plugin system allows you to:

- Create new widget types
- Add custom properties
- Integrate external data sources
- Share widgets with the community
- Use the compact grid layout for custom widgets

## Support

For additional help:

1. Press **F1** for keyboard shortcuts
2. Check the troubleshooting section above
3. Review the widget development documentation
4. Test with different configurations
5. Report issues with detailed error information

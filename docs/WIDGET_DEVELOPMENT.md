# Widget Development Guide

This guide explains how to create custom widgets for Pixoomat using the plugin system.

## 📖 Related Documentation

- **[README.md](../README.md)** - Main project documentation with quick start guide and configuration options
- **[AGENTS.md](AGENTS.md)** - Agent-specific information and development patterns
- **[WIDGET_DEVELOPMENT.md](WIDGET_DEVELOPMENT.md)** - This file - Comprehensive widget development guide

## Overview

Pixoomat supports extensible widgets through a plugin system. Custom widgets can be created as Python modules and dynamically loaded into the application.

## Available Widgets

Pixoomat includes 7 built-in widgets:

1. **ClockWidget**: Displays current time in 12/24 hour formats with optional seconds indicator
2. **WeatherWidget**: Shows current temperature with Celsius/Fahrenheit support from Open-Meteo API
3. **DateWidget**: Configurable date display with day of week and multiple format options
4. **CountdownWidget**: Countdown to specific date/time with real-time updates every second
5. **ProgressBarWidget**: Visual progress indicators with customizable colors and fill patterns
6. **SimpleTextWidget**: Custom text display with font size, color, and content options
7. **SystemStatsWidget**: CPU, memory, and disk usage monitoring using psutil library

Each widget supports position, size, configuration properties, and serialization for layout persistence.

## Widget Architecture

### Base Widget Class

All widgets inherit from `BaseWidget` which provides:

- Position and size management
- Property system for configuration
- Update interval management
- Serialization support
- Abstract methods for rendering

### Required Methods

When creating a custom widget, you must implement these abstract methods:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class BaseWidget(ABC):
    @abstractmethod
    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """Return default (width, height) for given screen size."""
        pass

    @abstractmethod
    def get_render_data(self) -> Dict[str, Any]:
        """Return data needed for rendering this widget."""
        pass
```

## Creating a Plugin

### Step 1: Create Widget Class

```python
from typing import Dict, Any, Tuple
from base_widget import BaseWidget
from plugin_system import WidgetPlugin, WidgetMetadata

class MyCustomWidget(BaseWidget):
    def __init__(self, x: int = 0, y: int = 0,
                 custom_property: str = "default", **kwargs):
        super().__init__(x, y, **kwargs)
        self.custom_property = custom_property

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        # Scale based on screen size (16, 32, or 64)
        scale_factor = screen_size / 64.0
        return (int(50 * scale_factor), int(20 * scale_factor))

    def get_render_data(self) -> Dict[str, Any]:
        return {
            "type": "custom",
            "custom_property": self.custom_property,
            "position": (self.x, self.y),
            "size": (self.width, self.height)
        }

    def render(self, image: Image.Image) -> Image.Image:
        # Implement actual rendering here
        # Use PIL (Pillow) to draw on the image
        pass

    def get_property_schema(self) -> Dict[str, Any]:
        """Define configurable properties for the GUI."""
        return {
            "custom_property": {
                "type": "string",
                "label": "Custom Property",
                "default": "default",
                "description": "Description of this property"
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize widget for saving."""
        return {
            "type": "MyCustom",
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "custom_property": self.custom_property
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MyCustomWidget':
        """Create widget from saved data."""
        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            width=data.get("width"),
            height=data.get("height"),
            custom_property=data.get("custom_property", "default")
        )
```

### Step 2: Create Plugin Class

```python
class MyCustomPlugin(WidgetPlugin):
    @property
    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            name="MyCustom",
            description="Description of your custom widget",
            version="1.0.0",
            author="Your Name",
            category="Custom",
            dependencies=[]  # List any required packages
        )

    def create_widget(self, **kwargs) -> MyCustomWidget:
        """Create widget instance."""
        return MyCustomWidget(**kwargs)

    def get_property_schema(self) -> Dict[str, Any]:
        """Return property schema for configuration UI."""
        widget = MyCustomWidget()
        return widget.get_property_schema()
```

### Step 3: Install Plugin

1. Create a Python file in `widgets/plugins/` directory
2. Name it descriptively (e.g., `my_custom_widget.py`)
3. The plugin will be automatically discovered on next startup

## Property Schema

The property schema defines how widget properties appear in the GUI:

### Supported Property Types

- **string**: Text input
- **integer**: Number input with min/max constraints
- **float**: Decimal number input with min/max/step constraints
- **boolean**: Checkbox
- **color**: RGB color picker
- **select**: Single-choice dropdown with predefined options
- **multiselect**: Multi-choice dropdown with predefined options
- **checkbox**: Alternative to boolean for checkbox UI

### Advanced Property Types

#### Select Properties

Used for single-choice selections from predefined options:

```python
"temperature_unit": {
    "type": "select",
    "label": "Temperature Unit",
    "options": ["C", "F"],
    "default": "C"
}
```

#### Multiselect Properties

Used for multi-choice selections from predefined options:

```python
"metrics": {
    "type": "multiselect",
    "label": "Metrics to Display",
    "default": ["CPU", "Memory", "Disk"],
    "options": ["CPU", "Memory", "Disk"],
    "description": "Select which system metrics to display"
}
```

#### Checkbox Properties

Alternative to boolean for better UI consistency:

```python
"show_icon": {
    "type": "checkbox",
    "default": True,
    "label": "Show Weather Icon"
}
```

### Schema Format

```python
{
    "property_name": {
        "type": "string|integer|float|boolean|color",
        "label": "Display Name",
        "default": default_value,
        "min": minimum_value,        # For integer/float
        "max": maximum_value,        # For integer/float
        "step": step_value,          # For float
        "description": "Help text"
    }
}
```

## Example: Simple Text Widget

Here's a complete example from the codebase:

```python
class SimpleTextWidget(BaseWidget):
    def __init__(self, x: int = 0, y: int = 0,
                 text: str = "Hello", color: Tuple[int, int, int] = (255, 255, 255),
                 font_size: int = 12):
        super().__init__(x, y)
        self.text = text
        self.color = color
        self.font_size = font_size
        self._calculate_dimensions()

    def _calculate_dimensions(self):
        """Calculate widget dimensions based on text and font."""
        self.width = max(50, len(self.text) * 6)
        self.height = max(15, self.font_size)

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        scale_factor = screen_size / 64.0
        return (50, 12)

    def get_render_data(self) -> Dict[str, Any]:
        return {
            "type": "text",
            "text": self.text,
            "color": self.color,
            "position": (self.x, self.y),
            "size": (self.width, self.height)
        }

    def render(self, image: Image.Image) -> Image.Image:
        draw = ImageDraw.Draw(image)
        draw.text((self.x, self.y), self.text, fill=self.color)
        return image

    def get_property_schema(self) -> Dict[str, Any]:
        return {
            "text": {
                "type": "string",
                "label": "Text",
                "default": "Hello"
            },
            "color": {
                "type": "color",
                "label": "Text Color",
                "default": (255, 255, 255)
            },
            "font_size": {
                "type": "integer",
                "label": "Font Size",
                "default": 12,
                "min": 8,
                "max": 32
            }
        }
```

## Best Practices

1. **Screen Size Awareness**: Always scale widgets based on screen size
2. **Property Validation**: Validate property values and provide sensible defaults
3. **Error Handling**: Handle rendering errors gracefully
4. **Performance**: Keep rendering efficient for small displays
5. **Documentation**: Provide clear descriptions for all properties
6. **Testing**: Test widgets with different screen sizes and property values

## Testing Your Widget

Create a test script to verify your widget:

```python
from widgets.plugin_system import get_plugin_manager

def test_my_widget():
    plugin_manager = get_plugin_manager()

    # Create widget
    widget = plugin_manager.create_widget("MyCustom",
                                      custom_property="test")

    # Test basic properties
    assert widget.x == 0
    assert widget.y == 0
    assert widget.custom_property == "test"

    # Test serialization
    data = widget.to_dict()
    restored = widget.__class__.from_dict(data)
    assert restored.custom_property == widget.custom_property

    print("Widget tests passed!")

if __name__ == "__main__":
    test_my_widget()
```

## Distribution

To share your widget:

1. Package your plugin file
2. Include installation instructions
3. Provide example configurations
4. Document any dependencies
5. Test on different screen sizes

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure plugin files are in the correct directory
2. **Missing Methods**: Implement all required abstract methods
3. **Property Schema**: Ensure schema uses correct types
4. **Screen Scaling**: Test on different screen sizes

### Debugging

Enable debug mode to see plugin loading information:

```bash
python main.py --debug --use-gui
```

This will show plugin loading errors and registration status.

## Screen Size Scaling

### Scaling Principles

All widgets must properly scale based on the target screen size (16, 32, or 64 pixels). The recommended approach is to use a scale factor relative to the standard 64px screen:

```python
def get_default_size(self, screen_size: int) -> Tuple[int, int]:
    scale_factor = screen_size / 64.0

    # Base dimensions for 64px screen
    base_width = 50
    base_height = 20

    # Apply scaling with minimum constraints
    width = max(int(base_width * scale_factor), 20)
    height = max(int(base_height * scale_factor), 10)

    return (width, height)
```

### Scaling Patterns from Existing Widgets

**Text-Based Widgets** (Clock, Date, Simple Text):

- Scale based on character count and font size
- Account for different time formats (12h vs 24h)
- Ensure minimum readability on small screens

```python
# Clock widget example
def get_default_size(self, screen_size: int) -> Tuple[int, int]:
    time_format = self.get_property('time_format', '24')
    show_seconds = self.get_property('show_seconds', False)

    if time_format == '12':
        text_length = 11 if show_seconds else 8
    else:
        text_length = 8 if show_seconds else 5

    font_size = self.get_property('font_size', 4)
    scale_factor = screen_size / 64.0
    width = min(text_length * font_size, screen_size)
    height = min(font_size + 2, screen_size)

    return (width, height)
```

**Visual Widgets** (Progress Bar, System Stats):

- Scale based on visual elements and spacing
- Maintain aspect ratios for visual consistency
- Adjust spacing and padding appropriately

```python
# Progress bar example
def get_default_size(self, screen_size: int) -> Tuple[int, int]:
    scale_factor = screen_size / 64.0
    default_width = int(80 * scale_factor)
    default_height = int(8 * scale_factor)
    return (default_width, default_height)
```

**Dynamic Widgets** (Countdown):

- Account for multi-line text displays
- Scale based on expected content length
- Ensure countdown numbers remain readable

### Minimum Size Constraints

- **16px screens**: Minimum 10px width, 8px height
- **32px screens**: Minimum 20px width, 12px height
- **64px screens**: Minimum 30px width, 15px height

### Content-Aware Scaling

Some widgets should scale based on content rather than just screen size:

```python
# Simple text widget with content-aware sizing
def _calculate_dimensions(self):
    text = self.get_property('text', 'Hello')
    font_size = self.get_property('font_size', 12)

    # Estimate text dimensions
    char_width = font_size * 0.6
    char_height = font_size

    self.width = max(50, len(text) * char_width)
    self.height = max(15, font_size)
```

## Update Interval Best Practices

### Recommended Update Intervals

**High-Frequency Updates (1-5 seconds)**:

- CountdownWidget: 1 second for accurate countdown
- SystemStatsWidget: 5 seconds for responsive system monitoring

**Medium-Frequency Updates (30-60 seconds)**:

- ClockWidget: 60 seconds (1 minute) for time display
- DateWidget: 60 seconds to ensure date changes at midnight

**Low-Frequency Updates (5-30 minutes)**:

- WeatherWidget: 1800 seconds (30 minutes) to respect API limits
- ProgressBarWidget: Depends on use case (typically 60 seconds)

### Update Interval Guidelines

1. **Balance responsiveness with performance**

   - Avoid excessive updates that drain device resources
   - Ensure critical data updates in real-time when needed

2. **Consider data source limitations**

   - Weather APIs often have rate limits
   - System statistics should not poll too frequently
   - Time/date updates can be less frequent

3. **Screen size considerations**

   - Smaller screens may need more frequent updates due to limited content
   - Larger screens can afford longer intervals for static content

4. **User experience expectations**
   - Countdown timers expect real-time updates
   - Clock displays should update at least every minute
   - Weather information is typically expected to be current within 10-15 minutes

### Dynamic Interval Adjustment

Some widgets can implement dynamic interval adjustment:

```python
# System stats widget with dynamic interval
def __init__(self, ..., update_interval: int = 5, ...):
    self.update_interval = update_interval
    # Adjust based on selected metrics
    if 'CPU' in self.get_property('metrics', []):
        self.update_interval = min(self.update_interval, 3)
```

## Error Handling Patterns

### Graceful Degradation

All widgets should handle errors gracefully and continue functioning:

```python
def get_system_stats(self) -> Dict[str, float]:
    """Get current system statistics with error handling."""
    stats = {}

    try:
        # CPU usage
        stats['cpu'] = psutil.cpu_percent(interval=0.1)

        # Memory usage
        memory = psutil.virtual_memory()
        stats['memory'] = memory.percent

        # Disk usage
        disk = psutil.disk_usage('/')
        stats['disk'] = (disk.used / disk.total) * 100

    except Exception as e:
        # Return default values if data unavailable
        if 'cpu' not in stats:
            stats['cpu'] = 0.0
        if 'memory' not in stats:
            stats['memory'] = 0.0
        if 'disk' not in stats:
            stats['disk'] = 0.0

    return stats
```

### Input Validation

Validate user input and provide meaningful error messages:

```python
def validate(self) -> List[str]:
    """Validate widget configuration."""
    errors = super().validate()

    # Validate metrics selection
    metrics = self.get_property('metrics', ['CPU', 'Memory', 'Disk'])
    if not metrics:
        errors.append("At least one metric must be selected")

    # Validate color format
    color = self.get_property('color', (144, 238, 144))
    if (len(color) != 3 or
        any(not isinstance(c, int) or c < 0 or c > 255 for c in color)):
        errors.append("Color must be RGB values between 0 and 255")

    return errors
```

### Date/Time Parsing

Handle invalid date formats gracefully:

```python
def get_render_data(self) -> Dict[str, Any]:
    target_date_str = self.get_property('target_date', '2024-01-01 00:00:00')

    try:
        target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Show error message for invalid format
        return {
            "type": "text",
            "text": "Invalid date format",
            "color": (255, 0, 0),  # Red for error
            "position": (self.x, self.y),
            "size": (self.width, self.height)
        }
```

### Network/External Dependencies

Handle external service failures:

```python
def get_weather_data(self) -> Optional[Dict[str, Any]]:
    """Get weather data with error handling."""
    try:
        # Attempt to fetch weather data
        return self._fetch_weather_from_api()
    except Exception as e:
        # Log error but continue with cached/placeholder data
        print(f"Weather fetch failed: {e}")
        return None
```

## Rendering Considerations

### Small Display Challenges

**Font Handling**:

- Use small, readable fonts (2-8px range for 64px screens)
- Implement fallback rendering for missing fonts
- Consider pixel-perfect fonts for better readability

```python
def render(self, image: Image.Image) -> Image.Image:
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.load_default()
    except:
        font = None  # Fallback to default text rendering

    if font:
        draw.text((self.x, self.y), self.text, fill=self.color, font=font)
    else:
        draw.text((self.x, self.y), self.text, fill=self.color)
```

**Color Management**:

- Use high-contrast colors for better visibility
- Implement color validation and clamping
- Consider color accessibility

```python
# Ensure colors are valid RGB tuples
def clamp_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return tuple(max(0, min(255, int(c))) for c in color)
```

**Text Layout**:

- Account for text wrapping on small displays
- Use abbreviations for long text
- Implement multi-line text support where needed

```python
# Multi-line text handling
def format_multiline_text(self, text: str, max_width: int) -> List[str]:
    """Split text into multiple lines based on width constraints."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        if len(test_line) * 6 <= max_width:  # Approximate character width
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Word is too long, force split
                lines.append(word[:max_width//6])
                current_line = [word[max_width//6:]]

    if current_line:
        lines.append(' '.join(current_line))

    return lines
```

**Performance Optimization**:

- Minimize rendering operations
- Cache expensive calculations
- Use efficient drawing methods

```python
# Cache font loading
class CachedFontWidget(BaseWidget):
    _font_cache = {}

    def _get_font(self, font_size: int):
        if font_size not in self._font_cache:
            try:
                self._font_cache[font_size] = ImageFont.truetype("arial.ttf", font_size)
            except:
                self._font_cache[font_size] = ImageFont.load_default()
        return self._font_cache[font_size]
```

### Positioning Strategies

**Centered Text**:

```python
def get_centered_position(self, text: str, font_size: int) -> Tuple[int, int]:
    """Calculate centered position for text."""
    text_width = len(text) * font_size * 0.6
    x = (self.width - text_width) // 2
    y = (self.height - font_size) // 2
    return (int(x), int(y))
```

**Dynamic Widget Sizing**:

```python
def adjust_widget_size(self, content: str) -> Tuple[int, int]:
    """Adjust widget size based on content."""
    # Calculate required size based on content
    content_width = len(content) * self.font_size * 0.6
    content_height = self.font_size

    # Ensure minimum size
    width = max(content_width, self.minimum_width)
    height = max(content_height, self.minimum_height)

    return (int(width), int(height))
```

## Testing Strategies

### Comprehensive Widget Testing

**Basic Functionality Tests**:

- Widget instantiation via plugin manager
- Direct instantiation with parameters
- Default property validation
- Position and size calculations

```python
def test_widget_creation():
    """Test widget creation through multiple methods."""
    # Test via plugin manager
    plugin_manager = get_plugin_manager()
    widget = plugin_manager.create_widget("Clock")
    assert widget is not None

    # Test direct instantiation
    direct_widget = ClockWidget(x=10, y=20)
    assert direct_widget.x == 10
    assert direct_widget.y == 20

    # Test default properties
    assert widget.get_property('time_format') == '24'
    assert widget.get_property('show_seconds') == False
```

**Rendering Tests**:

- Render data structure validation
- Image rendering without errors
- Text positioning and formatting
- Color handling

```python
def test_widget_rendering():
    """Test widget rendering functionality."""
    widget = ClockWidget()

    # Test render data structure
    render_data = widget.get_render_data()
    assert 'type' in render_data
    assert 'text' in render_data
    assert 'position' in render_data
    assert 'color' in render_data

    # Test actual rendering (if applicable)
    from PIL import Image
    test_image = Image.new('RGB', (64, 64), (0, 0, 0))
    result_image = widget.render(test_image)
    assert result_image is not None
```

**Serialization Tests**:

- Widget to dictionary conversion
- Dictionary to widget restoration
- Property preservation across serialization

```python
def test_widget_serialization():
    """Test widget serialization/deserialization."""
    widget = ClockWidget(x=15, y=25, width=100, height=30)
    widget.set_property('time_format', '12')
    widget.set_property('show_seconds', True)

    # Test serialization
    widget_dict = widget.to_dict()
    assert widget_dict['type'] == 'ClockWidget'
    assert widget_dict['x'] == 15
    assert widget_dict['y'] == 25
    assert 'properties' in widget_dict

    # Test deserialization
    restored_widget = ClockWidget.from_dict(widget_dict)
    assert restored_widget.x == 15
    assert restored_widget.y == 25
    assert restored_widget.get_property('time_format') == '12'
    assert restored_widget.get_property('show_seconds') == True
```

**Screen Size Scaling Tests**:

- Test default size calculations for different screen sizes
- Verify proper scaling behavior
- Ensure minimum size constraints

```python
def test_screen_scaling():
    """Test widget scaling across different screen sizes."""
    widget = ClockWidget()

    # Test different screen sizes
    size_16 = widget.get_default_size(16)
    size_32 = widget.get_default_size(32)
    size_64 = widget.get_default_size(64)

    # Verify scaling works correctly
    assert size_16[0] <= size_32[0] <= size_64[0]
    assert size_16[1] <= size_32[1] <= size_64[1]

    # Verify minimum sizes
    assert size_16[0] >= 10  # Minimum width for 16px screen
    assert size_16[1] >= 8   # Minimum height for 16px screen
```

**Error Handling Tests**:

- Invalid input handling
- Edge case scenarios
- Exception recovery

```python
def test_error_handling():
    """Test widget error handling."""
    # Test countdown widget with invalid date
    countdown = CountdownWidget()
    countdown.set_property('target_date', 'invalid-date')

    render_data = countdown.get_render_data()
    assert 'Invalid date format' in render_data['text']
    assert render_data['color'] == (255, 0, 0)  # Error color

    # Test system stats with no metrics
    stats = SystemStatsWidget()
    stats.set_property('metrics', [])

    errors = stats.validate()
    assert len(errors) > 0
    assert any('metric' in error.lower() for error in errors)
```

**Integration Tests**:

- Widget layout management
- Multiple widget interactions
- Real-world usage scenarios

```python
def test_widget_integration():
    """Test widget integration with layout system."""
    from layout_manager import LayoutManager

    layout = LayoutManager(64)

    # Add multiple widgets
    clock = ClockWidget(x=0, y=0)
    date = DateWidget(x=0, y=20)
    stats = SystemStatsWidget(x=40, y=0)

    layout.add_widget(clock)
    layout.add_widget(date)
    layout.add_widget(stats)

    # Test layout validation
    validation_errors = layout.validate_layout()
    assert len(validation_errors) == 0  # Should have no errors

    # Test render data generation
    render_data = layout.get_render_data()
    assert len(render_data['widgets']) == 3
```

### Performance Testing

**Update Interval Testing**:

- Verify update intervals are respected
- Test high-frequency updates don't cause issues
- Validate interval-based updates

```python
def test_update_intervals():
    """Test widget update intervals."""
    countdown = CountdownWidget()
    assert countdown.update_interval == 1  # Should update every second

    clock = ClockWidget()
    assert clock.update_interval == 60  # Should update every minute

    weather = WeatherWidget()
    assert weather.update_interval == 1800  # Should update every 30 minutes
```

**Memory Usage Testing**:

- Monitor memory usage during widget operations
- Test for memory leaks in long-running scenarios
- Verify proper cleanup

```python
def test_memory_usage():
    """Test widget memory usage."""
    import gc
    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    # Create and destroy multiple widgets
    for _ in range(100):
        widget = SystemStatsWidget()
        data = widget.get_render_data()

    # Force garbage collection
    gc.collect()
    final_memory = process.memory_info().rss

    # Memory increase should be minimal
    memory_increase = final_memory - initial_memory
    assert memory_increase < 1024 * 1024  # Less than 1MB increase
```

### Cross-Platform Testing

**Different Environments**:

- Test on different operating systems
- Verify behavior with missing dependencies
- Test with various screen configurations

```python
def test_cross_platform():
    """Test widget behavior across different platforms."""
    # Test with missing psutil (for non-system widgets)
    try:
        import psutil
        psutil_available = True
    except ImportError:
        psutil_available = False

    # System stats should handle missing psutil gracefully
    stats = SystemStatsWidget()
    system_data = stats.get_system_stats()
    assert isinstance(system_data, dict)
    assert 'cpu' in system_data
    assert 'memory' in system_data
    assert 'disk' in system_data
```

## Lessons Learned

### Key Insights from Widget Development

### 1. Property Schema Evolution

- Started with basic types (string, integer, boolean, color)
- Discovered need for advanced types (select, multiselect, checkbox)
- Property schemas should be comprehensive but not overly complex
- Default values should be sensible and useful out-of-the-box

### 2. Screen Size Scaling Challenges

- Scaling is not linear - different widgets need different approaches
- Content-aware scaling often works better than simple multiplication
- Minimum size constraints are crucial for usability
- Text-based widgets need special consideration for character width

### 3. Update Interval Strategies

- Not all widgets need the same update frequency
- High-frequency updates should be used sparingly
- External API calls should be cached and rate-limited
- User expectations vary by widget type

### 4. Error Handling Patterns

- Graceful degradation is more important than perfect functionality
- Input validation should happen early and provide clear feedback
- External dependencies should fail safely
- Error states should be visually distinct

### 5. Rendering Optimization

- Small displays require careful font and color management
- Caching expensive operations (like font loading) improves performance
- Multi-line text support is essential for complex content
- Positioning algorithms need to be robust

### 6. Testing Best Practices

- Comprehensive testing requires multiple approaches
- Serialization/deserialization testing is critical for persistence
- Error handling tests should cover edge cases
- Performance testing ensures widgets don't impact system responsiveness

### 7. Plugin System Benefits

- Dynamic loading enables easy extension
- Plugin architecture encourages consistent interfaces
- Metadata helps with organization and discovery
- Versioning allows for backward compatibility

### 8. User Experience Considerations

- Defaults should work well for most users
- Configuration options should be intuitive
- Visual feedback helps users understand widget state
- Consistent styling across widgets improves usability

### Development Patterns to Avoid

### 1. Hardcoded Dimensions

- Always scale based on screen size
- Use relative sizing rather than absolute values
- Consider content-aware sizing for dynamic widgets

### 2. Inconsistent Error Handling

- Implement error handling consistently across all widgets
- Provide meaningful error messages
- Ensure widgets continue functioning even when data is unavailable

### 3. Neglecting Testing

- Test all widget functionality thoroughly
- Include edge cases and error scenarios
- Verify serialization works correctly
- Test across different screen sizes

### 4. Over-Engineering

- Keep widgets focused on their core functionality
- Avoid adding unnecessary complexity
- Balance features with maintainability

### 5. Ignoring Performance

- Optimize rendering for small displays
- Cache expensive operations
- Respect update intervals and API rate limits

## Dependencies

When developing widgets, ensure you have the required dependencies:

- **Pillow** (PIL): Required for all widget rendering - install with `pip install Pillow`
- **psutil**: Required for SystemStatsWidget - install with `pip install psutil`
- Standard library modules: All other dependencies are included with Python

### Widget-Specific Dependencies

Some widgets may have additional dependencies:

```python
# In your plugin metadata, specify dependencies
class MyCustomPlugin(WidgetPlugin):
    @property
    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            name="MyCustom",
            description="Description of your custom widget",
            version="1.0.0",
            author="Your Name",
            category="Custom",
            dependencies=[]  # Add any required packages here
        )
```

These lessons learned provide valuable guidance for future widget development, helping create more robust, user-friendly, and maintainable widgets.

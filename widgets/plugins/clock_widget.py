"""
Clock widget implementation for Pixoomat
Displays the current time in various formats
"""
import datetime
from typing import Dict, Any, Tuple, Optional

from widgets.base_widget import BaseWidget
from widgets.plugin_system import WidgetPlugin, WidgetMetadata


class ClockWidget(BaseWidget):
    """Widget for displaying current time"""

    def __init__(self, x: int = 0, y: int = 0, width: Optional[int] = None, height: Optional[int] = None, screen_size: int = 64):
        """
        Initialize clock widget

        Args:
            x: X position on screen
            y: Y position on screen
            width: Widget width in pixels (None for default)
            height: Widget height in pixels (None for default)
            screen_size: Screen size in pixels
        """
        super().__init__(x, y, width, height, screen_size)

    def _init_properties(self):
        """Initialize clock-specific properties"""
        self.set_property('time_format', '24')  # '12' or '24'
        self.set_property('show_seconds', False)
        self.set_property('font_size', 4)  # Pixel font size estimate
        self.set_property('text_color', (255, 255, 255))  # RGB color
        self.set_property('background_color', None)  # None for transparent

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """
        Get default size for clock widget based on screen size

        Args:
            screen_size: Screen size in pixels

        Returns:
            Default (width, height) tuple
        """
        # Time text is typically 8 chars wide for 24h format (HH:MM:SS) or 11 chars for 12h (HH:MM AM/PM)
        time_format = self.get_property('time_format', '24')
        show_seconds = self.get_property('show_seconds', False)

        if time_format == '12':
            text_length = 11 if show_seconds else 8  # HH:MM AM/PM or HH:MM:SS AM/PM
        else:
            text_length = 8 if show_seconds else 5  # HH:MM:SS or HH:MM

        font_size = self.get_property('font_size', 4)
        width = text_length * font_size
        height = font_size + 2  # Add some padding

        return (min(width, screen_size), min(height, screen_size))

    def format_time(self) -> str:
        """
        Format current time according to widget settings

        Returns:
            Formatted time string
        """
        now = datetime.datetime.now()
        time_format = self.get_property('time_format', '24')
        show_seconds = self.get_property('show_seconds', False)

        if time_format == '12':
            if show_seconds:
                return now.strftime("%I:%M:%S %p")
            else:
                return now.strftime("%I:%M %p")
        else:  # 24-hour format
            if show_seconds:
                return now.strftime("%H:%M:%S")
            else:
                return now.strftime("%H:%M")

    def get_render_data(self) -> Dict[str, Any]:
        """
        Get data needed for rendering the clock widget

        Returns:
            Dictionary containing render information
        """
        time_text = self.format_time()
        text_color = self.get_property('text_color', (255, 255, 255))
        background_color = self.get_property('background_color', None)

        render_data = {
            'type': 'text',
            'text': time_text,
            'x': self.x,
            'y': self.y,
            'color': text_color,
            'background_color': background_color
        }

        return render_data

    def validate(self) -> list[str]:
        """
        Validate clock widget configuration

        Returns:
            List of validation error messages
        """
        errors = super().validate()

        time_format = self.get_property('time_format', '24')
        if time_format not in ['12', '24']:
            errors.append("Time format must be '12' or '24'")

        text_color = self.get_property('text_color', (255, 255, 255))
        if (len(text_color) != 3 or
            any(not isinstance(c, int) or c < 0 or c > 255 for c in text_color)):
            errors.append("Text color must be RGB values between 0 and 255")

        if self.get_property('show_seconds') and self.update_interval > 1:
            errors.append("Update interval should be 1 second or less when showing seconds")

        return errors

    def get_property_schema(self) -> Dict[str, Any]:
        """Get property schema for clock widget"""
        return {
            'time_format': {
                'type': 'string',
                'label': 'Time Format',
                'default': '24'
            },
            'show_seconds': {
                'type': 'boolean',
                'label': 'Show Seconds',
                'default': False
            },
            'font_size': {
                'type': 'integer',
                'label': 'Font Size',
                'min': 2,
                'max': 8,
                'default': 4
            },
            'text_color': {
                'type': 'color',
                'label': 'Text Color',
                'default': (255, 255, 255)
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert clock widget to dictionary representation"""
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClockWidget':
        """Create clock widget from dictionary representation"""
        # Extract properties that are part of the BaseWidget constructor
        init_kwargs = {
            'x': data.get('x', 0),
            'y': data.get('y', 0),
            'width': data.get('width'),
            'height': data.get('height'),
            'screen_size': data.get('screen_size', 64) # Assuming screen_size is passed or has a default
        }

        widget = cls(**init_kwargs)

        # Restore BaseWidget attributes
        widget.visible = data.get('visible', True)
        widget.z_index = data.get('z_index', 0)
        widget.update_interval = data.get('update_interval', 60)
        widget.properties = data.get('properties', widget.properties)

        return widget


class ClockWidgetPlugin(WidgetPlugin):
    """Plugin for the ClockWidget."""

    @property
    def metadata(self) -> WidgetMetadata:
        """Return metadata for this plugin."""
        return WidgetMetadata(
            name="Clock",
            description="Displays the current time.",
            version="1.0.0",
            author="Pixoomat",
            category="Time"
        )

    def create_widget(self, **kwargs) -> ClockWidget:
        """Create an instance of the ClockWidget."""
        return ClockWidget(**kwargs)

    def get_property_schema(self) -> Dict[str, Any]:
        """Return the property schema for the ClockWidget."""
        return ClockWidget().get_property_schema()
"""
Date Widget Plugin for Pixoomat
Displays the current date in a configurable format.
"""
import datetime
from typing import Dict, Any, Tuple

from widgets.base_widget import BaseWidget
from widgets.plugin_system import WidgetPlugin, WidgetMetadata


class DateWidget(BaseWidget):
    """A widget to display the current date."""

    def __init__(self, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None, screen_size: int = 64):
        super().__init__(x, y, width, height, screen_size)
        # Set a shorter update interval to ensure the date changes at midnight
        self.update_interval = 60

    def _init_properties(self):
        """Initialize default properties for the DateWidget."""
        self.properties = {
            'format': '%m/%d/%y',
            'color': (255, 255, 255),
            'show_day_of_week': True
        }

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """Calculate a default size based on the screen size."""
        scale_factor = screen_size / 64.0
        # Estimate width based on a typical date format like "MM/DD/YY" or "Day"
        # and height based on a single line of text.
        return (int(48 * scale_factor), int(12 * scale_factor))

    def get_render_data(self) -> Dict[str, Any]:
        """Prepare the data needed to render the date."""
        now = datetime.datetime.now()
        date_format = self.get_property('format', '%m/%d/%y')
        date_str = now.strftime(date_format)

        full_text = date_str
        if self.get_property('show_day_of_week', True):
            day_of_week = now.strftime('%A')
            # Add a separator if both are shown
            full_text = f"{day_of_week} {date_str}"

        return {
            "type": "text",
            "text": full_text,
            "color": self.get_property('color', (255, 255, 255)),
            "position": (self.x, self.y),
            "size": (self.width, self.height)
        }

    def get_property_schema(self) -> Dict[str, Any]:
        """Define the configurable properties for the GUI."""
        return {
            'format': {
                'type': 'string',
                'label': 'Date Format',
                'default': '%m/%d/%y',
                'description': 'Date format using strftime codes (e.g., %Y-%m-%d, %d.%m.%Y)'
            },
            'color': {
                'type': 'color',
                'label': 'Text Color',
                'default': (255, 255, 255),
                'description': 'The color of the date text.'
            },
            'show_day_of_week': {
                'type': 'boolean',
                'label': 'Show Day of Week',
                'default': True,
                'description': 'Whether to display the day of the week (e.g., "Monday").'
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the widget's state to a dictionary."""
        data = super().to_dict()
        # Properties are already handled by the base class
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DateWidget':
        """Create a widget instance from a dictionary."""
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


class DateWidgetPlugin(WidgetPlugin):
    """Plugin for the DateWidget."""

    @property
    def metadata(self) -> WidgetMetadata:
        """Return metadata for this plugin."""
        return WidgetMetadata(
            name="Date",
            description="Displays the current date in a configurable format.",
            version="1.0.0",
            author="Pixoomat",
            category="Time"
        )

    def create_widget(self, **kwargs) -> DateWidget:
        """Create an instance of the DateWidget."""
        return DateWidget(**kwargs)

    def get_property_schema(self) -> Dict[str, Any]:
        """Return the property schema for the DateWidget."""
        return DateWidget().get_property_schema()
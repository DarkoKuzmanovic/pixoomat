"""
Countdown Widget Plugin for Pixoomat
Counts down to a specific date and time.
"""
import datetime
from typing import Dict, Any, Tuple

from widgets.base_widget import BaseWidget
from widgets.plugin_system import WidgetPlugin, WidgetMetadata


class CountdownWidget(BaseWidget):
    """A widget to display a countdown to a specific date and time."""

    def __init__(self, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None, screen_size: int = 64):
        super().__init__(x, y, width, height, screen_size)
        # Set update interval to 1 second for accurate countdown
        self.update_interval = 1

    def _init_properties(self):
        """Initialize default properties for the CountdownWidget."""
        # Default to New Year as a reasonable target date
        now = datetime.datetime.now()
        next_year = now.year + 1
        default_target = datetime.datetime(next_year, 1, 1, 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')

        self.properties = {
            'target_date': default_target,
            'label': 'Countdown',
            'color': (255, 255, 255)
        }

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """Calculate a default size based on the screen size."""
        scale_factor = screen_size / 64.0
        # Estimate size based on typical countdown display format
        # "Label" on one line and "DD:HH:MM:SS" on another
        return (int(50 * scale_factor), int(20 * scale_factor))

    def get_render_data(self) -> Dict[str, Any]:
        """Prepare the data needed to render the countdown."""
        target_date_str = self.get_property('target_date', '2024-01-01 00:00:00')
        label = self.get_property('label', 'Countdown')
        color = self.get_property('color', (255, 255, 255))

        try:
            target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # If parsing fails, show an error message
            return {
                "type": "text",
                "text": "Invalid date format",
                "color": (255, 0, 0),  # Red for error
                "position": (self.x, self.y),
                "size": (self.width, self.height)
            }

        now = datetime.datetime.now()
        if now >= target_date:
            # Countdown has reached zero
            countdown_text = "00:00:00:00"
        else:
            # Calculate time difference
            delta = target_date - now
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Format as DD:HH:MM:SS
            countdown_text = f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"

        # Combine label and countdown
        full_text = f"{label}\n{countdown_text}"

        return {
            "type": "text",
            "text": full_text,
            "color": color,
            "position": (self.x, self.y),
            "size": (self.width, self.height)
        }

    def get_property_schema(self) -> Dict[str, Any]:
        """Define the configurable properties for the GUI."""
        return {
            'target_date': {
                'type': 'string',
                'label': 'Target Date',
                'default': '2024-01-01 00:00:00',
                'description': 'Target date and time in YYYY-MM-DD HH:MM:SS format'
            },
            'label': {
                'type': 'string',
                'label': 'Label',
                'default': 'Countdown',
                'description': 'Label to display above the countdown'
            },
            'color': {
                'type': 'color',
                'label': 'Text Color',
                'default': (255, 255, 255),
                'description': 'The color of the countdown text'
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the widget's state to a dictionary."""
        data = super().to_dict()
        # Properties are already handled by the base class
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CountdownWidget':
        """Create a widget instance from a dictionary."""
        # Extract properties that are part of the BaseWidget constructor
        init_kwargs = {
            'x': data.get('x', 0),
            'y': data.get('y', 0),
            'width': data.get('width'),
            'height': data.get('height'),
            'screen_size': data.get('screen_size', 64)  # Assuming screen_size is passed or has a default
        }

        widget = cls(**init_kwargs)

        # Restore BaseWidget attributes
        widget.visible = data.get('visible', True)
        widget.z_index = data.get('z_index', 0)
        widget.update_interval = data.get('update_interval', 1)
        widget.properties = data.get('properties', widget.properties)

        return widget


class CountdownWidgetPlugin(WidgetPlugin):
    """Plugin for the CountdownWidget."""

    @property
    def metadata(self) -> WidgetMetadata:
        """Return metadata for this plugin."""
        return WidgetMetadata(
            name="Countdown",
            description="Counts down to a specific date and time.",
            version="1.0.0",
            author="Pixoomat",
            category="Time"
        )

    def create_widget(self, **kwargs) -> CountdownWidget:
        """Create an instance of the CountdownWidget."""
        return CountdownWidget(**kwargs)

    def get_property_schema(self) -> Dict[str, Any]:
        """Return the property schema for the CountdownWidget."""
        return CountdownWidget().get_property_schema()
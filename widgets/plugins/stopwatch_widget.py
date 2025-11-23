"""
Stopwatch Widget Plugin for Pixoomat
A simple stopwatch with start/stop/reset functionality.
"""
import datetime
from typing import Dict, Any, Tuple

from widgets.base_widget import BaseWidget
from widgets.plugin_system import WidgetPlugin, WidgetMetadata


class StopwatchWidget(BaseWidget):
    """A widget to display a stopwatch with start/stop/reset functionality."""

    def __init__(self, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None, screen_size: int = 64):
        super().__init__(x, y, width, height, screen_size)
        # Update interval will be managed dynamically based on state
        self.update_interval = 60  # Default to 60 seconds when not running

    def _init_properties(self):
        """Initialize default properties for the StopwatchWidget."""
        self.properties = {
            'state': 'stopped',  # 'stopped', 'running', 'reset'
            'start_time': None,  # ISO format string when running
            'elapsed_seconds': 0.0,  # Accumulated elapsed time in seconds
            'label': 'Stopwatch',
            'color': (255, 255, 255)
        }

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """Calculate a default size based on the screen size."""
        scale_factor = screen_size / 64.0
        # Estimate size for "Label" and "HH:MM:SS" format
        return (int(60 * scale_factor), int(20 * scale_factor))

    def get_render_data(self) -> Dict[str, Any]:
        """Prepare the data needed to render the stopwatch."""
        state = self.get_property('state', 'stopped')
        label = self.get_property('label', 'Stopwatch')
        color = self.get_property('color', (255, 255, 255))

        elapsed_seconds = self.get_property('elapsed_seconds', 0.0)

        if state == 'running':
            start_time_str = self.get_property('start_time')
            if not start_time_str:
                # Start the stopwatch
                self.properties['start_time'] = datetime.datetime.now().isoformat()
                start_time_str = self.properties['start_time']
            try:
                start_time = datetime.datetime.fromisoformat(start_time_str)
                now = datetime.datetime.now()
                current_elapsed = (now - start_time).total_seconds()
                total_elapsed = elapsed_seconds + current_elapsed
            except (ValueError, TypeError):
                total_elapsed = elapsed_seconds
            self.update_interval = 1  # Update every second when running
        elif state == 'stopped':
            total_elapsed = elapsed_seconds
            self.update_interval = 60  # Update less frequently when stopped
        elif state == 'reset':
            # Perform reset
            total_elapsed = 0.0
            self.properties['elapsed_seconds'] = 0.0
            self.properties['start_time'] = None
            self.properties['state'] = 'stopped'  # Change state to stopped after reset
            self.update_interval = 60
        else:
            total_elapsed = elapsed_seconds
            self.update_interval = 60

        elapsed_text = self.format_seconds(total_elapsed)

        # Combine label and elapsed time
        full_text = f"{label}\n{elapsed_text}"

        return {
            "type": "text",
            "text": full_text,
            "color": color,
            "position": (self.x, self.y),
            "size": (self.width, self.height)
        }

    def format_seconds(self, seconds: float) -> str:
        """Format seconds into HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def get_property_schema(self) -> Dict[str, Any]:
        """Define the configurable properties for the GUI."""
        return {
            'state': {
                'type': 'select',
                'label': 'State',
                'default': 'stopped',
                'options': ['stopped', 'running', 'reset'],
                'description': 'Current state of the stopwatch'
            },
            'label': {
                'type': 'string',
                'label': 'Label',
                'default': 'Stopwatch',
                'description': 'Label to display above the stopwatch'
            },
            'color': {
                'type': 'color',
                'label': 'Text Color',
                'default': (255, 255, 255),
                'description': 'The color of the stopwatch text'
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the widget's state to a dictionary."""
        data = super().to_dict()
        # Properties are already handled by the base class
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StopwatchWidget':
        """Create a widget instance from a dictionary."""
        # Extract properties that are part of the BaseWidget constructor
        init_kwargs = {
            'x': data.get('x', 0),
            'y': data.get('y', 0),
            'width': data.get('width'),
            'height': data.get('height'),
            'screen_size': data.get('screen_size', 64)
        }

        widget = cls(**init_kwargs)

        # Restore BaseWidget attributes
        widget.visible = data.get('visible', True)
        widget.z_index = data.get('z_index', 0)
        widget.update_interval = data.get('update_interval', 60)
        widget.properties = data.get('properties', widget.properties)

        return widget


class StopwatchWidgetPlugin(WidgetPlugin):
    """Plugin for the StopwatchWidget."""

    @property
    def metadata(self) -> WidgetMetadata:
        """Return metadata for this plugin."""
        return WidgetMetadata(
            name="Stopwatch",
            description="A simple stopwatch with start/stop/reset functionality.",
            version="1.0.0",
            author="Pixoomat",
            category="Utility"
        )

    def create_widget(self, **kwargs) -> StopwatchWidget:
        """Create an instance of the StopwatchWidget."""
        return StopwatchWidget(**kwargs)

    def get_property_schema(self) -> Dict[str, Any]:
        """Return the property schema for the StopwatchWidget."""
        return StopwatchWidget().get_property_schema()
"""
System Stats widget plugin for Pixoomat.

This plugin provides a widget that displays system CPU usage, memory usage,
and disk space percentage as simple bar graphs.
"""

from typing import Dict, Any, Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFont
import psutil
import os

from widgets.base_widget import BaseWidget
from widgets.plugin_system import WidgetPlugin, WidgetMetadata


class SystemStatsWidget(BaseWidget):
    """System statistics display widget."""

    def __init__(self, x: int = 0, y: int = 0,
                 metrics: Optional[List[str]] = None, update_interval: int = 5,
                 color: Tuple[int, int, int] = (144, 238, 144),  # Light green
                 width: Optional[int] = None, height: Optional[int] = None,
                 screen_size: int = 64):
        super().__init__(x, y, width, height, screen_size)

        # Set default metrics if not provided
        if metrics is None:
            metrics = ['CPU', 'Memory', 'Disk']

        # Set update interval and store properties
        self.update_interval = update_interval
        self.set_property('metrics', metrics)
        self.set_property('color', color)
        self.set_property('update_interval', update_interval)

    def _init_properties(self):
        """Initialize system stats widget properties."""
        self.set_property('metrics', ['CPU', 'Memory', 'Disk'])
        self.set_property('color', (144, 238, 144))  # Light green
        self.set_property('update_interval', 5)

    def get_system_stats(self) -> Dict[str, float]:
        """Get current system statistics."""
        stats = {}

        try:
            # CPU usage
            stats['cpu'] = psutil.cpu_percent(interval=0.1)

            # Memory usage
            memory = psutil.virtual_memory()
            stats['memory'] = memory.percent

            # Disk usage (root partition)
            disk = psutil.disk_usage('/')
            stats['disk'] = (disk.used / disk.total) * 100

        except Exception as e:
            # If we can't get system stats, return default values
            if 'cpu' not in stats:
                stats['cpu'] = 0.0
            if 'memory' not in stats:
                stats['memory'] = 0.0
            if 'disk' not in stats:
                stats['disk'] = 0.0

        return stats

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """Get default size for system stats widget based on screen size."""
        scale_factor = screen_size / 64.0

        # Each metric will take about 20px width + some spacing
        metrics = self.get_property('metrics', ['CPU', 'Memory', 'Disk'])
        num_metrics = len(metrics)

        width = max(int(60 * scale_factor), num_metrics * 20)
        height = max(int(30 * scale_factor), 15)

        return (width, height)

    def get_render_data(self) -> Dict[str, Any]:
        """Get data needed for rendering this widget."""
        stats = self.get_system_stats()
        metrics = self.get_property('metrics', ['CPU', 'Memory', 'Disk'])
        color = self.get_property('color', (144, 238, 144))

        # Filter stats to only include selected metrics
        filtered_stats = {}
        for metric in metrics:
            if metric.lower() == 'cpu':
                filtered_stats['CPU'] = stats['cpu']
            elif metric.lower() == 'memory':
                filtered_stats['Memory'] = stats['memory']
            elif metric.lower() == 'disk':
                filtered_stats['Disk'] = stats['disk']

        return {
            "type": "system_stats",
            "stats": filtered_stats,
            "color": color,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }

    def render(self, image: Image.Image) -> Image.Image:
        """Render the system stats widget on the image."""
        stats = self.get_system_stats()
        metrics = self.get_property('metrics', ['CPU', 'Memory', 'Disk'])
        color = self.get_property('color', (144, 238, 144))

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Set up bar dimensions
        bar_height = max(3, int(self.height / (len(metrics) + 1)))
        bar_spacing = bar_height + 2
        font_size = max(6, int(bar_height * 0.8))

        try:
            font = ImageFont.load_default()
        except:
            font = None

        y_offset = self.y

        for metric in metrics:
            # Get the appropriate stat value
            if metric.lower() == 'cpu':
                value = stats['cpu']
                label = 'CPU'
            elif metric.lower() == 'memory':
                value = stats['memory']
                label = 'MEM'
            elif metric.lower() == 'disk':
                value = stats['disk']
                label = 'DSK'
            else:
                continue

            # Draw label
            if font:
                draw.text((self.x, y_offset), f"{label}:", fill=color, font=font)
            else:
                draw.text((self.x, y_offset), f"{label}:", fill=color)

            # Draw bar background (dark)
            bar_x = self.x + 25
            bar_width = max(30, self.width - 30)
            bar_y = y_offset + int(bar_height / 4)

            # Draw background bar
            draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
                          fill=(50, 50, 50))

            # Draw value bar
            filled_width = int(bar_width * (value / 100.0))
            draw.rectangle([bar_x, bar_y, bar_x + filled_width, bar_y + bar_height],
                          fill=color)

            # Draw percentage text
            percentage_text = f"{value:.0f}%"
            if font:
                text_bbox = draw.textbbox((0, 0), percentage_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = bar_x + bar_width - text_width - 2
                draw.text((text_x, y_offset), percentage_text, fill=color, font=font)
            else:
                draw.text((bar_x + bar_width - 20, y_offset), percentage_text, fill=color)

            y_offset += bar_spacing

        return image

    def get_property_schema(self) -> Dict[str, Any]:
        """Return property schema for this widget."""
        return {
            "metrics": {
                "type": "multiselect",
                "label": "Metrics to Display",
                "default": ["CPU", "Memory", "Disk"],
                "options": ["CPU", "Memory", "Disk"],
                "description": "Select which system metrics to display"
            },
            "update_interval": {
                "type": "integer",
                "label": "Update Interval",
                "default": 5,
                "min": 1,
                "max": 60,
                "description": "Update interval in seconds"
            },
            "color": {
                "type": "color",
                "label": "Bar Color",
                "default": (144, 238, 144),
                "description": "Color for the progress bars"
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert widget to dictionary representation."""
        data = super().to_dict()
        data['type'] = 'SystemStats'
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemStatsWidget':
        """Create widget from dictionary representation."""
        color_data = data.get("color", (144, 238, 144))

        # Ensure proper tuple type for color
        if isinstance(color_data, (list, tuple)):
            color_list = [int(c) for c in color_data[:3]]
            if len(color_list) < 3:
                color_list.extend([144] * (3 - len(color_list)))
            color = (color_list[0], color_list[1], color_list[2])
        else:
            color = (144, 238, 144)

        # Get metrics from properties
        properties = data.get('properties', {})
        metrics = properties.get('metrics', ['CPU', 'Memory', 'Disk'])

        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            metrics=metrics,
            update_interval=data.get("update_interval", 5),
            color=color,
            width=data.get("width"),
            height=data.get("height"),
            screen_size=data.get("screen_size", 64)
        )

    def validate(self) -> List[str]:
        """Validate widget configuration."""
        errors = super().validate()

        metrics = self.get_property('metrics', ['CPU', 'Memory', 'Disk'])
        if not metrics:
            errors.append("At least one metric must be selected")

        color = self.get_property('color', (144, 238, 144))
        if (len(color) != 3 or
            any(not isinstance(c, int) or c < 0 or c > 255 for c in color)):
            errors.append("Color must be RGB values between 0 and 255")

        return errors


class SystemStatsWidgetPlugin(WidgetPlugin):
    """Plugin for the System Stats widget."""

    @property
    def metadata(self) -> WidgetMetadata:
        """Return metadata for this plugin."""
        return WidgetMetadata(
            name="SystemStats",
            description="Displays system CPU, memory, and disk usage as bar graphs",
            version="1.0.0",
            author="Pixoomat Team",
            category="System",
            dependencies=["psutil>=5.8.0"]
        )

    def create_widget(self, **kwargs) -> SystemStatsWidget:
        """Create an instance of the system stats widget."""
        return SystemStatsWidget(**kwargs)

    def get_property_schema(self) -> Dict[str, Any]:
        """Return property schema for configuration UI."""
        widget = SystemStatsWidget()
        return widget.get_property_schema()
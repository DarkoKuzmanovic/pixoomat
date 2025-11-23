"""
Progress bar widget plugin for Pixoomat.

This plugin provides a progress bar widget that can display
progress with configurable colors and styles.
"""

from typing import Dict, Any, Tuple, Optional
from PIL import Image, ImageDraw

from widgets.base_widget import BaseWidget
from widgets.plugin_system import WidgetPlugin, WidgetMetadata


class ProgressBarWidget(BaseWidget):
    """Progress bar widget."""

    def __init__(self, x: int = 0, y: int = 0,
                 width: int = 50, height: int = 10,
                 progress: float = 0.5,
                 foreground_color: Tuple[int, int, int] = (0, 255, 0),
                 background_color: Tuple[int, int, int] = (64, 64, 64),
                 border_color: Tuple[int, int, int] = (128, 128, 128),
                 show_percentage: bool = False,
                 screen_size: int = 64):
        super().__init__(x, y, width, height, screen_size)

        # Store properties in the properties dictionary for consistency
        self.set_property('progress', max(0.0, min(1.0, progress)))  # Clamp between 0 and 1
        self.set_property('foreground_color', foreground_color)
        self.set_property('background_color', background_color)
        self.set_property('border_color', border_color)
        self.set_property('show_percentage', show_percentage)

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """Get default size for this widget based on screen size."""
        scale_factor = screen_size / 64.0
        default_width = int(80 * scale_factor)
        default_height = int(8 * scale_factor)
        return (default_width, default_height)

    def get_render_data(self) -> Dict[str, Any]:
        """Get data needed for rendering this widget."""
        return {
            "type": "progress_bar",
            "progress": self.get_property('progress', 0.5),
            "foreground_color": self.get_property('foreground_color', (0, 255, 0)),
            "background_color": self.get_property('background_color', (64, 64, 64)),
            "border_color": self.get_property('border_color', (128, 128, 128)),
            "show_percentage": self.get_property('show_percentage', False),
            "position": (self.x, self.y),
            "size": (self.width, self.height)
        }

    def get_property_schema(self) -> Dict[str, Any]:
        """Return property schema for this widget."""
        return {
            "width": {
                "type": "integer",
                "label": "Width",
                "default": 50,
                "min": 20,
                "max": 64,
                "description": "Width of the progress bar"
            },
            "height": {
                "type": "integer",
                "label": "Height",
                "default": 10,
                "min": 4,
                "max": 20,
                "description": "Height of the progress bar"
            },
            "progress": {
                "type": "float",
                "label": "Progress",
                "default": 0.5,
                "min": 0.0,
                "max": 1.0,
                "step": 0.01,
                "description": "Progress value (0.0 to 1.0)"
            },
            "foreground_color": {
                "type": "color",
                "label": "Progress Color",
                "default": (0, 255, 0),
                "description": "RGB color for the progress fill"
            },
            "background_color": {
                "type": "color",
                "label": "Background Color",
                "default": (64, 64, 64),
                "description": "RGB color for the background"
            },
            "border_color": {
                "type": "color",
                "label": "Border Color",
                "default": (128, 128, 128),
                "description": "RGB color for the border"
            },
            "show_percentage": {
                "type": "boolean",
                "label": "Show Percentage",
                "default": False,
                "description": "Show percentage text on the progress bar"
            }
        }

    def render(self, image: Image.Image) -> Image.Image:
        """Render the progress bar widget on the image."""
        # Get properties
        progress = self.get_property('progress', 0.5)
        foreground_color = self.get_property('foreground_color', (0, 255, 0))
        background_color = self.get_property('background_color', (64, 64, 64))
        border_color = self.get_property('border_color', (128, 128, 128))
        show_percentage = self.get_property('show_percentage', False)

        draw = ImageDraw.Draw(image)

        # Draw background
        draw.rectangle(
            [self.x, self.y, self.x + self.width - 1, self.y + self.height - 1],
            fill=background_color,
            outline=border_color
        )

        # Draw progress fill
        if progress > 0:
            fill_width = int((self.width - 2) * progress)  # -2 for borders
            draw.rectangle(
                [self.x + 1, self.y + 1, self.x + fill_width, self.y + self.height - 2],
                fill=foreground_color
            )

        # Draw percentage text if enabled
        if show_percentage and self.height >= 8:
            percentage_text = f"{int(progress * 100)}%"
            try:
                # Try to center the text
                text_bbox = draw.textbbox((0, 0), percentage_text)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                text_x = self.x + (self.width - text_width) // 2
                text_y = self.y + (self.height - text_height) // 2

                # Use contrasting color for text
                text_color = (255, 255, 255) if sum(background_color) < 384 else (0, 0, 0)
                draw.text((text_x, text_y), percentage_text, fill=text_color)

            except Exception:
                # Skip text if rendering fails
                pass

        return image

    def to_dict(self) -> Dict[str, Any]:
        """Convert widget to dictionary representation."""
        data = super().to_dict()
        # Override type to match plugin name
        data['type'] = 'ProgressBar'
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProgressBarWidget':
        """Create widget from dictionary representation."""
        # Helper function to ensure 3-tuple colors
        def to_color_tuple(color_data, default):
            if isinstance(color_data, (list, tuple)):
                color_list = [int(c) for c in color_data[:3]]
                if len(color_list) < 3:
                    color_list.extend([default[i] for i in range(len(color_list), 3)])
                return (color_list[0], color_list[1], color_list[2])
            return default

        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            width=data.get("width", 50),
            height=data.get("height", 10),
            progress=data.get("progress", 0.5),
            foreground_color=to_color_tuple(data.get("foreground_color"), (0, 255, 0)),
            background_color=to_color_tuple(data.get("background_color"), (64, 64, 64)),
            border_color=to_color_tuple(data.get("border_color"), (128, 128, 128)),
            show_percentage=data.get("show_percentage", False),
            screen_size=data.get("screen_size", 64)
        )

    def update_property(self, property_name: str, value: Any):
        """Update a specific property."""
        if property_name == "progress":
            # Clamp progress between 0 and 1
            value = max(0.0, min(1.0, float(value)))
        self.set_property(property_name, value)


class ProgressBarPlugin(WidgetPlugin):
    """Plugin for the progress bar widget."""

    @property
    def metadata(self) -> WidgetMetadata:
        """Return metadata for this plugin."""
        return WidgetMetadata(
            name="ProgressBar",
            description="Display a horizontal progress bar with customizable colors and percentage display",
            version="1.0.0",
            author="Pixoomat Team",
            category="Display",
            dependencies=[]
        )

    def create_widget(self, **kwargs) -> ProgressBarWidget:
        """Create an instance of the progress bar widget."""
        return ProgressBarWidget(**kwargs)

    def get_property_schema(self) -> Dict[str, Any]:
        """Return property schema for configuration UI."""
        widget = ProgressBarWidget()
        return widget.get_property_schema()

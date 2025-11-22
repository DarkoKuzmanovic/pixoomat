"""
Simple text widget plugin for Pixoomat.

This plugin provides a basic text display widget that can show
custom text with configurable colors and positioning.
"""

from typing import Dict, Any, Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFont
import os

try:
    from ..base_widget import BaseWidget
    from ..plugin_system import WidgetPlugin, WidgetMetadata
except ImportError:
    from base_widget import BaseWidget
    from plugin_system import WidgetPlugin, WidgetMetadata


class SimpleTextWidget(BaseWidget):
    """Simple text display widget."""

    def __init__(self, x: int = 0, y: int = 0,
                 text: str = "Hello", color: Tuple[int, int, int] = (255, 255, 255),
                 font_size: int = 12, background_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
                 width: Optional[int] = None, height: Optional[int] = None, screen_size: int = 64):
        super().__init__(x, y, width, height, screen_size)

        # Store properties in the properties dictionary for consistency
        self.set_property('text', text)
        self.set_property('color', color)
        self.set_property('font_size', font_size)
        self.set_property('background_color', background_color)

        # Calculate actual dimensions based on text
        self._calculate_dimensions()

    def _calculate_dimensions(self):
        """Calculate widget dimensions based on text and font."""
        text = self.get_property('text', 'Hello')
        font_size = self.get_property('font_size', 12)

        try:
            # Try to use a simple font measurement
            temp_img = Image.new('RGB', (1, 1))
            draw = ImageDraw.Draw(temp_img)

            # Estimate text dimensions (character width approximation)
            char_width = font_size * 0.6
            char_height = font_size

            self.width = int(len(text) * char_width)
            self.height = int(char_height * 1.2)  # Add some padding

        except Exception:
            # Fallback dimensions
            self.width = max(50, len(text) * 6)
            self.height = max(15, font_size)

    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """Get default size for this widget based on screen size."""
        # Calculate based on text length and screen size
        text = self.get_property('text', 'Hello')
        font_size = self.get_property('font_size', 12)
        scale_factor = screen_size / 64.0  # Normalize to 64px screen
        char_width = int(6 * scale_factor)
        char_height = int(12 * scale_factor)

        width = max(len(text) * char_width, 30)
        height = max(char_height, 10)

        return (width, height)

    def get_render_data(self) -> Dict[str, Any]:
        """Get data needed for rendering this widget."""
        return {
            "type": "text",
            "text": self.get_property('text', 'Hello'),
            "color": self.get_property('color', (255, 255, 255)),
            "font_size": self.get_property('font_size', 12),
            "background_color": self.get_property('background_color', (0, 0, 0, 0)),
            "x": self.x,
            "y": self.y
        }

    def get_property_schema(self) -> Dict[str, Any]:
        """Return property schema for this widget."""
        return {
            "text": {
                "type": "string",
                "label": "Text",
                "default": "Hello",
                "description": "Text to display"
            },
            "color": {
                "type": "color",
                "label": "Text Color",
                "default": (255, 255, 255),
                "description": "RGB color for the text"
            },
            "font_size": {
                "type": "integer",
                "label": "Font Size",
                "default": 12,
                "min": 8,
                "max": 32,
                "description": "Size of the text font"
            },
            "background_color": {
                "type": "color",
                "label": "Background Color",
                "default": (0, 0, 0, 0),
                "description": "RGB color for background (alpha = transparent)"
            }
        }

    def render(self, image: Image.Image) -> Image.Image:
        """Render the text widget on the image."""
        # Get properties
        text = self.get_property('text', 'Hello')
        color = self.get_property('color', (255, 255, 255))
        background_color = self.get_property('background_color', (0, 0, 0, 0))

        # Create a transparent overlay for this widget
        overlay = Image.new('RGBA', (self.width, self.height), background_color)
        draw = ImageDraw.Draw(overlay)

        try:
            # Try to load a font
            font = ImageFont.load_default()

            # Draw text
            draw.text((0, 0), text, fill=color, font=font)

        except Exception:
            # Fallback rendering
            draw.text((0, 0), text, fill=color)

        # Paste the overlay onto the main image
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        image.paste(overlay, (self.x, self.y), overlay if background_color[3] < 255 else None)

        return image

    def to_dict(self) -> Dict[str, Any]:
        """Convert widget to dictionary representation."""
        data = super().to_dict()
        # Override type to match plugin name
        data['type'] = 'SimpleText'
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SimpleTextWidget':
        """Create widget from dictionary representation."""
        color_data = data.get("color", (255, 255, 255))
        bg_color_data = data.get("background_color", (0, 0, 0, 0))

        # Ensure proper tuple types
        if isinstance(color_data, (list, tuple)):
            color_list = [int(c) for c in color_data[:3]]
            if len(color_list) < 3:
                color_list.extend([255] * (3 - len(color_list)))
            color = (color_list[0], color_list[1], color_list[2])
        else:
            color = (255, 255, 255)

        if isinstance(bg_color_data, (list, tuple)):
            bg_color_list = [int(c) for c in bg_color_data[:4]]
            if len(bg_color_list) < 4:
                bg_color_list.extend([0] * (4 - len(bg_color_list)))
            bg_color = (bg_color_list[0], bg_color_list[1], bg_color_list[2], bg_color_list[3])
        else:
            bg_color = (0, 0, 0, 0)

        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            text=data.get("text", "Hello"),
            color=color,
            font_size=data.get("font_size", 12),
            background_color=bg_color,
            width=data.get("width"),
            height=data.get("height"),
            screen_size=data.get("screen_size", 64)
        )

    def update_property(self, property_name: str, value: Any):
        """Update a specific property."""
        self.set_property(property_name, value)
        if property_name in ["text", "font_size"]:
            self._calculate_dimensions()


class SimpleTextPlugin(WidgetPlugin):
    """Plugin for the simple text widget."""

    @property
    def metadata(self) -> WidgetMetadata:
        """Return metadata for this plugin."""
        return WidgetMetadata(
            name="SimpleText",
            description="Display custom text with configurable colors and font size",
            version="1.0.0",
            author="Pixoomat Team",
            category="Display",
            dependencies=[]
        )

    def create_widget(self, **kwargs) -> SimpleTextWidget:
        """Create an instance of the simple text widget."""
        return SimpleTextWidget(**kwargs)

    def get_property_schema(self) -> Dict[str, Any]:
        """Return property schema for configuration UI."""
        widget = SimpleTextWidget()
        return widget.get_property_schema()

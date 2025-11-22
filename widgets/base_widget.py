"""
Base widget class for Pixoomat
Provides common functionality and interface for all display widgets
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional
import datetime


class BaseWidget(ABC):
    """Base class for all display widgets"""

    def __init__(self, x: int = 0, y: int = 0, width: Optional[int] = None, height: Optional[int] = None, screen_size: int = 64):
        """
        Initialize widget with position and size

        Args:
            x: X position on screen (pixels from left)
            y: Y position on screen (pixels from top)
            width: Widget width in pixels (None for default)
            height: Widget height in pixels (None for default)
            screen_size: Screen size in pixels for calculating default sizes
        """
        self.screen_size = screen_size
        self.x = x
        self.y = y

        # Initialize properties before getting default size
        self.visible = True
        self.z_index = 0  # For layering overlapping widgets
        self.last_update = datetime.datetime.min
        self.update_interval = 60  # Default update interval in seconds

        # Widget-specific properties
        self.properties = {}
        try:
            self._init_properties()
        except Exception as e:
            print(f"Warning: Failed to initialize widget properties: {e}")
            # Set minimal default properties
            self.properties = {}

        # Set default size if not provided
        if width is None or height is None:
            default_width, default_height = self.get_default_size(screen_size)
            self.width = width if width is not None else default_width
            self.height = height if height is not None else default_height
        else:
            self.width = width
            self.height = height

    def _init_properties(self):
        """Initialize widget-specific properties. Override in subclasses."""
        pass

    @property
    def position(self) -> Tuple[int, int]:
        """Get widget position as (x, y) tuple"""
        return (self.x, self.y)

    @property
    def size(self) -> Tuple[int, int]:
        """Get widget size as (width, height) tuple"""
        return (self.width, self.height)

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """Get widget bounds as (x, y, x+width, y+height)"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def contains_point(self, x: int, y: int) -> bool:
        """
        Check if a point (x, y) is within the widget bounds

        Args:
            x: X coordinate to check
            y: Y coordinate to check

        Returns:
            True if point is within widget bounds
        """
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def set_position(self, x: int, y: int):
        """Set widget position"""
        self.x = x
        self.y = y

    def set_size(self, width: int, height: int):
        """Set widget size"""
        self.width = width
        self.height = height

    def set_property(self, key: str, value: Any):
        """Set a widget-specific property"""
        self.properties[key] = value

    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a widget-specific property"""
        return self.properties.get(key, default)

    def should_update(self) -> bool:
        """
        Check if widget should be updated based on its update interval

        Returns:
            True if widget should be updated
        """
        now = datetime.datetime.now()
        return (now - self.last_update).total_seconds() >= self.update_interval

    def mark_updated(self):
        """Mark the widget as updated (reset update timer)"""
        self.last_update = datetime.datetime.now()

    @abstractmethod
    def get_render_data(self) -> Dict[str, Any]:
        """
        Get data needed for rendering this widget

        Returns:
            Dictionary containing render information (text, shapes, colors, etc.)
        """
        pass

    @abstractmethod
    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """
        Get default size for this widget based on screen size

        Args:
            screen_size: Screen size in pixels (typically 16, 32, or 64)

        Returns:
            Default (width, height) tuple
        """
        pass

    def validate(self) -> list[str]:
        """
        Validate widget configuration

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if self.width <= 0 or self.height <= 0:
            errors.append("Widget dimensions must be positive")

        if self.update_interval <= 0:
            errors.append("Update interval must be positive")

        return errors

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert widget to dictionary representation for serialization

        Returns:
            Dictionary representation of widget
        """
        return {
            'type': self.__class__.__name__,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'visible': self.visible,
            'z_index': self.z_index,
            'update_interval': self.update_interval,
            'properties': self.properties
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseWidget':
        """
        Create widget from dictionary representation

        Args:
            data: Dictionary representation of widget

        Returns:
            Widget instance
        """
        # This method will be overridden in subclasses
        # because we need to know the specific widget type
        widget = cls(
            x=data.get('x', 0),
            y=data.get('y', 0),
            width=data.get('width', None),
            height=data.get('height', None)
        )
        widget.visible = data.get('visible', True)
        widget.z_index = data.get('z_index', 0)
        widget.update_interval = data.get('update_interval', 60)
        widget.properties = data.get('properties', {})
        return widget

    def __str__(self) -> str:
        """String representation of widget"""
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, w={self.width}, h={self.height})"
"""
Layout manager for Pixoomat widgets
Handles widget positioning, layering, and rendering coordination
"""
from typing import List, Dict, Any, Optional, Tuple, Type, Union
import datetime

from widgets.base_widget import BaseWidget


class WidgetFactory:
    """Factory for creating widget instances from type names and data"""

    def __init__(self):
        """Initialize the widget factory"""
        self._builtin_widgets = {}
        self._plugin_manager = None
        self._initialize_builtin_widgets()

    def _initialize_builtin_widgets(self):
        """Initialize built-in widget classes - now using plugin system"""
        # Built-in widgets are now handled by the plugin system
        self._builtin_widgets = {}

    def _get_plugin_manager(self):
        """Get the plugin manager instance"""
        if self._plugin_manager is None:
            try:
                from widgets.plugin_system import get_plugin_manager
                self._plugin_manager = get_plugin_manager()
            except ImportError as e:
                print(f"Warning: Could not import plugin system: {e}")
                self._plugin_manager = None
        return self._plugin_manager

    def create_widget(self, widget_type: str, widget_data: Dict[str, Any], screen_size: int = 64) -> Optional[BaseWidget]:
        """
        Create a widget instance from type and data

        Args:
            widget_type: Type name of the widget
            widget_data: Dictionary containing widget configuration
            screen_size: Screen size in pixels

        Returns:
            Widget instance or None if creation failed
        """
        # First try built-in widgets
        if widget_type in self._builtin_widgets:
            widget_class = self._builtin_widgets[widget_type]
            return self._create_builtin_widget(widget_class, widget_data, screen_size)

        # Then try plugin widgets
        plugin_manager = self._get_plugin_manager()
        if plugin_manager:
            # Try direct plugin name match
            widget_class = plugin_manager.get_widget_class(widget_type)
            if widget_class:
                return self._create_plugin_widget(widget_class, widget_data, screen_size)

            # Try plugin metadata name match (for backward compatibility)
            for plugin_name, plugin_class in plugin_manager.widget_classes.items():
                if plugin_name == widget_type:
                    return self._create_plugin_widget(plugin_class, widget_data, screen_size)

        return None

    def _create_builtin_widget(self, widget_class: Type[BaseWidget], widget_data: Dict[str, Any], screen_size: int) -> BaseWidget:
        """Create a built-in widget from data"""
        widget = widget_class(
            x=widget_data.get('x', 0),
            y=widget_data.get('y', 0),
            width=widget_data.get('width'),
            height=widget_data.get('height'),
            screen_size=screen_size
        )

        # Set common properties
        widget.visible = widget_data.get('visible', True)
        widget.z_index = widget_data.get('z_index', 0)
        widget.update_interval = widget_data.get('update_interval', 60)

        # Set widget-specific properties
        properties = widget_data.get('properties', {})
        for key, value in properties.items():
            widget.set_property(key, value)

        return widget

    def _create_plugin_widget(self, widget_class: Type[BaseWidget], widget_data: Dict[str, Any], screen_size: int) -> Optional[BaseWidget]:
        """Create a plugin widget from data"""
        # Extract widget-specific properties from the top level for backward compatibility
        kwargs = {
            'x': widget_data.get('x', 0),
            'y': widget_data.get('y', 0),
            'width': widget_data.get('width'),
            'height': widget_data.get('height'),
            'screen_size': screen_size
        }

        # Add other properties as kwargs (for plugin widgets that use direct attributes)
        for key, value in widget_data.items():
            if key not in ['type', 'x', 'y', 'width', 'height', 'visible', 'z_index', 'update_interval', 'properties']:
                kwargs[key] = value

        try:
            widget = widget_class(**kwargs)

            # Set common properties
            widget.visible = widget_data.get('visible', True)
            widget.z_index = widget_data.get('z_index', 0)
            widget.update_interval = widget_data.get('update_interval', 60)

            # If the widget uses properties dict, set those too
            properties = widget_data.get('properties', {})
            for key, value in properties.items():
                widget.set_property(key, value)

            return widget
        except Exception as e:
            print(f"Error creating plugin widget {widget_class.__name__}: {e}")
            return None

    def get_available_widget_types(self) -> List[str]:
        """Get list of all available widget types"""
        types = list(self._builtin_widgets.keys())

        plugin_manager = self._get_plugin_manager()
        if plugin_manager:
            types.extend(plugin_manager.widget_classes.keys())

        return types


class LayoutManager:
    """Manages widget layout and rendering for Pixoomat display"""

    def __init__(self, screen_size: int = 64):
        """
        Initialize layout manager

        Args:
            screen_size: Screen size in pixels (typically 16, 32, or 64)
        """
        self.screen_size = screen_size
        self.widgets: List[BaseWidget] = []
        self.background_color: Tuple[int, int, int] = (0, 0, 0)  # Default black background

    def add_widget(self, widget: BaseWidget):
        """
        Add a widget to the layout

        Args:
            widget: Widget to add
        """
        self.widgets.append(widget)
        # Sort widgets by z-index for proper layering
        self._sort_widgets()

    def remove_widget(self, widget: BaseWidget):
        """
        Remove a widget from the layout

        Args:
            widget: Widget to remove
        """
        if widget in self.widgets:
            self.widgets.remove(widget)

    def get_widget_at(self, x: int, y: int) -> Optional[BaseWidget]:
        """
        Get the widget at the specified position (top-most in z-order)

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Widget at position or None if no widget found
        """
        # Check widgets in reverse z-order (top to bottom)
        for widget in reversed(self._sorted_widgets()):
            if widget.visible and widget.contains_point(x, y):
                return widget
        return None

    def get_widgets_in_area(self, x: int, y: int, width: int, height: int) -> List[BaseWidget]:
        """
        Get all widgets within the specified area

        Args:
            x: X coordinate of area top-left
            y: Y coordinate of area top-left
            width: Width of area
            height: Height of area

        Returns:
            List of widgets in the area (ordered by z-index)
        """
        result = []
        area_bounds = (x, y, x + width, y + height)

        for widget in self._sorted_widgets():
            if not widget.visible:
                continue

            # Check if widget bounds intersect with area bounds
            w_bounds = widget.bounds
            if self._bounds_intersect(w_bounds, area_bounds):
                result.append(widget)

        return result

    def _bounds_intersect(self, bounds1: Tuple[int, int, int, int],
                         bounds2: Tuple[int, int, int, int]) -> bool:
        """
        Check if two bounds intersect

        Args:
            bounds1: (x1, y1, x2, y2)
            bounds2: (x1, y1, x2, y2)

        Returns:
            True if bounds intersect
        """
        x1, y1, x2, y2 = bounds1
        x3, y3, x4, y4 = bounds2

        return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

    def _sort_widgets(self):
        """Sort widgets by z-index"""
        self.widgets.sort(key=lambda w: w.z_index)

    def _sorted_widgets(self) -> List[BaseWidget]:
        """Get widgets sorted by z-index (lowest to highest)"""
        return sorted(self.widgets, key=lambda w: w.z_index)

    def validate_layout(self) -> List[str]:
        """
        Validate the entire layout

        Returns:
            List of validation error messages
        """
        errors = []

        # Validate each widget
        for widget in self.widgets:
            widget_errors = widget.validate()
            errors.extend([f"{widget}: {error}" for error in widget_errors])

        # Check for widgets outside screen bounds
        for widget in self.widgets:
            if widget.x < 0 or widget.y < 0:
                errors.append(f"{widget}: Position cannot be negative")

            if (widget.x + widget.width > self.screen_size or
                widget.y + widget.height > self.screen_size):
                errors.append(f"{widget}: Extends beyond screen bounds")

        return errors

    def get_render_data(self) -> Dict[str, Any]:
        """
        Get complete render data for all widgets

        Returns:
            Dictionary with all render information
        """
        # Background render data
        render_data = {
            'background': {
                'color': self.background_color,
                'width': self.screen_size,
                'height': self.screen_size
            },
            'widgets': []
        }

        # Add render data for each widget (in z-order)
        for widget in self._sorted_widgets():
            if widget.visible:
                widget_data = widget.get_render_data()
                widget_data['id'] = id(widget)  # Add unique identifier
                widget_data['z_index'] = widget.z_index
                render_data['widgets'].append(widget_data)

        return render_data

    def update_widgets(self) -> List[BaseWidget]:
        """
        Check and update widgets that need to be refreshed

        Returns:
            List of widgets that were updated
        """
        updated_widgets = []

        for widget in self.widgets:
            if widget.should_update():
                widget.mark_updated()
                updated_widgets.append(widget)

        return updated_widgets

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert layout to dictionary representation

        Returns:
            Dictionary representation of layout
        """
        return {
            'screen_size': self.screen_size,
            'background_color': list(self.background_color),
            'widgets': [widget.to_dict() for widget in self.widgets]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LayoutManager':
        """
        Create layout from dictionary representation

        Args:
            data: Dictionary representation of layout

        Returns:
            LayoutManager instance
        """
        screen_size = data.get('screen_size', 64)
        layout = cls(screen_size)

        # Set background color
        bg_color = data.get('background_color', [0, 0, 0])
        layout.background_color = tuple(bg_color) if len(bg_color) == 3 else (0, 0, 0)

        # Get widget factory
        factory = cls.get_widget_factory()

        # Create widgets
        for widget_data in data.get('widgets', []):
            widget_type = widget_data.get('type')

            # Try to create widget using factory
            widget = factory.create_widget(widget_type, widget_data, screen_size)

            if widget:
                layout.add_widget(widget)
            else:
                print(f"Warning: Unknown widget type '{widget_type}' skipped during layout loading")

        return layout

    @classmethod
    def get_widget_factory(cls) -> 'WidgetFactory':
        """Get the widget factory instance"""
        if not hasattr(cls, '_widget_factory'):
            cls._widget_factory = WidgetFactory()
        return cls._widget_factory

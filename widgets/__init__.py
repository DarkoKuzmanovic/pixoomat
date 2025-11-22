"""
Widget package for Pixoomat
Contains base widget classes and specific widget implementations
"""

from .base_widget import BaseWidget
from .clock_widget import ClockWidget
from .weather_widget import WeatherWidget
from .plugin_system import WidgetPlugin, WidgetMetadata, PluginManager, get_plugin_manager

__all__ = ['BaseWidget', 'ClockWidget', 'WeatherWidget', 'WidgetPlugin', 'WidgetMetadata', 'PluginManager', 'get_plugin_manager']
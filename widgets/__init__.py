"""
Widget package for Pixoomat
Contains base widget classes and specific widget implementations
"""

from .base_widget import BaseWidget
from .plugin_system import WidgetPlugin, WidgetMetadata, PluginManager, get_plugin_manager

__all__ = ['BaseWidget', 'WidgetPlugin', 'WidgetMetadata', 'PluginManager', 'get_plugin_manager']
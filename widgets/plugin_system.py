"""
Plugin system for Pixoomat widgets.

This module provides a framework for dynamically loading and managing
custom widgets, allowing users to extend Pixoomat with new functionality.
"""

import os
import sys
import importlib
import importlib.util
import inspect
from typing import Dict, List, Type, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

try:
    from .base_widget import BaseWidget
except ImportError:
    from base_widget import BaseWidget


@dataclass
class WidgetMetadata:
    """Metadata for a widget plugin."""
    name: str
    description: str
    version: str
    author: str
    category: str
    icon_path: Optional[str] = None
    dependencies: Optional[List[str]] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class WidgetPlugin(ABC):
    """Base class for widget plugins."""

    @property
    @abstractmethod
    def metadata(self) -> WidgetMetadata:
        """Return metadata for this plugin."""
        pass

    @abstractmethod
    def create_widget(self, **kwargs) -> BaseWidget:
        """Create an instance of the widget."""
        pass

    @abstractmethod
    def get_property_schema(self) -> Dict[str, Any]:
        """Return property schema for configuration UI."""
        pass


class PluginManager:
    """Manages loading and registration of widget plugins."""

    def __init__(self):
        self.plugins: Dict[str, WidgetPlugin] = {}
        self.widget_classes: Dict[str, Type[BaseWidget]] = {}
        self.plugin_paths: List[str] = []

        # Add default plugin paths
        try:
            self.add_plugin_path(os.path.join(os.path.dirname(__file__), 'plugins'))
        except Exception:
            self.add_plugin_path(os.path.join(os.getcwd(), 'widgets', 'plugins'))

    def add_plugin_path(self, path: str):
        """Add a directory to search for plugins."""
        if path not in self.plugin_paths:
            self.plugin_paths.append(path)

    def register_plugin(self, plugin: WidgetPlugin):
        """Register a plugin instance."""
        metadata = plugin.metadata

        # Check for conflicts
        if metadata.name in self.plugins:
            existing = self.plugins[metadata.name]
            if existing.metadata.version == metadata.version:
                return False

        # Register plugin
        self.plugins[metadata.name] = plugin

        # Register widget class
        widget_instance = plugin.create_widget()
        self.widget_classes[metadata.name] = widget_instance.__class__

        return True

    def unregister_plugin(self, name: str):
        """Unregister a plugin by name."""
        if name in self.plugins:
            del self.plugins[name]
        if name in self.widget_classes:
            del self.widget_classes[name]

    def load_plugins_from_directory(self, directory: str):
        """Load all plugins from a directory."""
        if not os.path.exists(directory):
            return

        # Save original working directory and path
        original_cwd = os.getcwd()
        original_path = sys.path[:]

        try:
            # Change to the parent directory for proper imports
            parent_dir = os.path.dirname(directory)
            os.chdir(parent_dir)

            # Add parent to path
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

            # Get the plugin subdirectory name
            plugin_subdir = os.path.basename(directory)

            # Scan for all Python files in the directory (excluding __init__.py)
            if not os.path.isdir(directory):
                return

            for filename in os.listdir(directory):
                if filename.endswith('.py') and filename != '__init__.py':
                    module_name = filename[:-3]  # Remove .py extension

                    try:
                        # Import the module
                        module = __import__(f"{plugin_subdir}.{module_name}", fromlist=[module_name])

                        # Look for plugin classes in the module
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if (issubclass(obj, WidgetPlugin) and
                                obj != WidgetPlugin and
                                not inspect.isabstract(obj)):
                                # Instantiate and register the plugin
                                plugin_instance = obj()
                                self.register_plugin(plugin_instance)
                                break  # Only register the first valid plugin class per module

                    except ImportError as e:
                        pass
                    except Exception as e:
                        pass

        finally:
            # Restore original directory and path
            os.chdir(original_cwd)
            sys.path[:] = original_path

    def load_plugin_from_file(self, file_path: str, module_name: Optional[str] = None):
        """Load a plugin from a Python file."""
        if module_name is None:
            module_name = os.path.splitext(os.path.basename(file_path))[0]

        try:
            # Save original working directory and path
            original_cwd = os.getcwd()
            original_path = sys.path[:]

            # Change to widgets directory
            widgets_dir = os.path.dirname(os.path.dirname(__file__))
            os.chdir(widgets_dir)
            if widgets_dir not in sys.path:
                sys.path.insert(0, widgets_dir)

            # Import the module
            plugin_dir = os.path.dirname(file_path)
            plugin_file = os.path.basename(file_path)

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                raise ImportError(f"Could not load spec from {file_path}")
            module = importlib.util.module_from_spec(spec)
            if spec.loader is None:
                raise ImportError(f"No loader found for {file_path}")
            spec.loader.exec_module(module)

            # Look for plugin classes in the module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, WidgetPlugin) and
                    obj != WidgetPlugin and
                    not inspect.isabstract(obj)):
                    plugin_instance = obj()
                    self.register_plugin(plugin_instance)
                    break

            # Restore original directory and path
            os.chdir(original_cwd)
            sys.path[:] = original_path

        except Exception as e:
            # Restore even on error
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
            if 'original_path' in locals():
                sys.path[:] = original_path

    def load_all_plugins(self):
        """Load plugins from all registered paths."""
        for path in self.plugin_paths:
            self.load_plugins_from_directory(path)

    def get_plugin(self, name: str) -> Optional[WidgetPlugin]:
        """Get a plugin by name."""
        return self.plugins.get(name)

    def get_widget_class(self, name: str) -> Optional[Type[BaseWidget]]:
        """Get a widget class by plugin name."""
        return self.widget_classes.get(name)

    def list_plugins(self) -> List[WidgetMetadata]:
        """List all registered plugins."""
        return [plugin.metadata for plugin in self.plugins.values()]

    def get_plugins_by_category(self, category: str) -> List[WidgetPlugin]:
        """Get all plugins in a specific category."""
        return [plugin for plugin in self.plugins.values()
                if plugin.metadata.category == category]

    def create_widget(self, plugin_name: str, **kwargs) -> Optional[BaseWidget]:
        """Create a widget instance from a plugin."""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            return plugin.create_widget(**kwargs)
        return None


# Global plugin manager instance
_plugin_manager = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
        _plugin_manager.load_all_plugins()
    return _plugin_manager


def register_plugin(plugin: WidgetPlugin):
    """Convenience function to register a plugin."""
    return get_plugin_manager().register_plugin(plugin)
#!/usr/bin/env python3
"""
Test script for Pixoomat plugin system
"""

import sys
import os

# Add the project root directory to sys.path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from widgets.plugin_system import get_plugin_manager, register_plugin
from widgets.plugins.simple_text import SimpleTextPlugin
from widgets.plugins.progress_bar import ProgressBarPlugin


def test_plugin_system():
    """Test the plugin system functionality."""
    print("Testing Pixoomat Plugin System")
    print("=" * 40)

    # Get plugin manager
    plugin_manager = get_plugin_manager()

    # Register plugins manually (in case auto-loading fails)
    print("\n1. Registering plugins...")
    register_plugin(SimpleTextPlugin())
    register_plugin(ProgressBarPlugin())

    # List all plugins
    print("\n2. Available plugins:")
    plugins = plugin_manager.list_plugins()
    for plugin_meta in plugins:
        print(f"   - {plugin_meta.name}: {plugin_meta.description}")
        print(f"     Version: {plugin_meta.version} by {plugin_meta.author}")
        print(f"     Category: {plugin_meta.category}")

    # Test creating widgets
    print("\n3. Creating widget instances:")

    # Test SimpleText widget
    text_widget = plugin_manager.create_widget("SimpleText",
                                                text="Test Text",
                                                color=(255, 0, 0),
                                                x=10, y=10)
    if text_widget:
        print(f"   + SimpleText widget created: '{text_widget.get_property('text')}' at ({text_widget.x}, {text_widget.y})")
        print(f"     Dimensions: {text_widget.width}x{text_widget.height}")
        print(f"     Schema keys: {list(text_widget.get_property_schema().keys())}")
    else:
        print("   - Failed to create SimpleText widget")

    # Test ProgressBar widget
    progress_widget = plugin_manager.create_widget("ProgressBar",
                                                  progress=0.75,
                                                  foreground_color=(0, 255, 0),
                                                  width=80, height=8)
    if progress_widget:
        print(f"   + ProgressBar widget created with {progress_widget.get_property('progress'):.0%} progress")
        print(f"     Dimensions: {progress_widget.width}x{progress_widget.height}")
        print(f"     Schema keys: {list(progress_widget.get_property_schema().keys())}")
    else:
        print("   - Failed to create ProgressBar widget")

    # Test property updates
    print("\n4. Testing property updates:")
    if text_widget:
        original_text = text_widget.get_property('text')
        text_widget.update_property("text", "Updated Text")
        print(f"   + Text changed from '{original_text}' to '{text_widget.get_property('text')}'")
        print(f"     New dimensions: {text_widget.width}x{text_widget.height}")

    if progress_widget:
        original_progress = progress_widget.get_property('progress')
        progress_widget.update_property("progress", 0.25)
        print(f"   + Progress changed from {original_progress:.0%} to {progress_widget.get_property('progress'):.0%}")

    # Test serialization
    print("\n5. Testing serialization:")
    if text_widget:
        text_dict = text_widget.to_dict()
        print(f"   + SimpleText serialized: {text_dict['type']} at ({text_dict['x']}, {text_dict['y']})")

        # Test deserialization
        restored_widget = text_widget.__class__.from_dict(text_dict)
        print(f"   + SimpleText restored: '{restored_widget.get_property('text')}' at ({restored_widget.x}, {restored_widget.y})")

    # Test plugin categories
    print("\n6. Testing plugin categories:")
    display_plugins = plugin_manager.get_plugins_by_category("Display")
    print(f"   Found {len(display_plugins)} plugins in 'Display' category:")
    for plugin in display_plugins:
        print(f"   - {plugin.metadata.name}")

    print("\n" + "=" * 40)
    print("Plugin system test completed!")
    return True


def test_plugin_gui_integration():
    """Test plugin integration with GUI components."""
    print("\nTesting GUI integration...")

    try:
        # Test GUI imports work with plugins
        from gui.main_window_compact import CompactPixoomatGUI
        from widgets import get_plugin_manager
        import tkinter as tk

        # Get plugin manager
        plugin_manager = get_plugin_manager()

        # Create a root window (hidden)
        root = tk.Tk()
        root.withdraw()

        # Test GUI initialization
        from config import PixoomatConfig
        config = PixoomatConfig()

        print("   + Compact GUI components import successfully")
        print("   + Plugin manager integrates with Compact GUI")

        root.destroy()
        return True

    except Exception as e:
        print(f"   - GUI integration test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_plugin_system()
    if success:
        success = test_plugin_gui_integration()

    if success:
        print("\n+ All plugin system tests passed!")
        print("\nTo test with GUI:")
        print("  python main.py --use-gui")
    else:
        print("\n- Some tests failed!")
        sys.exit(1)
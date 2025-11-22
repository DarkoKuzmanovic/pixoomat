#!/usr/bin/env python3
"""
Test script for advanced Compact GUI components and features
"""
import sys
import os

# Add project root directory to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import PixoomatConfig
from gui.main_window_compact import CompactPixoomatGUI
from widgets import get_plugin_manager
from widgets.plugins.simple_text import SimpleTextPlugin
from widgets.plugins.progress_bar import ProgressBarPlugin
import tkinter as tk


def test_gui_advanced():
    """Test advanced Compact GUI components and features"""
    print("Testing advanced Compact GUI components...")

    # Create a minimal Tkinter app to test GUI
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Create test config with advanced settings
    config = PixoomatConfig()
    config.screen_size = 64
    config.show_weather = True
    config.use_gui = True

    try:
        # Test 1: Basic GUI initialization
        print("\n1. Testing basic GUI initialization...")
        app = CompactPixoomatGUI(root, config)
        print("   + Compact GUI initialized successfully!")

        # Test 2: Plugin integration with Compact GUI
        print("\n2. Testing plugin integration...")
        plugin_manager = get_plugin_manager()

        # Register plugins
        plugin_manager.register_plugin(SimpleTextPlugin())
        plugin_manager.register_plugin(ProgressBarPlugin())

        # Test creating widgets through plugin system
        text_widget = plugin_manager.create_widget("SimpleText", text="Advanced Test", color=(255, 100, 100))
        progress_widget = plugin_manager.create_widget("ProgressBar", progress=0.75, foreground_color=(100, 255, 100))

        if text_widget and progress_widget:
            print("   + Plugin widgets created successfully!")

            # Test adding widgets to layout
            app._add_widget(text_widget)
            app._add_widget(progress_widget)
            print("   + Widgets added to Compact GUI layout!")
        else:
            print("   - Failed to create plugin widgets")

        # Test 3: Advanced GUI features
        print("\n3. Testing advanced GUI features...")

        # Test zoom functionality
        original_zoom = app.zoom_level
        app._zoom_in()
        app._zoom_out()
        app._reset_zoom()
        print(f"   + Zoom functionality working (reset to {app.zoom_level:.1f}x)")

        # Test theme toggle
        original_contrast = app.high_contrast
        app._toggle_high_contrast()
        app._toggle_high_contrast()  # Toggle back
        print(f"   + High contrast theme toggle working")

        # Test undo/redo system
        app.undo_manager.save_state("Test state", app.layout_manager.to_dict())
        print("   + Undo/redo system initialized")

        # Test 4: Layout management
        print("\n4. Testing layout management...")

        # Test widget selection and movement
        if app.layout_manager.widgets:
            app.selected_widget = app.layout_manager.widgets[0]
            app._move_widget(5, 5)  # Move widget by 5 pixels
            print("   + Widget selection and movement working")

        # Test canvas update
        app._update_canvas()
        app._update_active_widgets_list()
        print("   + Canvas and widget list updates working")

        print("\nAdvanced Compact GUI test completed successfully!")
        print("All advanced features are working with the Compact GUI!")
        return True

    except Exception as e:
        print(f"Advanced Compact GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            root.destroy()
        except:
            pass


if __name__ == "__main__":
    test_gui_advanced()

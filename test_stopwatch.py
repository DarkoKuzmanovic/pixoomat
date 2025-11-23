#!/usr/bin/env python3
"""
Simple test script for the StopwatchWidget
"""

import sys
import os
import datetime

# Add the project root directory to sys.path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from widgets.plugin_system import get_plugin_manager, register_plugin
from widgets.plugins.stopwatch_widget import StopwatchWidgetPlugin


def test_stopwatch_widget():
    """Test the StopwatchWidget functionality."""
    print("Testing StopwatchWidget...")

    # Test 1: Instantiation via plugin manager
    plugin_manager = get_plugin_manager()
    register_plugin(StopwatchWidgetPlugin())

    stopwatch_widget = plugin_manager.create_widget("Stopwatch", x=25, y=35, width=130, height=45)
    assert stopwatch_widget is not None, "Failed to create StopwatchWidget via plugin manager"

    # Check if the widget has the expected attributes and methods
    assert hasattr(stopwatch_widget, 'get_property'), "Widget missing get_property method"
    assert hasattr(stopwatch_widget, 'set_property'), "Widget missing set_property method"
    assert hasattr(stopwatch_widget, 'get_render_data'), "Widget missing get_render_data method"
    assert hasattr(stopwatch_widget, 'to_dict'), "Widget missing to_dict method"
    assert hasattr(stopwatch_widget, 'from_dict'), "Widget missing from_dict method"
    assert hasattr(stopwatch_widget, 'get_default_size'), "Widget missing get_default_size method"

    # Check if it's a BaseWidget instance
    from widgets.base_widget import BaseWidget
    assert isinstance(stopwatch_widget, BaseWidget), "Created widget is not a BaseWidget instance"

    print("✓ StopwatchWidget instantiation via plugin manager successful")

    # Test 2: Direct instantiation by importing from the correct module
    from widgets.plugins.stopwatch_widget import StopwatchWidget
    direct_widget = StopwatchWidget(x=12, y=18, width=95, height=40)
    assert direct_widget.x == 12, "Direct instantiation failed to set x position"
    assert direct_widget.y == 18, "Direct instantiation failed to set y position"
    assert direct_widget.width == 95, "Direct instantiation failed to set width"
    assert direct_widget.height == 40, "Direct instantiation failed to set height"
    print("✓ StopwatchWidget direct instantiation successful")

    # Test 3: Default properties
    assert stopwatch_widget.get_property('state') == 'stopped', "Default state is incorrect"
    assert stopwatch_widget.get_property('label') == 'Stopwatch', "Default label is incorrect"
    assert stopwatch_widget.get_property('color') == (255, 255, 255), "Default color is incorrect"
    assert stopwatch_widget.update_interval == 60, "Default update_interval is incorrect"
    print("✓ StopwatchWidget default properties are correct")

    # Test 4: Render data
    render_data = stopwatch_widget.get_render_data()
    assert render_data['type'] == 'text', "Render data type is incorrect"
    assert 'text' in render_data, "Render data missing text field"
    assert 'color' in render_data, "Render data missing color field"
    assert 'position' in render_data, "Render data missing position field"
    assert 'size' in render_data, "Render data missing size field"
    assert render_data['position'] == (25, 35), "Render data position is incorrect"
    assert render_data['size'] == (130, 45), "Render data size is incorrect"
    print("✓ StopwatchWidget render data structure is correct")

    # Test 5: State transitions - stopped state
    stopwatch_widget.set_property('state', 'stopped')
    render_data = stopwatch_widget.get_render_data()
    assert 'Stopwatch' in render_data['text'], "Label not in render data"
    assert '00:00:00' in render_data['text'], "Initial time not displayed correctly"
    assert stopwatch_widget.update_interval == 60, "Update interval should be 60 when stopped"
    print("✓ StopwatchWidget stopped state works correctly")

    # Test 6: State transitions - running state
    stopwatch_widget.set_property('state', 'running')
    render_data = stopwatch_widget.get_render_data()
    assert 'Stopwatch' in render_data['text'], "Label not in render data"
    assert ':' in render_data['text'], "Time format should contain colons"
    assert stopwatch_widget.update_interval == 1, "Update interval should be 1 when running"
    print("✓ StopwatchWidget running state works correctly")

    # Test 7: State transitions - reset state
    stopwatch_widget.set_property('state', 'reset')
    render_data = stopwatch_widget.get_render_data()
    assert 'Stopwatch' in render_data['text'], "Label not in render data"
    assert '00:00:00' in render_data['text'], "Reset time not displayed correctly"
    assert stopwatch_widget.get_property('state') == 'stopped', "State should change to stopped after reset"
    assert stopwatch_widget.update_interval == 60, "Update interval should be 60 after reset"
    print("✓ StopwatchWidget reset state works correctly")

    # Test 8: Custom properties
    stopwatch_widget.set_property('label', 'My Timer')
    stopwatch_widget.set_property('color', (255, 0, 128))

    render_data = stopwatch_widget.get_render_data()
    assert 'My Timer' in render_data['text'], "Custom label not applied in render data"
    assert render_data['color'] == (255, 0, 128), "Custom color not applied in render data"
    print("✓ StopwatchWidget custom properties work correctly")

    # Test 9: Serialization/Deserialization
    widget_dict = stopwatch_widget.to_dict()
    assert widget_dict['type'] == 'StopwatchWidget', "Serialization type is incorrect"
    assert widget_dict['x'] == 25, "Serialization x position is incorrect"
    assert widget_dict['y'] == 35, "Serialization y position is incorrect"
    assert widget_dict['width'] == 130, "Serialization width is incorrect"
    assert widget_dict['height'] == 45, "Serialization height is incorrect"
    assert 'properties' in widget_dict, "Serialization missing properties"

    restored_widget = StopwatchWidget.from_dict(widget_dict)
    assert restored_widget.x == 25, "Deserialization x position is incorrect"
    assert restored_widget.y == 35, "Deserialization y position is incorrect"
    assert restored_widget.width == 130, "Deserialization width is incorrect"
    assert restored_widget.height == 45, "Deserialization height is incorrect"
    assert restored_widget.get_property('label') == 'My Timer', "Deserialization label is incorrect"
    assert restored_widget.get_property('color') == (255, 0, 128), "Deserialization color is incorrect"
    print("✓ StopwatchWidget serialization/deserialization works correctly")

    # Test 10: Default size calculation
    default_size = stopwatch_widget.get_default_size(64)
    assert isinstance(default_size, tuple), "Default size is not a tuple"
    assert len(default_size) == 2, "Default size tuple does not have 2 elements"
    assert default_size[0] > 0, "Default width is not positive"
    assert default_size[1] > 0, "Default height is not positive"
    print("✓ StopwatchWidget default size calculation works correctly")

    return True


if __name__ == "__main__":
    print("Testing StopwatchWidget")
    print("=" * 30)

    try:
        success = test_stopwatch_widget()
        if success:
            print("\n" + "=" * 30)
            print("StopwatchWidget tests passed successfully!")
            sys.exit(0)
        else:
            print("\nSome tests failed!")
            sys.exit(1)

    except Exception as e:
        print(f"\nTest execution failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
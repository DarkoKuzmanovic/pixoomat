#!/usr/bin/env python3
"""
Test script for DateWidget, CountdownWidget, and SystemStatsWidget
"""

import sys
import os
import datetime

# Add the project root directory to sys.path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from widgets.plugin_system import get_plugin_manager, register_plugin
from widgets.plugins.date_widget import DateWidget, DateWidgetPlugin
from widgets.plugins.countdown_widget import CountdownWidget, CountdownWidgetPlugin
from widgets.plugins.system_stats_widget import SystemStatsWidget, SystemStatsWidgetPlugin


def test_date_widget():
    """Test the DateWidget functionality."""
    print("Testing DateWidget...")

    # Test 1: Instantiation via plugin manager
    plugin_manager = get_plugin_manager()
    register_plugin(DateWidgetPlugin())

    date_widget = plugin_manager.create_widget("Date", x=10, y=20, width=100, height=30)
    assert date_widget is not None, "Failed to create DateWidget via plugin manager"
    assert isinstance(date_widget, DateWidget), "Created widget is not a DateWidget instance"
    print("✓ DateWidget instantiation via plugin manager successful")

    # Test 2: Direct instantiation
    direct_widget = DateWidget(x=5, y=10, width=80, height=25)
    assert direct_widget.x == 5, "Direct instantiation failed to set x position"
    assert direct_widget.y == 10, "Direct instantiation failed to set y position"
    assert direct_widget.width == 80, "Direct instantiation failed to set width"
    assert direct_widget.height == 25, "Direct instantiation failed to set height"
    print("✓ DateWidget direct instantiation successful")

    # Test 3: Default properties
    assert date_widget.get_property('format') == '%m/%d/%y', "Default format is incorrect"
    assert date_widget.get_property('color') == (255, 255, 255), "Default color is incorrect"
    assert date_widget.get_property('show_day_of_week') == True, "Default show_day_of_week is incorrect"
    assert date_widget.update_interval == 60, "Default update_interval is incorrect"
    print("✓ DateWidget default properties are correct")

    # Test 4: Render data
    render_data = date_widget.get_render_data()
    assert render_data['type'] == 'text', "Render data type is incorrect"
    assert 'text' in render_data, "Render data missing text field"
    assert 'color' in render_data, "Render data missing color field"
    assert 'position' in render_data, "Render data missing position field"
    assert 'size' in render_data, "Render data missing size field"
    assert render_data['position'] == (10, 20), "Render data position is incorrect"
    assert render_data['size'] == (100, 30), "Render data size is incorrect"
    print("✓ DateWidget render data structure is correct")

    # Test 5: Custom properties
    date_widget.set_property('format', '%Y-%m-%d')
    date_widget.set_property('color', (100, 200, 50))
    date_widget.set_property('show_day_of_week', False)

    render_data = date_widget.get_render_data()
    expected_date = datetime.datetime.now().strftime('%Y-%m-%d')
    assert expected_date in render_data['text'], "Custom format not applied in render data"
    assert render_data['color'] == (100, 200, 50), "Custom color not applied in render data"
    print("✓ DateWidget custom properties work correctly")

    # Test 6: Serialization/Deserialization
    widget_dict = date_widget.to_dict()
    assert widget_dict['type'] == 'DateWidget', "Serialization type is incorrect"
    assert widget_dict['x'] == 10, "Serialization x position is incorrect"
    assert widget_dict['y'] == 20, "Serialization y position is incorrect"
    assert widget_dict['width'] == 100, "Serialization width is incorrect"
    assert widget_dict['height'] == 30, "Serialization height is incorrect"
    assert 'properties' in widget_dict, "Serialization missing properties"

    restored_widget = DateWidget.from_dict(widget_dict)
    assert restored_widget.x == 10, "Deserialization x position is incorrect"
    assert restored_widget.y == 20, "Deserialization y position is incorrect"
    assert restored_widget.width == 100, "Deserialization width is incorrect"
    assert restored_widget.height == 30, "Deserialization height is incorrect"
    assert restored_widget.get_property('format') == '%Y-%m-%d', "Deserialization format is incorrect"
    assert restored_widget.get_property('color') == (100, 200, 50), "Deserialization color is incorrect"
    assert restored_widget.get_property('show_day_of_week') == False, "Deserialization show_day_of_week is incorrect"
    print("✓ DateWidget serialization/deserialization works correctly")

    # Test 7: Default size calculation
    default_size = date_widget.get_default_size(64)
    assert isinstance(default_size, tuple), "Default size is not a tuple"
    assert len(default_size) == 2, "Default size tuple does not have 2 elements"
    assert default_size[0] > 0, "Default width is not positive"
    assert default_size[1] > 0, "Default height is not positive"
    print("✓ DateWidget default size calculation works correctly")

    return True


def test_countdown_widget():
    """Test the CountdownWidget functionality."""
    print("\nTesting CountdownWidget...")

    # Test 1: Instantiation via plugin manager
    plugin_manager = get_plugin_manager()
    register_plugin(CountdownWidgetPlugin())

    countdown_widget = plugin_manager.create_widget("Countdown", x=15, y=25, width=120, height=40)
    assert countdown_widget is not None, "Failed to create CountdownWidget via plugin manager"
    assert isinstance(countdown_widget, CountdownWidget), "Created widget is not a CountdownWidget instance"
    print("✓ CountdownWidget instantiation via plugin manager successful")

    # Test 2: Direct instantiation
    direct_widget = CountdownWidget(x=8, y=12, width=90, height=35)
    assert direct_widget.x == 8, "Direct instantiation failed to set x position"
    assert direct_widget.y == 12, "Direct instantiation failed to set y position"
    assert direct_widget.width == 90, "Direct instantiation failed to set width"
    assert direct_widget.height == 35, "Direct instantiation failed to set height"
    print("✓ CountdownWidget direct instantiation successful")

    # Test 3: Default properties
    # The target_date should be set to next year by default
    now = datetime.datetime.now()
    next_year = now.year + 1
    expected_default_target = datetime.datetime(next_year, 1, 1, 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')

    assert countdown_widget.get_property('target_date') == expected_default_target, "Default target_date is incorrect"
    assert countdown_widget.get_property('label') == 'Countdown', "Default label is incorrect"
    assert countdown_widget.get_property('color') == (255, 255, 255), "Default color is incorrect"
    assert countdown_widget.update_interval == 1, "Default update_interval is incorrect"
    print("✓ CountdownWidget default properties are correct")

    # Test 4: Render data
    render_data = countdown_widget.get_render_data()
    assert render_data['type'] == 'text', "Render data type is incorrect"
    assert 'text' in render_data, "Render data missing text field"
    assert 'color' in render_data, "Render data missing color field"
    assert 'position' in render_data, "Render data missing position field"
    assert 'size' in render_data, "Render data missing size field"
    assert render_data['position'] == (15, 25), "Render data position is incorrect"
    assert render_data['size'] == (120, 40), "Render data size is incorrect"
    print("✓ CountdownWidget render data structure is correct")

    # Test 5: Custom properties
    future_date = (datetime.datetime.now() + datetime.timedelta(days=5, hours=4, minutes=3, seconds=2))
    future_date_str = future_date.strftime('%Y-%m-%d %H:%M:%S')

    countdown_widget.set_property('target_date', future_date_str)
    countdown_widget.set_property('label', 'My Countdown')
    countdown_widget.set_property('color', (50, 100, 200))

    render_data = countdown_widget.get_render_data()
    assert 'My Countdown' in render_data['text'], "Custom label not applied in render data"
    assert render_data['color'] == (50, 100, 200), "Custom color not applied in render data"
    print("✓ CountdownWidget custom properties work correctly")

    # Test 6: Invalid date format handling
    countdown_widget.set_property('target_date', 'invalid-date-format')
    render_data = countdown_widget.get_render_data()
    assert 'Invalid date format' in render_data['text'], "Invalid date format not handled correctly"
    assert render_data['color'] == (255, 0, 0), "Error color not applied for invalid date"
    print("✓ CountdownWidget handles invalid date format correctly")

    # Test 7: Serialization/Deserialization
    # Reset to a valid date for serialization test
    countdown_widget.set_property('target_date', future_date_str)

    widget_dict = countdown_widget.to_dict()
    assert widget_dict['type'] == 'CountdownWidget', "Serialization type is incorrect"
    assert widget_dict['x'] == 15, "Serialization x position is incorrect"
    assert widget_dict['y'] == 25, "Serialization y position is incorrect"
    assert widget_dict['width'] == 120, "Serialization width is incorrect"
    assert widget_dict['height'] == 40, "Serialization height is incorrect"
    assert 'properties' in widget_dict, "Serialization missing properties"

    restored_widget = CountdownWidget.from_dict(widget_dict)
    assert restored_widget.x == 15, "Deserialization x position is incorrect"
    assert restored_widget.y == 25, "Deserialization y position is incorrect"
    assert restored_widget.width == 120, "Deserialization width is incorrect"
    assert restored_widget.height == 40, "Deserialization height is incorrect"
    assert restored_widget.get_property('target_date') == future_date_str, "Deserialization target_date is incorrect"
    assert restored_widget.get_property('label') == 'My Countdown', "Deserialization label is incorrect"
    assert restored_widget.get_property('color') == (50, 100, 200), "Deserialization color is incorrect"
    print("✓ CountdownWidget serialization/deserialization works correctly")

    # Test 8: Default size calculation
    default_size = countdown_widget.get_default_size(64)
    assert isinstance(default_size, tuple), "Default size is not a tuple"
    assert len(default_size) == 2, "Default size tuple does not have 2 elements"
    assert default_size[0] > 0, "Default width is not positive"
    assert default_size[1] > 0, "Default height is not positive"
    print("✓ CountdownWidget default size calculation works correctly")

    return True


def test_system_stats_widget():
    """Test the SystemStatsWidget functionality."""
    print("\nTesting SystemStatsWidget...")

    # Test 1: Instantiation via plugin manager
    plugin_manager = get_plugin_manager()
    register_plugin(SystemStatsWidgetPlugin())

    stats_widget = plugin_manager.create_widget("SystemStats", x=20, y=30, width=120, height=50)
    assert stats_widget is not None, "Failed to create SystemStatsWidget via plugin manager"
    assert isinstance(stats_widget, SystemStatsWidget), "Created widget is not a SystemStatsWidget instance"
    print("✓ SystemStatsWidget instantiation via plugin manager successful")

    # Test 2: Direct instantiation
    direct_widget = SystemStatsWidget(x=15, y=25, width=100, height=45)
    assert direct_widget.x == 15, "Direct instantiation failed to set x position"
    assert direct_widget.y == 25, "Direct instantiation failed to set y position"
    assert direct_widget.width == 100, "Direct instantiation failed to set width"
    assert direct_widget.height == 45, "Direct instantiation failed to set height"
    print("✓ SystemStatsWidget direct instantiation successful")

    # Test 3: Default properties
    assert stats_widget.get_property('metrics') == ['CPU', 'Memory', 'Disk'], "Default metrics are incorrect"
    assert stats_widget.get_property('color') == (144, 238, 144), "Default color is incorrect"  # Light green
    assert stats_widget.update_interval == 5, "Default update_interval is incorrect"
    print("✓ SystemStatsWidget default properties are correct")

    # Test 4: Render data
    render_data = stats_widget.get_render_data()
    assert render_data['type'] == 'system_stats', "Render data type is incorrect"
    assert 'stats' in render_data, "Render data missing stats field"
    assert 'color' in render_data, "Render data missing color field"
    assert 'x' in render_data and 'y' in render_data, "Render data missing position fields"
    assert 'width' in render_data and 'height' in render_data, "Render data missing size fields"
    assert render_data['x'] == 20, "Render data x position is incorrect"
    assert render_data['y'] == 30, "Render data y position is incorrect"
    assert render_data['width'] == 120, "Render data width is incorrect"
    assert render_data['height'] == 50, "Render data height is incorrect"

    # Verify system stats are within valid ranges
    stats = render_data['stats']
    assert isinstance(stats, dict), "Stats should be a dictionary"
    for metric_name, value in stats.items():
        assert isinstance(value, (int, float)), f"Metric {metric_name} should be numeric"
        assert 0 <= value <= 100, f"Metric {metric_name} value {value} should be between 0 and 100"

    print("✓ SystemStatsWidget render data structure is correct")

    # Test 5: Custom properties
    custom_metrics = ['CPU', 'Memory']
    custom_color = (255, 128, 0)
    custom_interval = 10

    stats_widget.set_property('metrics', custom_metrics)
    stats_widget.set_property('color', custom_color)
    stats_widget.update_interval = custom_interval

    render_data = stats_widget.get_render_data()
    assert len(render_data['stats']) == 2, "Custom metrics not applied correctly"
    assert 'CPU' in render_data['stats'] and 'Memory' in render_data['stats'], "Expected metrics not found"
    assert 'Disk' not in render_data['stats'], "Unexpected metric found in filtered stats"
    assert render_data['color'] == custom_color, "Custom color not applied in render data"
    assert stats_widget.update_interval == custom_interval, "Custom update_interval not applied"
    print("✓ SystemStatsWidget custom properties work correctly")

    # Test 6: System stats validation
    system_stats = stats_widget.get_system_stats()
    assert isinstance(system_stats, dict), "System stats should return a dictionary"

    # Check that required metrics are present
    expected_metrics = ['cpu', 'memory', 'disk']
    for metric in expected_metrics:
        assert metric in system_stats, f"Required metric {metric} not found in system stats"
        assert isinstance(system_stats[metric], (int, float)), f"Metric {metric} should be numeric"
        assert 0 <= system_stats[metric] <= 100, f"Metric {metric} value should be between 0 and 100"

    print("✓ SystemStatsWidget system stats validation passed")

    # Test 7: Serialization/Deserialization
    widget_dict = stats_widget.to_dict()
    assert widget_dict['type'] == 'SystemStats', "Serialization type is incorrect"
    assert widget_dict['x'] == 20, "Serialization x position is incorrect"
    assert widget_dict['y'] == 30, "Serialization y position is incorrect"
    assert widget_dict['width'] == 120, "Serialization width is incorrect"
    assert widget_dict['height'] == 50, "Serialization height is incorrect"
    assert 'properties' in widget_dict, "Serialization missing properties"

    restored_widget = SystemStatsWidget.from_dict(widget_dict)
    assert restored_widget.x == 20, "Deserialization x position is incorrect"
    assert restored_widget.y == 30, "Deserialization y position is incorrect"
    assert restored_widget.width == 120, "Deserialization width is incorrect"
    assert restored_widget.height == 50, "Deserialization height is incorrect"
    assert restored_widget.get_property('metrics') == custom_metrics, "Deserialization metrics are incorrect"
    assert restored_widget.get_property('color') == custom_color, "Deserialization color is incorrect"
    assert restored_widget.update_interval == custom_interval, "Deserialization update_interval is incorrect"
    print("✓ SystemStatsWidget serialization/deserialization works correctly")

    # Test 8: Default size calculation
    default_size = stats_widget.get_default_size(64)
    assert isinstance(default_size, tuple), "Default size is not a tuple"
    assert len(default_size) == 2, "Default size tuple does not have 2 elements"
    assert default_size[0] > 0, "Default width is not positive"
    assert default_size[1] > 0, "Default height is not positive"

    # Test scaling with different screen sizes
    small_size = stats_widget.get_default_size(32)
    large_size = stats_widget.get_default_size(128)
    assert small_size[0] < default_size[0], "Smaller screen should produce smaller width"
    assert default_size[0] < large_size[0], "Larger screen should produce larger width"
    print("✓ SystemStatsWidget default size calculation works correctly")

    # Test 9: Widget validation
    # Test with valid configuration
    errors = stats_widget.validate()
    assert isinstance(errors, list), "Validation should return a list"

    # Test with invalid metrics
    stats_widget.set_property('metrics', [])
    errors = stats_widget.validate()
    assert len(errors) > 0, "Should have validation errors for empty metrics"
    assert any("metric" in error.lower() for error in errors), "Should have metric-related validation error"

    # Test with invalid color
    stats_widget.set_property('metrics', ['CPU', 'Memory', 'Disk'])  # Reset metrics
    stats_widget.set_property('color', (300, 200, 100))  # Invalid color
    errors = stats_widget.validate()
    assert len(errors) > 0, "Should have validation errors for invalid color"
    assert any("color" in error.lower() for error in errors), "Should have color-related validation error"

    print("✓ SystemStatsWidget validation works correctly")

    return True


def test_stopwatch_widget():
    """Test the StopwatchWidget functionality."""
    print("\nTesting StopwatchWidget...")

    # Test 1: Instantiation via plugin manager
    plugin_manager = get_plugin_manager()
    register_plugin(StopwatchWidgetPlugin())

    stopwatch_widget = plugin_manager.create_widget("Stopwatch", x=25, y=35, width=130, height=45)
    assert stopwatch_widget is not None, "Failed to create StopwatchWidget via plugin manager"
    assert isinstance(stopwatch_widget, StopwatchWidget), "Created widget is not a StopwatchWidget instance"
    print("✓ StopwatchWidget instantiation via plugin manager successful")

    # Test 2: Direct instantiation
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


def test_new_widgets():
    """Run all tests for the new widgets."""
    print("Testing new widgets: DateWidget, CountdownWidget, and SystemStatsWidget")
    print("=" * 60)

        success = success and test_stopwatch_widget()
    try:
        success = test_date_widget()
        success = success and test_countdown_widget()
        success = success and test_system_stats_widget()

        if success:
            print("\n" + "=" * 60)
            print("All tests for new widgets passed successfully!")
            return True
        else:
            print("\nSome tests failed!")
            return False

    except Exception as e:
        print(f"\nTest execution failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_new_widgets()
    sys.exit(0 if success else 1)
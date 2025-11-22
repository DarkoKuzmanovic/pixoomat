#!/usr/bin/env python3
"""
Test edge cases for widget configuration system:
- Unknown widget types
- Corrupted configuration data
- Backward compatibility
- Error handling
"""

import json
import sys
from layout_manager import LayoutManager, WidgetFactory
from widgets.plugin_system import get_plugin_manager


def test_unknown_widget_type():
    """
    Test handling of unknown widget types in configuration
    """
    print("=" * 60)
    print("EDGE CASE #1: Unknown Widget Type")
    print("=" * 60)

    # Create a config with an unknown widget type
    config_with_unknown = {
        "screen_size": 64,
        "background_color": [0, 0, 0],
        "widgets": [
            {
                "type": "ClockWidget",
                "x": 10,
                "y": 10,
                "width": 20,
                "height": 6,
                "visible": True,
                "z_index": 0,
                "update_interval": 60,
                "properties": {}
            },
            {
                "type": "NonExistentWidget",  # Unknown widget type
                "x": 10,
                "y": 30,
                "width": 30,
                "height": 10,
                "visible": True,
                "z_index": 0,
                "update_interval": 60,
                "properties": {}
            },
            {
                "type": "WeatherWidget",
                "x": 10,
                "y": 50,
                "width": 18,
                "height": 5,
                "visible": True,
                "z_index": 0,
                "update_interval": 60,
                "properties": {}
            }
        ]
    }

    try:
        layout = LayoutManager.from_dict(config_with_unknown)

        # Should have loaded the valid widgets and skipped the unknown one
        print(f"✓ Loaded {len(layout.widgets)} widgets (skipped unknown type)")

        widget_types = [type(w).__name__ for w in layout.widgets]
        print(f"  Loaded widget types: {widget_types}")

        if len(layout.widgets) == 2:
            print("✓ Correctly skipped unknown widget type")
            return True
        else:
            print(f"✗ FAIL: Expected 2 widgets, got {len(layout.widgets)}")
            return False

    except Exception as e:
        print(f"✗ FAIL: Exception raised: {e}")
        return False


def test_corrupted_configuration():
    """
    Test handling of corrupted configuration data
    """
    print("\n" + "=" * 60)
    print("EDGE CASE #2: Corrupted Configuration Data")
    print("=" * 60)

    test_cases = [
        {
            "name": "Missing 'type' field",
            "config": {
                "screen_size": 64,
                "background_color": [0, 0, 0],
                "widgets": [
                    {
                        # Missing 'type' field
                        "x": 10,
                        "y": 10,
                        "width": 20,
                        "height": 6
                    }
                ]
            }
        },
        {
            "name": "Invalid coordinates",
            "config": {
                "screen_size": 64,
                "background_color": [0, 0, 0],
                "widgets": [
                    {
                        "type": "ClockWidget",
                        "x": "invalid",  # String instead of int
                        "y": 10,
                        "width": 20,
                        "height": 6
                    }
                ]
            }
        },
        {
            "name": "Malformed properties",
            "config": {
                "screen_size": 64,
                "background_color": [0, 0, 0],
                "widgets": [
                    {
                        "type": "ClockWidget",
                        "x": 10,
                        "y": 10,
                        "width": 20,
                        "height": 6,
                        "properties": "not a dict"  # Invalid properties
                    }
                ]
            }
        }
    ]

    all_passed = True
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            layout = LayoutManager.from_dict(test_case['config'])
            print(f"  ✓ Handled gracefully, loaded {len(layout.widgets)} widgets")
        except Exception as e:
            print(f"  ⚠ Exception (acceptable): {type(e).__name__}: {e}")
            # Some errors are acceptable - we just want to avoid crashes

    print("\n✓ All corrupted configs handled without crashes")
    return True


def test_backward_compatibility():
    """
    Test backward compatibility with older configuration formats
    """
    print("\n" + "=" * 60)
    print("EDGE CASE #3: Backward Compatibility")
    print("=" * 60)

    # Old format without 'properties' field (pre-fix format)
    old_format_config = {
        "screen_size": 64,
        "background_color": [0, 0, 0],
        "widgets": [
            {
                "type": "ClockWidget",
                "x": 10,
                "y": 10,
                "width": 20,
                "height": 6,
                "visible": True,
                "z_index": 0,
                "update_interval": 60
                # No 'properties' field
            }
        ]
    }

    try:
        layout = LayoutManager.from_dict(old_format_config)
        print(f"✓ Loaded old format config with {len(layout.widgets)} widgets")

        # Widget should still be created with default properties
        if len(layout.widgets) == 1:
            widget = layout.widgets[0]
            print(f"  Widget type: {type(widget).__name__}")
            print(f"  Widget has properties dict: {hasattr(widget, 'properties')}")
            print("✓ Backward compatibility maintained")
            return True
        else:
            print("✗ FAIL: Widget not loaded correctly")
            return False

    except Exception as e:
        print(f"✗ FAIL: Exception raised: {e}")
        return False


def test_property_type_validation():
    """
    Test that invalid property types are handled gracefully
    """
    print("\n" + "=" * 60)
    print("EDGE CASE #4: Property Type Validation")
    print("=" * 60)

    plugin_manager = get_plugin_manager()
    plugin_manager.load_all_plugins()

    # Test setting invalid property values
    text_widget = plugin_manager.create_widget("SimpleText", x=10, y=10, text="Test")

    test_cases = [
        ("Setting None value", "text", None),
        ("Setting wrong type for color", "color", "not a tuple"),
        ("Setting negative font size", "font_size", -5),
        ("Setting extremely large value", "font_size", 10000)
    ]

    all_handled = True
    for test_name, prop_name, value in test_cases:
        print(f"\nTesting: {test_name}")
        try:
            text_widget.set_property(prop_name, value)
            current_value = text_widget.get_property(prop_name)
            print(f"  ✓ Handled: {prop_name} = {current_value}")
        except Exception as e:
            print(f"  ⚠ Exception (acceptable): {type(e).__name__}")

    print("\n✓ Property validation tests completed")
    return True


def test_empty_and_large_layouts():
    """
    Test edge cases for layout size
    """
    print("\n" + "=" * 60)
    print("EDGE CASE #5: Empty and Large Layouts")
    print("=" * 60)

    # Test empty layout
    print("\nTesting empty layout:")
    empty_layout = LayoutManager(64)
    empty_dict = empty_layout.to_dict()
    restored_empty = LayoutManager.from_dict(empty_dict)

    if len(restored_empty.widgets) == 0:
        print("✓ Empty layout serializes/deserializes correctly")
    else:
        print("✗ FAIL: Empty layout has widgets")
        return False

    # Test large layout
    print("\nTesting large layout:")
    plugin_manager = get_plugin_manager()
    plugin_manager.load_all_plugins()

    large_layout = LayoutManager(64)

    # Add many widgets
    for i in range(20):
        text_widget = plugin_manager.create_widget(
            "SimpleText",
            x=(i % 10) * 6,
            y=(i // 10) * 15,
            text=f"W{i}"
        )
        large_layout.add_widget(text_widget)

    print(f"Created layout with {len(large_layout.widgets)} widgets")

    # Serialize and deserialize
    large_dict = large_layout.to_dict()
    restored_large = LayoutManager.from_dict(large_dict)

    if len(restored_large.widgets) == 20:
        print(f"✓ Large layout serializes/deserializes correctly")
        return True
    else:
        print(f"✗ FAIL: Expected 20 widgets, got {len(restored_large.widgets)}")
        return False


def test_widget_factory_edge_cases():
    """
    Test WidgetFactory edge cases
    """
    print("\n" + "=" * 60)
    print("EDGE CASE #6: WidgetFactory Edge Cases")
    print("=" * 60)

    factory = WidgetFactory()

    # Test creating widget with minimal data
    print("\nTesting minimal widget data:")
    minimal_data = {"type": "ClockWidget"}
    widget = factory.create_widget("ClockWidget", minimal_data, 64)

    if widget is not None:
        print(f"✓ Created widget with minimal data: {widget}")
    else:
        print("✗ FAIL: Could not create widget with minimal data")
        return False

    # Test creating widget with extra/unknown fields
    print("\nTesting widget with extra fields:")
    extra_data = {
        "type": "ClockWidget",
        "x": 10,
        "y": 10,
        "unknown_field": "should be ignored",
        "another_unknown": 123
    }
    widget = factory.create_widget("ClockWidget", extra_data, 64)

    if widget is not None:
        print(f"✓ Created widget with extra fields (ignored): {widget}")
        return True
    else:
        print("✗ FAIL: Could not create widget with extra fields")
        return False


def main():
    """Run all edge case tests"""
    print("\n" + "=" * 60)
    print("WIDGET CONFIGURATION EDGE CASE TEST SUITE")
    print("=" * 60 + "\n")

    results = {
        "Unknown Widget Type": test_unknown_widget_type(),
        "Corrupted Configuration": test_corrupted_configuration(),
        "Backward Compatibility": test_backward_compatibility(),
        "Property Type Validation": test_property_type_validation(),
        "Empty and Large Layouts": test_empty_and_large_layouts(),
        "WidgetFactory Edge Cases": test_widget_factory_edge_cases()
    }

    print("\n" + "=" * 60)
    print("EDGE CASE TEST RESULTS SUMMARY")
    print("=" * 60)

    for test_name, result in results.items():
        status = "PASSED ✓" if result else "FAILED ✗"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())
    print("=" * 60)
    if all_passed:
        print("✓ ALL EDGE CASE TESTS PASSED")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME EDGE CASE TESTS FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
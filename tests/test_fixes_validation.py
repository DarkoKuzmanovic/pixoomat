#!/usr/bin/env python3
"""
Test script to validate the specific widget configuration fixes:
1. Plugin Widget Serialization Failure
2. Inconsistent Property Storage
3. Missing Widget Type Registration
"""

import json
import sys
from layout_manager import LayoutManager, WidgetFactory
from widgets.plugin_system import get_plugin_manager
from widgets import ClockWidget, WeatherWidget


def test_fix_1_plugin_serialization():
    """
    Test Fix #1: Plugin Widget Serialization Failure
    Verify that plugin widgets can be serialized and deserialized correctly
    """
    print("=" * 60)
    print("TEST FIX #1: Plugin Widget Serialization")
    print("=" * 60)

    plugin_manager = get_plugin_manager()
    plugin_manager.load_all_plugins()

    # Create plugin widgets with various properties
    text_widget = plugin_manager.create_widget(
        "SimpleText",
        x=15, y=20,
        text="Serialization Test",
        color=(255, 100, 50),
        font_size=14
    )

    progress_widget = plugin_manager.create_widget(
        "ProgressBar",
        x=5, y=50,
        width=50, height=8,
        progress=0.65,
        foreground_color=(100, 200, 255)
    )

    # Create layout and add widgets
    layout = LayoutManager(64)
    layout.add_widget(text_widget)
    layout.add_widget(progress_widget)

    # Serialize
    serialized = layout.to_dict()
    print(f"✓ Serialized {len(serialized['widgets'])} plugin widgets")

    # Check that properties are in the serialized data
    for widget_data in serialized['widgets']:
        if 'properties' not in widget_data:
            print(f"✗ FAIL: Widget {widget_data['type']} missing 'properties' field")
            return False
        print(f"  - {widget_data['type']}: {len(widget_data['properties'])} properties serialized")

    # Deserialize
    restored_layout = LayoutManager.from_dict(serialized)
    print(f"✓ Deserialized {len(restored_layout.widgets)} plugin widgets")

    # Verify properties were restored
    restored_text = restored_layout.widgets[0]
    restored_progress = restored_layout.widgets[1]

    if restored_text.get_property('text') == "Serialization Test":
        print(f"✓ SimpleText 'text' property correctly restored")
    else:
        print(f"✗ FAIL: SimpleText 'text' property not restored correctly")
        return False

    if abs(restored_progress.get_property('progress') - 0.65) < 0.01:
        print(f"✓ ProgressBar 'progress' property correctly restored")
    else:
        print(f"✗ FAIL: ProgressBar 'progress' property not restored correctly")
        return False

    print("✓ Fix #1 PASSED: Plugin widgets serialize/deserialize correctly\n")
    return True


def test_fix_2_property_storage():
    """
    Test Fix #2: Inconsistent Property Storage
    Verify that properties are stored consistently across all widget types
    """
    print("=" * 60)
    print("TEST FIX #2: Inconsistent Property Storage")
    print("=" * 60)

    plugin_manager = get_plugin_manager()
    plugin_manager.load_all_plugins()

    # Test built-in widgets
    clock = ClockWidget(x=10, y=10)
    weather = WeatherWidget(x=10, y=30)

    # Test plugin widgets
    text = plugin_manager.create_widget("SimpleText", x=10, y=50, text="Test")
    progress = plugin_manager.create_widget("ProgressBar", x=10, y=60, progress=0.5)

    widgets = [
        ("ClockWidget", clock),
        ("WeatherWidget", weather),
        ("SimpleText", text),
        ("ProgressBar", progress)
    ]

    all_consistent = True
    for name, widget in widgets:
        # Check that widget has properties dict
        if not hasattr(widget, 'properties'):
            print(f"✗ FAIL: {name} missing 'properties' attribute")
            all_consistent = False
            continue

        if not isinstance(widget.properties, dict):
            print(f"✗ FAIL: {name} 'properties' is not a dict")
            all_consistent = False
            continue

        # Check that widget has get_property and set_property methods
        if not hasattr(widget, 'get_property') or not hasattr(widget, 'set_property'):
            print(f"✗ FAIL: {name} missing property accessor methods")
            all_consistent = False
            continue

        # Test property access
        widget.set_property('test_key', 'test_value')
        if widget.get_property('test_key') != 'test_value':
            print(f"✗ FAIL: {name} property get/set doesn't work")
            all_consistent = False
            continue

        print(f"✓ {name}: Consistent property storage")

    if all_consistent:
        print("✓ Fix #2 PASSED: All widgets use consistent property storage\n")
    else:
        print("✗ Fix #2 FAILED: Property storage inconsistent\n")

    return all_consistent


def test_fix_3_widget_type_registration():
    """
    Test Fix #3: Missing Widget Type Registration
    Verify that all widget types are properly registered with the factory
    """
    print("=" * 60)
    print("TEST FIX #3: Widget Type Registration")
    print("=" * 60)

    # Load plugins first
    plugin_manager = get_plugin_manager()
    plugin_manager.load_all_plugins()

    # Get widget factory
    factory = WidgetFactory()
    available_types = factory.get_available_widget_types()

    print(f"Available widget types: {available_types}")

    # Expected widget types
    expected_types = ['ClockWidget', 'WeatherWidget', 'SimpleText', 'ProgressBar']

    missing_types = []
    for expected in expected_types:
        if expected not in available_types:
            missing_types.append(expected)
            print(f"✗ FAIL: Widget type '{expected}' not registered")
        else:
            print(f"✓ Widget type '{expected}' registered")

    # Test creating each widget type
    creation_success = True
    for widget_type in available_types:
        test_data = {
            "type": widget_type,
            "x": 5,
            "y": 5,
            "width": 30,
            "height": 15
        }

        widget = factory.create_widget(widget_type, test_data, 64)
        if widget is None:
            print(f"✗ FAIL: Could not create widget of type '{widget_type}'")
            creation_success = False
        else:
            print(f"✓ Successfully created '{widget_type}'")

    if len(missing_types) == 0 and creation_success:
        print("✓ Fix #3 PASSED: All widget types properly registered\n")
        return True
    else:
        print("✗ Fix #3 FAILED: Widget type registration incomplete\n")
        return False


def test_mixed_layout_roundtrip():
    """
    Integration test: Create a complex mixed layout, serialize, deserialize, and verify
    """
    print("=" * 60)
    print("INTEGRATION TEST: Mixed Layout Roundtrip")
    print("=" * 60)

    plugin_manager = get_plugin_manager()
    plugin_manager.load_all_plugins()

    # Create a complex layout
    layout = LayoutManager(64)

    # Add built-in widgets
    clock = ClockWidget(x=2, y=2)
    weather = WeatherWidget(x=2, y=35)
    layout.add_widget(clock)
    layout.add_widget(weather)

    # Add plugin widgets
    text1 = plugin_manager.create_widget("SimpleText", x=25, y=5, text="Title", color=(255, 255, 0))
    text2 = plugin_manager.create_widget("SimpleText", x=25, y=20, text="Subtitle", color=(0, 255, 255))
    progress = plugin_manager.create_widget("ProgressBar", x=5, y=55, width=54, height=6, progress=0.85)

    layout.add_widget(text1)
    layout.add_widget(text2)
    layout.add_widget(progress)

    print(f"Created layout with {len(layout.widgets)} widgets")

    # Serialize
    serialized = layout.to_dict()
    json_str = json.dumps(serialized, indent=2)
    print(f"Serialized to {len(json_str)} characters")

    # Deserialize
    restored = LayoutManager.from_dict(serialized)
    print(f"Restored layout with {len(restored.widgets)} widgets")

    # Verify widget count
    if len(restored.widgets) != len(layout.widgets):
        print(f"✗ FAIL: Widget count mismatch ({len(restored.widgets)} vs {len(layout.widgets)})")
        return False

    # Verify widget types
    original_types = [type(w).__name__ for w in layout.widgets]
    restored_types = [type(w).__name__ for w in restored.widgets]

    if original_types != restored_types:
        print(f"✗ FAIL: Widget types don't match")
        print(f"  Original: {original_types}")
        print(f"  Restored: {restored_types}")
        return False

    print(f"✓ Widget types match: {restored_types}")

    # Verify specific properties
    restored_text1 = restored.widgets[2]  # Third widget (first SimpleText)
    if restored_text1.get_property('text') != "Title":
        print(f"✗ FAIL: Text property not preserved")
        return False

    restored_progress = restored.widgets[4]  # Fifth widget (ProgressBar)
    if abs(restored_progress.get_property('progress') - 0.85) > 0.01:
        print(f"✗ FAIL: Progress property not preserved")
        return False

    print("✓ Properties correctly preserved")
    print("✓ INTEGRATION TEST PASSED: Mixed layout roundtrip successful\n")
    return True


def main():
    """Run all fix validation tests"""
    print("\n" + "=" * 60)
    print("WIDGET CONFIGURATION FIXES VALIDATION TEST SUITE")
    print("=" * 60 + "\n")

    results = {
        "Fix #1 - Plugin Serialization": test_fix_1_plugin_serialization(),
        "Fix #2 - Property Storage": test_fix_2_property_storage(),
        "Fix #3 - Widget Type Registration": test_fix_3_widget_type_registration(),
        "Integration - Mixed Layout": test_mixed_layout_roundtrip()
    }

    print("=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)

    for test_name, result in results.items():
        status = "PASSED ✓" if result else "FAILED ✗"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Test script to verify widget configuration serialization/deserialization fixes
"""

import json
from layout_manager import LayoutManager, WidgetFactory
from widgets.plugin_system import get_plugin_manager

def test_widget_serialization():
    """Test that widgets can be properly serialized and deserialized"""

    print("Testing widget serialization and deserialization...")

    # Test 1: Create layout with built-in widgets
    print("\n1. Testing built-in widgets...")
    layout1 = LayoutManager(64)

    # Add built-in widgets
    from widgets import ClockWidget, WeatherWidget
    clock = ClockWidget(x=5, y=5)
    weather = WeatherWidget(x=5, y=30)

    layout1.add_widget(clock)
    layout1.add_widget(weather)

    # Serialize to dict
    layout1_dict = layout1.to_dict()
    print(f"Built-in layout serialized: {json.dumps(layout1_dict, indent=2)}")

    # Deserialize from dict
    layout1_restored = LayoutManager.from_dict(layout1_dict)
    print(f"Restored built-in widgets: {len(layout1_restored.widgets)}")

    # Test 2: Create layout with plugin widgets
    print("\n2. Testing plugin widgets...")
    layout2 = LayoutManager(64)

    # Get plugin manager and create plugin widgets
    plugin_manager = get_plugin_manager()
    plugin_manager.load_all_plugins()

    # Create plugin widgets
    simple_text = plugin_manager.create_widget("SimpleText", x=10, y=10, text="Test")
    progress_bar = plugin_manager.create_widget("ProgressBar", x=10, y=40, progress=0.7)

    if simple_text:
        layout2.add_widget(simple_text)
        print(f"Added SimpleText widget: {simple_text}")

    if progress_bar:
        layout2.add_widget(progress_bar)
        print(f"Added ProgressBar widget: {progress_bar}")

    # Serialize to dict
    layout2_dict = layout2.to_dict()
    print(f"Plugin layout serialized: {json.dumps(layout2_dict, indent=2)}")

    # Deserialize from dict
    layout2_restored = LayoutManager.from_dict(layout2_dict)
    print(f"Restored plugin widgets: {len(layout2_restored.widgets)}")
    for widget in layout2_restored.widgets:
        print(f"  - {widget.__class__.__name__}: {widget}")

    # Test 3: Test widget factory directly
    print("\n3. Testing WidgetFactory...")
    factory = WidgetFactory()
    available_types = factory.get_available_widget_types()
    print(f"Available widget types: {available_types}")

    # Test creating each widget type
    for widget_type in available_types:
        test_data = {
            "type": widget_type,
            "x": 0,
            "y": 0,
            "width": 50,
            "height": 20
        }

        widget = factory.create_widget(widget_type, test_data, 64)
        if widget:
            print(f"✓ Successfully created {widget_type}: {widget}")
        else:
            print(f"✗ Failed to create {widget_type}")

    # Test 4: Test mixed layout serialization/deserialization
    print("\n4. Testing mixed layout...")
    mixed_layout = LayoutManager(64)

    # Add both built-in and plugin widgets
    if simple_text:
        mixed_layout.add_widget(simple_text)
    if progress_bar:
        mixed_layout.add_widget(progress_bar)
    mixed_layout.add_widget(clock)

    mixed_dict = mixed_layout.to_dict()
    mixed_restored = LayoutManager.from_dict(mixed_dict)

    print(f"Mixed layout - Original: {len(mixed_layout.widgets)} widgets")
    print(f"Mixed layout - Restored: {len(mixed_restored.widgets)} widgets")

    # Verify widget types
    original_types = [type(w).__name__ for w in mixed_layout.widgets]
    restored_types = [type(w).__name__ for w in mixed_restored.widgets]

    print(f"Original types: {original_types}")
    print(f"Restored types: {restored_types}")

    if original_types == restored_types:
        print("✓ Widget types match!")
    else:
        print("✗ Widget types don't match!")

    print("\n✓ All serialization tests completed!")

if __name__ == "__main__":
    test_widget_serialization()
#!/usr/bin/env python3
"""
Test script for the new widget system
"""
import sys
import os

# Add the pixoomat directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from widgets import ClockWidget, WeatherWidget
from layout_manager import LayoutManager


def test_widget_system():
    """Test the new widget system"""
    print("Testing new widget system...")
    
    # Test ClockWidget
    print("\n1. Testing ClockWidget:")
    clock_widget = ClockWidget()
    print(f"Default size: {clock_widget.size}")
    print(f"Position: {clock_widget.position}")
    print(f"Render data: {clock_widget.get_render_data()}")
    
    # Test WeatherWidget
    print("\n2. Testing WeatherWidget:")
    weather_widget = WeatherWidget()
    print(f"Default size: {weather_widget.size}")
    print(f"Position: {weather_widget.position}")
    print(f"Render data: {weather_widget.get_render_data()}")
    
    # Test LayoutManager
    print("\n3. Testing LayoutManager:")
    layout = LayoutManager(64)
    
    # Add widgets
    layout.add_widget(clock_widget)
    layout.add_widget(weather_widget)
    
    print(f"Widget count: {len(layout.widgets)}")
    print(f"Layout validation: {layout.validate_layout()}")
    
    # Test render data
    render_data = layout.get_render_data()
    print(f"Render data widgets: {len(render_data['widgets'])}")
    
    # Test widget positioning
    print("\n4. Testing widget positioning:")
    clock_widget.set_position(10, 10)
    weather_widget.set_position(40, 40)
    
    # Check for widgets at specific positions
    widget_at_10_10 = layout.get_widget_at(10, 10)
    widget_at_40_40 = layout.get_widget_at(40, 40)
    widget_at_20_20 = layout.get_widget_at(20, 20)
    
    print(f"Widget at (10,10): {widget_at_10_10}")
    print(f"Widget at (40,40): {widget_at_40_40}")
    print(f"Widget at (20,20): {widget_at_20_20}")
    
    # Test serialization
    print("\n5. Testing serialization:")
    layout_dict = layout.to_dict()
    print(f"Serialization keys: {list(layout_dict.keys())}")
    print(f"Widget serialization count: {len(layout_dict['widgets'])}")
    
    # Test deserialization
    new_layout = LayoutManager.from_dict(layout_dict)
    print(f"Deserialized widget count: {len(new_layout.widgets)}")
    
    print("\nWidget system test completed successfully!")
    return True


if __name__ == "__main__":
    test_widget_system()
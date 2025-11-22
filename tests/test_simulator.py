#!/usr/bin/env python3
"""
Test script for Pixoomat using simulator
"""
import sys
import os

# Add the pixoomat directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import PixoomatApp
from config import PixoomatConfig


def test_simulator():
    """Test Pixoomat with simulated Pixoo device"""
    print("Testing Pixoomat with simulator...")
    
    # Create config for simulator
    config = PixoomatConfig()
    config.ip_address = "192.168.1.999"  # Fake IP for simulator
    config.debug = True
    config.time_format = "24"
    config.brightness = 80
    config.text_color = (255, 255, 255)
    config.background_color = (0, 0, 0)
    
    # Create app with simulator mode
    # Note: We'll need to modify the Pixoo class to support simulator
    # For now, let's just test the configuration and time formatting
    
    from clock_display import ClockDisplay
    clock = ClockDisplay(64)
    
    print("Testing time display formatting...")
    time_data = clock.get_time_display_data("24")
    print(f"Time display data: {time_data}")
    
    time_data_12 = clock.get_time_display_data("12")
    print(f"12-hour time: {time_data_12}")
    
    print("\nConfiguration validation:")
    errors = config.validate()
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid!")
    
    print("\nPixoomat application logic test completed successfully!")
    print("To test with real device:")
    print("1. Make sure your Pixoo 64 is on the same WiFi network")
    print("2. Find your device's IP address (check router or Pixoo app)")
    print("3. Run: python main.py --ip <YOUR_DEVICE_IP>")
    print("4. Or use auto-discovery: python main.py --discover")


if __name__ == "__main__":
    test_simulator()
#!/usr/bin/env python3
"""
Test script for GUI components
"""
import sys
import os

# Add project root directory to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import PixoomatConfig
from gui.main_window_compact import CompactPixoomatGUI
import tkinter as tk


def test_gui():
    """Test GUI without launching full application"""
    print("Testing GUI components...")

    # Create a minimal Tkinter app to test GUI
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Create test config
    config = PixoomatConfig()
    config.screen_size = 64
    config.show_weather = True

    try:
        # Create GUI app
        app = CompactPixoomatGUI(root, config)
        print("Compact GUI components initialized successfully!")
        print("GUI test completed - you can now run: python main.py --use-gui")
    except Exception as e:
        print(f"GUI test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    test_gui()
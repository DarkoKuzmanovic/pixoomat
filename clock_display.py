"""
Clock display functionality for Pixoomat
"""
import datetime
import math
from typing import Optional, Tuple


class ClockDisplay:
    """Handles time formatting and display rendering for Pixoo device"""

    def __init__(self, screen_size: int = 64):
        self.screen_size = screen_size
        self.center_x = screen_size // 2
        self.center_y = screen_size // 2

    def format_time(self, time_format: str = "24") -> str:
        """Format current time according to specified format"""
        now = datetime.datetime.now()

        if time_format == "12":
            return now.strftime("%I:%M %p")
        else:  # 24-hour format
            return now.strftime("%H:%M")

    def calculate_text_position(self, text: str, font_width: int = 4, font_height: int = 6) -> Tuple[int, int]:
        """Calculate centered position for text on screen"""
        # Estimate text width based on character count and font
        text_width = len(text) * font_width
        text_height = font_height

        # Calculate centered position
        x = max(0, self.center_x - text_width // 2)
        y = max(0, self.center_y - text_height // 2)

        return x, y

    def get_time_display_data(self, time_format: str = "24") -> dict:
        """Get formatted time and position data for display"""
        time_str = self.format_time(time_format)
        x, y = self.calculate_text_position(time_str)

        return {
            'text': time_str,
            'x': x,
            'y': y,
            'format': time_format
        }

    def get_date_display_data(self) -> dict:
        """Get current date for optional display"""
        now = datetime.datetime.now()
        date_str = now.strftime("%m/%d")
        x, y = self.calculate_text_position(date_str)

        return {
            'text': date_str,
            'x': x,
            'y': y + 10  # Position below time
        }

    def get_weather_display_data(self, weather_data: dict) -> Optional[dict]:
        """Get weather display data"""
        if not weather_data:
            return None

        temp = round(weather_data.get('temperature', 0))
        text = f"{temp}°C"

        # Calculate position (bottom right)
        text_width = len(text) * 4
        x = self.screen_size - text_width - 2
        y = self.screen_size - 8

        return {
            'text': text,
            'x': x,
            'y': y,
            'code': weather_data.get('weathercode', 0)
        }

    def get_seconds_indicator(self) -> dict:
        """Get visual seconds indicator (optional feature)"""
        now = datetime.datetime.now()
        seconds = now.second

        # Create a simple progress bar for seconds
        bar_width = int((seconds / 60) * (self.screen_size - 10))
        bar_x = 5
        bar_y = self.screen_size - 8

        return {
            'x': bar_x,
            'y': bar_y,
            'width': bar_width,
            'height': 2
        }

    def should_update_display(self, last_update: datetime.datetime, interval: int) -> bool:
        """Check if display should be updated based on interval"""
        now = datetime.datetime.now()
        return (now - last_update).total_seconds() >= interval
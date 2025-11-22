"""
Weather widget implementation for Pixoomat
Displays current weather information
"""
import datetime
from typing import Dict, Any, Tuple, Optional

from .base_widget import BaseWidget


class WeatherWidget(BaseWidget):
    """Widget for displaying current weather"""
    
    def __init__(self, x: int = 0, y: int = 0, width: int = None, height: int = None, screen_size: int = 64):
        """
        Initialize weather widget
        
        Args:
            x: X position on screen
            y: Y position on screen
            width: Widget width in pixels (None for default)
            height: Widget height in pixels (None for default)
            screen_size: Screen size in pixels
        """
        super().__init__(x, y, width, height, screen_size)
    
    def _init_properties(self):
        """Initialize weather-specific properties"""
        self.set_property('temperature_unit', 'C')  # 'C' or 'F'
        self.set_property('show_icon', True)  # Show weather icon if supported
        self.set_property('font_size', 3)  # Smaller font for weather
        self.set_property('text_color', (255, 255, 255))  # RGB color
        self.set_property('background_color', None)  # None for transparent
        self.set_property('location', None)  # None for auto-detect
        self.set_property('api_provider', 'open-meteo')  # Weather API provider
        
        # Weather update interval should be longer than time
        self.update_interval = 1800  # 30 minutes default
    
    def get_default_size(self, screen_size: int) -> Tuple[int, int]:
        """
        Get default size for weather widget based on screen size
        
        Args:
            screen_size: Screen size in pixels
            
        Returns:
            Default (width, height) tuple
        """
        # Weather text is typically like "23°C" (4 chars) or "73°F" (4 chars)
        font_size = self.get_property('font_size', 3)
        width = 6 * font_size  # Allow some extra space
        height = font_size + 2  # Add some padding
        
        return (min(width, screen_size), min(height, screen_size))
    
    def format_temperature(self, temperature: float) -> str:
        """
        Format temperature according to widget settings
        
        Args:
            temperature: Temperature in Celsius
            
        Returns:
            Formatted temperature string
        """
        unit = self.get_property('temperature_unit', 'C')
        
        if unit == 'F':
            # Convert to Fahrenheit
            temperature = (temperature * 9/5) + 32
            unit_symbol = '°F'
        else:
            unit_symbol = '°C'
        
        return f"{round(temperature)}{unit_symbol}"
    
    def get_weather_data(self) -> Optional[Dict[str, Any]]:
        """
        Get weather data from the weather service
        
        Returns:
            Weather data dictionary or None if unavailable
        """
        # This method will be implemented to interface with the WeatherService
        # For now, return None to indicate no data available
        return None
    
    def get_render_data(self) -> Dict[str, Any]:
        """
        Get data needed for rendering the weather widget
        
        Returns:
            Dictionary containing render information
        """
        weather_data = self.get_weather_data()
        
        if not weather_data:
            # Show placeholder when no data available
            weather_text = "--°C"
        else:
            temperature = weather_data.get('temperature', 0)
            weather_text = self.format_temperature(temperature)
        
        text_color = self.get_property('text_color', (255, 255, 255))
        background_color = self.get_property('background_color', None)
        
        render_data = {
            'type': 'text',
            'text': weather_text,
            'x': self.x,
            'y': self.y,
            'color': text_color,
            'background_color': background_color
        }
        
        # Add weather code if available for potential future icon rendering
        if weather_data and 'weathercode' in weather_data:
            render_data['weather_code'] = weather_data['weathercode']
        
        return render_data
    
    def validate(self) -> list[str]:
        """
        Validate weather widget configuration
        
        Returns:
            List of validation error messages
        """
        errors = super().validate()
        
        temp_unit = self.get_property('temperature_unit', 'C')
        if temp_unit not in ['C', 'F']:
            errors.append("Temperature unit must be 'C' or 'F'")
        
        text_color = self.get_property('text_color', (255, 255, 255))
        if (len(text_color) != 3 or 
            any(not isinstance(c, int) or c < 0 or c > 255 for c in text_color)):
            errors.append("Text color must be RGB values between 0 and 255")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert weather widget to dictionary representation"""
        data = super().to_dict()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WeatherWidget':
        """Create weather widget from dictionary representation"""
        widget = super().from_dict(data)
        # Note: Properties are already set by the base class method
        return widget
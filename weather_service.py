"""
Weather service for Pixoomat
Handles location detection and weather data fetching
"""
import json
import time
import urllib.request
import urllib.error
import threading
from typing import Optional, Tuple, Dict


class WeatherService:
    """Service to fetch weather data from Open-Meteo"""

    def __init__(self, cache_duration: int = 1800):
        self.cache_duration = cache_duration  # Default 30 minutes
        self.last_fetch = 0
        self.cached_weather = None
        self.location = None
        self._update_thread = None
        self._is_updating = False

    def get_location(self) -> Optional[Tuple[float, float]]:
        """Get location from IP-API"""
        if self.location:
            return self.location

        try:
            # Set timeout to avoid hanging
            with urllib.request.urlopen("http://ip-api.com/json/", timeout=5) as response:
                data = json.loads(response.read().decode())
                if data['status'] == 'success':
                    self.location = (data['lat'], data['lon'])
                    return self.location
        except Exception as e:
            print(f"ERROR: Failed to get location: {e}")
            return None

    def get_weather(self, lat: Optional[float] = None, lon: Optional[float] = None) -> Optional[Dict]:
        """Get current weather for location (non-blocking)"""
        # Check if we need an update
        if time.time() - self.last_fetch > self.cache_duration:
            # Start update in background if not already running
            if not self._is_updating:
                self._is_updating = True
                self._update_thread = threading.Thread(
                    target=self._fetch_weather_sync,
                    args=(lat, lon),
                    daemon=True
                )
                self._update_thread.start()

        return self.cached_weather

    def _fetch_weather_sync(self, lat: Optional[float] = None, lon: Optional[float] = None):
        """Synchronous weather fetch to be run in thread"""
        try:
            # Determine location
            if lat is None or lon is None:
                loc = self.get_location()
                if not loc:
                    return
                lat, lon = loc

            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                if 'current_weather' in data:
                    self.cached_weather = data['current_weather']
                    self.last_fetch = time.time()
        except Exception as e:
            print(f"ERROR: Failed to get weather: {e}")
        finally:
            self._is_updating = False

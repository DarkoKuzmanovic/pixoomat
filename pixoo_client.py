"""
Custom Pixoo client wrapper
"""
from pixoo import Pixoo

class CustomPixoo(Pixoo):
    """Custom Pixoo class to support non-standard ports"""
    def __init__(self, address, size=64, debug=False, refresh_connection_automatically=True, port=80):
        self.port = port
        super().__init__(address, size, debug, refresh_connection_automatically)
        # Override the base_url to include the port
        self.base_url = f'http://{address}:{port}/post'

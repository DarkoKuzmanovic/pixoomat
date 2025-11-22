"""
Plugins directory for Pixoomat widgets.

This package contains widget plugins that extend the functionality
of the Pixoomat application.
"""

# Import all plugins to make them discoverable
from .simple_text import SimpleTextPlugin
from .progress_bar import ProgressBarPlugin

__all__ = ['SimpleTextPlugin', 'ProgressBarPlugin']
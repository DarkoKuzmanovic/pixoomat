"""
Main toolbar for Pixoomat GUI with consolidated controls
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable


class MainToolbar:
    """Main toolbar with frequently used actions"""

    def __init__(self, parent, on_action: Optional[Callable] = None):
        """
        Initialize main toolbar

        Args:
            parent: Parent tkinter widget
            on_action: Callback function for toolbar actions
        """
        self.parent = parent
        self.on_action = on_action

        # Create toolbar frame
        self.frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)

        # Create toolbar buttons
        self._setup_toolbar()

    def _setup_toolbar(self):
        """Setup toolbar buttons"""
        # File actions
        ttk.Button(
            self.frame,
            text="New",
            command=lambda: self._on_action("new_layout"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(
            self.frame,
            text="Open",
            command=lambda: self._on_action("open_layout"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(
            self.frame,
            text="Save",
            command=lambda: self._on_action("save_layout"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Edit actions
        ttk.Button(
            self.frame,
            text="Undo",
            command=lambda: self._on_action("undo"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(
            self.frame,
            text="Redo",
            command=lambda: self._on_action("redo"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(
            self.frame,
            text="Duplicate",
            command=lambda: self._on_action("duplicate_widget"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Device actions
        self.connect_button = ttk.Button(
            self.frame,
            text="Connect",
            command=lambda: self._on_action("toggle_connection"),
            width=8
        )
        self.connect_button.pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(
            self.frame,
            text="Apply",
            command=lambda: self._on_action("apply_to_device"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # View actions
        ttk.Button(
            self.frame,
            text="Zoom In",
            command=lambda: self._on_action("zoom_in"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(
            self.frame,
            text="Zoom Out",
            command=lambda: self._on_action("zoom_out"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(
            self.frame,
            text="Reset",
            command=lambda: self._on_action("reset_zoom"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Layout actions
        ttk.Button(
            self.frame,
            text="Front",
            command=lambda: self._on_action("bring_to_front"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(
            self.frame,
            text="Back",
            command=lambda: self._on_action("send_to_back"),
            width=8
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Add keyboard shortcuts info
        shortcuts_frame = ttk.Frame(self.frame)
        shortcuts_frame.pack(side=tk.RIGHT, padx=10)

        ttk.Label(
            shortcuts_frame,
            text="Shortcuts: Ctrl+Z (Undo) | Ctrl+Y (Redo) | Del (Delete) | F1 (Help)",
            font=('Arial', 8)
        ).pack()

    def _on_action(self, action: str):
        """Handle toolbar action"""
        if self.on_action:
            self.on_action(action)

    def set_connection_state(self, connected: bool):
        """Update connection button state"""
        if connected:
            self.connect_button.config(text="Disconnect")
        else:
            self.connect_button.config(text="Connect")
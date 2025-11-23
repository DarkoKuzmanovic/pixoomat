"""
Enhanced main toolbar for Pixoomat GUI with improved visual design and functionality
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Dict, Any


class MainToolbar:
    """Enhanced main toolbar with icons, tooltips, state management, and accessibility"""

    # Button configuration with icons, tooltips, and metadata
    BUTTON_CONFIGS = {
        'new_layout': {
            'action_id': 'new_layout',
            'text': 'New',
            'icon': '📄',
            'tooltip': 'Create new layout (Ctrl+N)',
            'shortcut': 'Ctrl+N',
            'category': 'file',
            'mnemonic': 'N'
        },
        'open_layout': {
            'action_id': 'open_layout',
            'text': 'Open',
            'icon': '📂',
            'tooltip': 'Open layout file (Ctrl+O)',
            'shortcut': 'Ctrl+O',
            'category': 'file',
            'mnemonic': 'O'
        },
        'save_layout': {
            'action_id': 'save_layout',
            'text': 'Save',
            'icon': '💾',
            'tooltip': 'Save layout (Ctrl+S)',
            'shortcut': 'Ctrl+S',
            'category': 'file',
            'mnemonic': 'S'
        },
        'undo': {
            'action_id': 'undo',
            'text': 'Undo',
            'icon': '↶',
            'tooltip': 'Undo last action (Ctrl+Z)',
            'shortcut': 'Ctrl+Z',
            'category': 'edit',
            'mnemonic': 'U',
            'state_dependent': True
        },
        'redo': {
            'action_id': 'redo',
            'text': 'Redo',
            'icon': '↷',
            'tooltip': 'Redo last action (Ctrl+Y)',
            'shortcut': 'Ctrl+Y',
            'category': 'edit',
            'mnemonic': 'R',
            'state_dependent': True
        },
        'duplicate_widget': {
            'action_id': 'duplicate_widget',
            'text': 'Duplicate',
            'icon': '📋',
            'tooltip': 'Duplicate selected widget (Ctrl+D)',
            'shortcut': 'Ctrl+D',
            'category': 'edit',
            'mnemonic': 'D',
            'selection_dependent': True
        },
        'delete_widget': {
            'action_id': 'delete_widget',
            'text': 'Delete',
            'icon': '🗑️',
            'tooltip': 'Delete selected widget (Delete)',
            'shortcut': 'Delete',
            'category': 'edit',
            'mnemonic': 'L',
            'selection_dependent': True
        },
        'toggle_connection': {
            'action_id': 'toggle_connection',
            'text': 'Connect',
            'icon': '🔌',
            'tooltip': 'Connect to device',
            'category': 'device',
            'mnemonic': 'C'
        },
        'apply_to_device': {
            'action_id': 'apply_to_device',
            'text': 'Apply',
            'icon': '📱',
            'tooltip': 'Apply layout to device',
            'category': 'device',
            'mnemonic': 'A',
            'connection_dependent': True
        },
        'zoom_in': {
            'action_id': 'zoom_in',
            'text': 'Zoom In',
            'icon': '🔍+',
            'tooltip': 'Zoom in (Ctrl++)',
            'shortcut': 'Ctrl++',
            'category': 'view',
            'mnemonic': 'I'
        },
        'zoom_out': {
            'action_id': 'zoom_out',
            'text': 'Zoom Out',
            'icon': '🔍-',
            'tooltip': 'Zoom out (Ctrl+-)',
            'shortcut': 'Ctrl+-',
            'category': 'view',
            'mnemonic': 'O'
        },
        'reset_zoom': {
            'action_id': 'reset_zoom',
            'text': 'Reset',
            'icon': '🔍',
            'tooltip': 'Reset zoom (Ctrl+0)',
            'shortcut': 'Ctrl+0',
            'category': 'view',
            'mnemonic': 'R'
        },
        'bring_to_front': {
            'action_id': 'bring_to_front',
            'text': 'Front',
            'icon': '⬆️',
            'tooltip': 'Bring widget to front (Ctrl+Home)',
            'shortcut': 'Ctrl+Home',
            'category': 'layout',
            'mnemonic': 'F',
            'selection_dependent': True
        },
        'send_to_back': {
            'action_id': 'send_to_back',
            'text': 'Back',
            'icon': '⬇️',
            'tooltip': 'Send widget to back (Ctrl+End)',
            'shortcut': 'Ctrl+End',
            'category': 'layout',
            'mnemonic': 'B',
            'selection_dependent': True
        }
    }

    def __init__(self, parent, on_action: Optional[Callable] = None, status_callback: Optional[Callable] = None):
        """
        Initialize enhanced main toolbar

        Args:
            parent: Parent tkinter widget
            on_action: Callback function for toolbar actions
            status_callback: Callback function for status updates
        """
        self.parent = parent
        self.on_action = on_action
        self.status_callback = status_callback

        # State tracking
        self.connected = False
        self.device_info = None
        self.can_undo = False
        self.can_redo = False
        self.has_selection = False
        self.high_contrast = False

        # Button references for state management
        self.buttons = {}
        self.connect_button = None
        self.connection_indicator = None

        # Create toolbar frame
        self.frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)

        # Create toolbar buttons
        self._setup_toolbar()

    def _setup_toolbar(self):
        """Setup toolbar buttons with enhanced features"""
        # Create toolbar sections
        self._setup_file_buttons()
        self._add_separator()
        self._setup_edit_buttons()
        self._add_separator()
        self._setup_device_buttons()
        self._add_separator()
        self._setup_view_buttons()
        self._add_separator()
        self._setup_layout_buttons()

        # Add connection status indicator
        self._setup_connection_indicator()

        # Add keyboard shortcuts info
        self._setup_shortcuts_info()

    def _setup_file_buttons(self):
        """Setup file operation buttons"""
        file_buttons = ['new_layout', 'open_layout', 'save_layout']
        for button_id in file_buttons:
            self.buttons[button_id] = self._create_button(
                self.frame,
                self.BUTTON_CONFIGS[button_id]
            )

    def _setup_edit_buttons(self):
        """Setup edit operation buttons"""
        edit_buttons = ['undo', 'redo', 'duplicate_widget', 'delete_widget']
        for button_id in edit_buttons:
            self.buttons[button_id] = self._create_button(
                self.frame,
                self.BUTTON_CONFIGS[button_id]
            )

    def _setup_device_buttons(self):
        """Setup device operation buttons"""
        for button_id in ['toggle_connection', 'apply_to_device']:
            button = self._create_button(
                self.frame,
                self.BUTTON_CONFIGS[button_id]
            )
            self.buttons[button_id] = button

            # Store reference to connect button for state updates
            if button_id == 'toggle_connection':
                self.connect_button = button

    def _setup_view_buttons(self):
        """Setup view operation buttons"""
        view_buttons = ['zoom_in', 'zoom_out', 'reset_zoom']
        for button_id in view_buttons:
            self.buttons[button_id] = self._create_button(
                self.frame,
                self.BUTTON_CONFIGS[button_id]
            )

    def _setup_layout_buttons(self):
        """Setup layout operation buttons"""
        layout_buttons = ['bring_to_front', 'send_to_back']
        for button_id in layout_buttons:
            self.buttons[button_id] = self._create_button(
                self.frame,
                self.BUTTON_CONFIGS[button_id]
            )

    def _create_button(self, parent, config: Dict[str, Any]) -> ttk.Button:
        """
        Factory method for creating consistent toolbar buttons

        Args:
            parent: Parent widget
            config: Button configuration dictionary

        Returns:
            Created button widget
        """
        # Create button with icon and text
        button_text = f"{config['icon']} {config['text']}"

        # Create tooltip text with shortcut if available
        tooltip_text = config['tooltip']

        # Create button with mnemonic support
        button = ttk.Button(
            parent,
            text=button_text,
            command=lambda: self._on_action(config['action_id']),
            style='Toolbar.TButton'
        )

        # Add tooltip
        self._create_tooltip(button, tooltip_text)

        # Add mnemonic if specified
        if 'mnemonic' in config:
            # Store mnemonic for keyboard navigation using a dictionary
            if not hasattr(self, '_mnemonics'):
                self._mnemonics = {}
            self._mnemonics[button] = config['mnemonic']

        # Pack button with consistent styling
        button.pack(side=tk.LEFT, padx=3, pady=3)

        return button

    def _create_tooltip(self, widget, text: str):
        """
        Create tooltip for a widget

        Args:
            widget: Widget to add tooltip to
            text: Tooltip text
        """
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(
                tooltip,
                text=text,
                background="lightyellow",
                relief=tk.SOLID,
                borderwidth=1,
                font=("Arial", 9)
            )
            label.pack()

            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _add_separator(self):
        """Add visual separator between button groups"""
        separator = ttk.Separator(self.frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)

    def _setup_connection_indicator(self):
        """Setup visual connection status indicator"""
        indicator_frame = ttk.Frame(self.frame)
        indicator_frame.pack(side=tk.LEFT, padx=10)

        # Connection status label
        ttk.Label(indicator_frame, text="Device:").pack(side=tk.LEFT)

        # Status indicator (colored circle)
        self.connection_indicator = tk.Canvas(
            indicator_frame,
            width=12,
            height=12,
            highlightthickness=0
        )
        self.connection_indicator.pack(side=tk.LEFT, padx=3)

        # Initial state (disconnected)
        self._update_connection_indicator(False)

        # Device info label
        self.device_info_label = ttk.Label(indicator_frame, text="Not connected")
        self.device_info_label.pack(side=tk.LEFT)

    def _setup_shortcuts_info(self):
        """Setup keyboard shortcuts information"""
        shortcuts_frame = ttk.Frame(self.frame)
        shortcuts_frame.pack(side=tk.RIGHT, padx=10)

        # Create a more compact shortcuts display
        shortcuts_text = "F1:Help | Ctrl+Z:Undo | Ctrl+Y:Redo | Del:Delete"
        ttk.Label(
            shortcuts_frame,
            text=shortcuts_text,
            font=('Arial', 8),
            foreground='gray'
        ).pack()

    def _update_connection_indicator(self, connected: bool):
        """Update the visual connection status indicator"""
        if self.connection_indicator:
            self.connection_indicator.delete("all")

            # Draw colored circle
            color = "#00aa00" if connected else "#aa0000"  # Green if connected, red if disconnected
            self.connection_indicator.create_oval(
                2, 2, 10, 10,
                fill=color,
                outline="black"
            )

    def _get_action_from_text(self, text: str) -> str:
        """Convert button text to action ID"""
        action_map = {
            'New': 'new_layout',
            'Open': 'open_layout',
            'Save': 'save_layout',
            'Undo': 'undo',
            'Redo': 'redo',
            'Duplicate': 'duplicate_widget',
            'Delete': 'delete_widget',
            'Connect': 'toggle_connection',
            'Disconnect': 'toggle_connection',
            'Apply': 'apply_to_device',
            'Zoom In': 'zoom_in',
            'Zoom Out': 'zoom_out',
            'Reset': 'reset_zoom',
            'Front': 'bring_to_front',
            'Back': 'send_to_back'
        }
        return action_map.get(text, text.lower().replace(' ', '_'))

    def _on_action(self, action: str):
        """
        Enhanced action handling with error handling and status updates

        Args:
            action: Action identifier
        """
        try:
            # Update status
            if self.status_callback:
                action_text = action.replace('_', ' ').title()
                self.status_callback(f"Executing: {action_text}")

            # Call the action callback
            if self.on_action:
                self.on_action(action)

        except Exception as e:
            # Handle errors gracefully
            error_msg = f"Error executing {action}: {str(e)}"
            if self.status_callback:
                self.status_callback(error_msg)
            messagebox.showerror("Toolbar Error", error_msg)

    def set_connection_state(self, connected: bool, device_info: Optional[str] = None):
        """
        Update connection state with enhanced visual feedback

        Args:
            connected: Whether device is connected
            device_info: Optional device information string
        """
        self.connected = connected
        self.device_info = device_info

        # Update connection button
        if self.connect_button:
            if connected:
                self.connect_button.config(text="🔌 Disconnect")
            else:
                self.connect_button.config(text="🔌 Connect")

        # Update connection indicator
        self._update_connection_indicator(connected)

        # Update device info label
        if hasattr(self, 'device_info_label'):
            if connected and device_info:
                self.device_info_label.config(text=device_info)
            elif connected:
                self.device_info_label.config(text="Connected")
            else:
                self.device_info_label.config(text="Not connected")

        # Update connection-dependent buttons
        self._update_connection_dependent_buttons()

    def set_undo_redo_state(self, can_undo: bool, can_redo: bool):
        """
        Update undo/redo button states

        Args:
            can_undo: Whether undo is available
            can_redo: Whether redo is available
        """
        self.can_undo = can_undo
        self.can_redo = can_redo

        # Update button states
        if 'undo' in self.buttons:
            self.buttons['undo'].config(state=tk.NORMAL if can_undo else tk.DISABLED)

        if 'redo' in self.buttons:
            self.buttons['redo'].config(state=tk.NORMAL if can_redo else tk.DISABLED)

    def set_widget_selection_state(self, has_selection: bool):
        """
        Update selection-dependent button states

        Args:
            has_selection: Whether a widget is selected
        """
        self.has_selection = has_selection

        # Update selection-dependent buttons
        selection_dependent = ['duplicate_widget', 'delete_widget', 'bring_to_front', 'send_to_back']
        for button_id in selection_dependent:
            if button_id in self.buttons:
                self.buttons[button_id].config(
                    state=tk.NORMAL if has_selection else tk.DISABLED
                )

    def _update_connection_dependent_buttons(self):
        """Update buttons that depend on connection state"""
        connection_dependent = ['apply_to_device']
        for button_id in connection_dependent:
            if button_id in self.buttons:
                self.buttons[button_id].config(
                    state=tk.NORMAL if self.connected else tk.DISABLED
                )

    def set_high_contrast(self, high_contrast: bool):
        """
        Set high contrast mode for accessibility

        Args:
            high_contrast: Whether to use high contrast mode
        """
        self.high_contrast = high_contrast
        # Note: ttk themes are more complex to change dynamically
        # This is a placeholder for high contrast implementation
        pass

    def update_status(self, message: str):
        """
        Update status via callback

        Args:
            message: Status message
        """
        if self.status_callback:
            self.status_callback(message)

    def enable_all_buttons(self):
        """Enable all toolbar buttons"""
        for button in self.buttons.values():
            button.config(state=tk.NORMAL)

    def disable_all_buttons(self):
        """Disable all toolbar buttons"""
        for button in self.buttons.values():
            button.config(state=tk.DISABLED)
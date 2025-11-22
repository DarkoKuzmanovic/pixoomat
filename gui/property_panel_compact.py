"""
Tabbed property panel for editing widget properties with compact layout
"""
import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Optional

from widgets.base_widget import BaseWidget
from widgets.clock_widget import ClockWidget
from widgets.weather_widget import WeatherWidget


class CompactPropertyPanel:
    """Tabbed panel for editing selected widget properties"""

    def __init__(self, parent, on_property_changed=None):
        """
        Initialize property panel

        Args:
            parent: Parent tkinter widget
            on_property_changed: Callback function when properties change
        """
        self.parent = parent
        self.on_property_changed = on_property_changed
        self.current_widget = None
        self.compact_mode = True

        # Create main frame
        self.frame = ttk.Frame(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components"""
        # Title
        self.title_label = ttk.Label(self.frame, text="Properties", font=('Arial', 10, 'bold'))
        self.title_label.pack(anchor=tk.W, pady=(0, 5))

        # Compact mode toggle
        self.compact_var = tk.BooleanVar(value=True)
        compact_check = ttk.Checkbutton(
            self.frame,
            text="Compact Mode",
            variable=self.compact_var,
            command=self._toggle_compact_mode
        )
        compact_check.pack(anchor=tk.W, pady=(0, 5))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_frame, text="Basic")

        self.appearance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.appearance_frame, text="Appearance")

        self.advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_frame, text="Advanced")

        # Initial empty message
        self.empty_label = ttk.Label(
            self.basic_frame,
            text="Select a widget to edit its properties"
        )
        self.empty_label.pack(pady=20)

    def _toggle_compact_mode(self):
        """Toggle between compact and full property display"""
        self.compact_mode = self.compact_var.get()
        if self.current_widget:
            self.set_widget(self.current_widget)

    def set_widget(self, widget: Optional[BaseWidget] = None):
        """
        Set the widget to edit

        Args:
            widget: Widget to edit or None to clear
        """
        self.current_widget = widget

        # Clear current properties
        self._clear_all_tabs()

        if not widget:
            self.title_label.config(text="No Widget Selected")
            self.empty_label = ttk.Label(
                self.basic_frame,
                text="Select a widget to edit its properties"
            )
            self.empty_label.pack(pady=20)
            return

        # Set title
        widget_type = widget.__class__.__name__.replace("Widget", "")
        self.title_label.config(text=f"{widget_type} Properties")

        # Create property editors based on widget type
        if hasattr(widget, 'get_property_schema'):
            self._create_dynamic_properties(widget)
        elif isinstance(widget, ClockWidget):
            self._create_clock_properties(widget)
        elif isinstance(widget, WeatherWidget):
            self._create_weather_properties(widget)
        else:
            self._create_base_properties(widget)

    def _clear_all_tabs(self):
        """Clear all tab frames"""
        for tab_frame in [self.basic_frame, self.appearance_frame, self.advanced_frame]:
            for child in tab_frame.winfo_children():
                child.destroy()

    def _create_base_properties(self, widget: BaseWidget):
        """Create property editors for base widget properties"""
        # Basic tab - Position and Size
        if self.compact_mode:
            # Compact layout - position and size in same row
            pos_frame = ttk.Frame(self.basic_frame)
            pos_frame.pack(fill=tk.X, pady=10)

            ttk.Label(pos_frame, text="X:").pack(side=tk.LEFT)
            x_var = tk.IntVar(value=widget.x)
            x_entry = ttk.Entry(pos_frame, textvariable=x_var, width=6)
            x_entry.pack(side=tk.LEFT, padx=(5, 10))

            ttk.Label(pos_frame, text="Y:").pack(side=tk.LEFT)
            y_var = tk.IntVar(value=widget.y)
            y_entry = ttk.Entry(pos_frame, textvariable=y_var, width=6)
            y_entry.pack(side=tk.LEFT, padx=5)

            ttk.Label(pos_frame, text="W:").pack(side=tk.LEFT, padx=(10, 0))
            width_var = tk.IntVar(value=widget.width)
            width_entry = ttk.Entry(pos_frame, textvariable=width_var, width=6)
            width_entry.pack(side=tk.LEFT, padx=(5, 10))

            ttk.Label(pos_frame, text="H:").pack(side=tk.LEFT)
            height_var = tk.IntVar(value=widget.height)
            height_entry = ttk.Entry(pos_frame, textvariable=height_var, width=6)
            height_entry.pack(side=tk.LEFT, padx=5)
        else:
            # Full layout
            ttk.Label(self.basic_frame, text="Position:").pack(anchor=tk.W, pady=(10, 5))

            pos_frame = ttk.Frame(self.basic_frame)
            pos_frame.pack(fill=tk.X, pady=(0, 10))

            ttk.Label(pos_frame, text="X:").pack(side=tk.LEFT)
            x_var = tk.IntVar(value=widget.x)
            x_entry = ttk.Entry(pos_frame, textvariable=x_var, width=10)
            x_entry.pack(side=tk.LEFT, padx=(5, 10))

            ttk.Label(pos_frame, text="Y:").pack(side=tk.LEFT)
            y_var = tk.IntVar(value=widget.y)
            y_entry = ttk.Entry(pos_frame, textvariable=y_var, width=10)
            y_entry.pack(side=tk.LEFT, padx=5)

            # Size
            ttk.Label(self.basic_frame, text="Size:").pack(anchor=tk.W, pady=(0, 5))

            size_frame = ttk.Frame(self.basic_frame)
            size_frame.pack(fill=tk.X, pady=(0, 10))

            ttk.Label(size_frame, text="Width:").pack(side=tk.LEFT)
            width_var = tk.IntVar(value=widget.width)
            width_entry = ttk.Entry(size_frame, textvariable=width_var, width=10)
            width_entry.pack(side=tk.LEFT, padx=(5, 10))

            ttk.Label(size_frame, text="Height:").pack(side=tk.LEFT)
            height_var = tk.IntVar(value=widget.height)
            height_entry = ttk.Entry(size_frame, textvariable=height_var, width=10)
            height_entry.pack(side=tk.LEFT, padx=5)

        # Advanced tab - Z-index and Update interval
        z_frame = ttk.Frame(self.advanced_frame)
        z_frame.pack(fill=tk.X, pady=10)

        ttk.Label(z_frame, text="Z-Index:").pack(side=tk.LEFT)
        z_var = tk.IntVar(value=widget.z_index)
        z_spinbox = ttk.Spinbox(
            z_frame,
            from_=0,
            to=99,
            textvariable=z_var,
            width=8
        )
        z_spinbox.pack(side=tk.LEFT, padx=5)

        interval_frame = ttk.Frame(self.advanced_frame)
        interval_frame.pack(fill=tk.X, pady=10)

        ttk.Label(interval_frame, text="Update (s):").pack(side=tk.LEFT)
        interval_var = tk.IntVar(value=widget.update_interval)
        interval_entry = ttk.Entry(interval_frame, textvariable=interval_var, width=8)
        interval_entry.pack(side=tk.LEFT, padx=5)

        # Basic tab - Visible checkbox
        visible_var = tk.BooleanVar(value=widget.visible)
        visible_check = ttk.Checkbutton(
            self.basic_frame,
            text="Visible",
            variable=visible_var
        )
        visible_check.pack(anchor=tk.W, pady=10)

        # Bind change events
        def on_change():
            try:
                x_pos = int(x_var.get()) if x_var.get() else 0
                y_pos = int(y_var.get()) if y_var.get() else 0
                width_val = int(width_var.get()) if width_var.get() else widget.width
                height_val = int(height_var.get()) if height_var.get() else widget.height
                z_val = int(z_var.get()) if z_var.get() else widget.z_index
                interval_val = int(interval_var.get()) if interval_var.get() else widget.update_interval
                visible_val = bool(visible_var.get())

                widget.set_position(x_pos, y_pos)
                widget.set_size(width_val, height_val)
                widget.z_index = z_val
                widget.update_interval = interval_val
                widget.visible = visible_val

                if self.on_property_changed:
                    self.on_property_changed(widget)
            except (ValueError, tk.TclError) as e:
                print(f"Property change error: {e}")

        x_var.trace('w', lambda *args: on_change())
        y_var.trace('w', lambda *args: on_change())
        width_var.trace('w', lambda *args: on_change())
        height_var.trace('w', lambda *args: on_change())
        z_var.trace('w', lambda *args: on_change())
        interval_var.trace('w', lambda *args: on_change())
        visible_var.trace('w', lambda *args: on_change())

    def _create_dynamic_properties(self, widget):
        """Create property editors based on widget schema"""
        # First create base properties
        self._create_base_properties(widget)

        # Add widget-specific properties to appropriate tabs
        schema = widget.get_property_schema()

        for prop_name, prop_info in schema.items():
            label_text = prop_info.get('label', prop_name.capitalize())
            prop_type = prop_info.get('type', 'string')

            # Determine which tab based on property type
            if prop_name in ['text_color', 'background_color', 'font_size']:
                tab_frame = self.appearance_frame
            elif prop_name in ['update_interval', 'z_index', 'visible']:
                tab_frame = self.advanced_frame
            else:
                tab_frame = self.basic_frame

            current_value = widget.get_property(prop_name)
            if current_value is None:
                current_value = prop_info.get('default')

            if prop_type == 'color':
                self._create_color_editor(tab_frame, prop_name, label_text, current_value, widget)
            elif prop_type == 'boolean':
                self._create_boolean_editor(tab_frame, prop_name, label_text, current_value, widget, prop_info.get('description', ''))
            elif prop_type == 'integer':
                self._create_integer_editor(tab_frame, prop_name, label_text, current_value, widget, prop_info)
            else:
                self._create_string_editor(tab_frame, prop_name, label_text, current_value, widget)

    def _create_color_editor(self, parent, prop_name, label_text, current_value, widget):
        """Create visual color editor with color chooser dialog"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text=f"{label_text}:").pack(anchor=tk.W)

        # Color display frame
        color_frame = ttk.Frame(frame)
        color_frame.pack(fill=tk.X, pady=(2, 0))

        # Extract RGB values from current_value
        if isinstance(current_value, (list, tuple)):
            if len(current_value) >= 3:
                r, g, b = current_value[:3]  # Take first 3 values for RGB
            else:
                r, g, b = 255, 255, 255  # Default white
        else:
            r, g, b = 255, 255, 255  # Default for non-list/tuple values

        # Create color swatch
        color_var = tk.StringVar(value=f"#{r:02x}{g:02x}{b:02x}")
        color_swatch = tk.Label(
            color_frame,
            bg=color_var.get(),
            width=10,
            relief=tk.RAISED,
            borderwidth=2
        )
        color_swatch.pack(side=tk.LEFT, padx=(0, 5))

        # Create color picker button
        color_button = ttk.Button(
            color_frame,
            text="Choose Color",
            command=lambda: self._choose_color(prop_name, color_var, color_swatch, widget)
        )
        color_button.pack(side=tk.LEFT)

        # Function to update color swatch
        def update_swatch():
            color_swatch.config(bg=color_var.get())

        color_var.trace('w', lambda *args: update_swatch())

    def _choose_color(self, prop_name, color_var, color_swatch, widget):
        """Open color chooser dialog and update color when selected"""
        # Get current color
        current_color = color_var.get()

        # Open color chooser dialog
        result = colorchooser.askcolor(
            color=current_color,
            title=f"Choose {prop_name.replace('_', ' ').title()}"
        )

        # If a color was selected (not cancelled)
        if result[0]:  # result[0] contains the RGB tuple
            r, g, b = result[0]
            hex_color = result[1]  # result[1] contains the hex string

            # Update color variable and swatch
            color_var.set(hex_color)
            color_swatch.config(bg=hex_color)

            # Update widget property with RGB tuple
            widget.set_property(prop_name, (int(r), int(g), int(b)))

            # Trigger property change callback
            if self.on_property_changed:
                self.on_property_changed(widget)

    def _create_boolean_editor(self, parent, prop_name, label_text, current_value, widget, description):
        """Create boolean editor"""
        var = tk.BooleanVar(value=bool(current_value))
        check = ttk.Checkbutton(parent, text=description or label_text, variable=var)
        check.pack(anchor=tk.W, pady=2)

        def on_change():
            widget.set_property(prop_name, var.get())
            if self.on_property_changed:
                self.on_property_changed(widget)

        var.trace('w', lambda *args: on_change())

    def _create_integer_editor(self, parent, prop_name, label_text, current_value, widget, prop_info):
        """Create integer editor"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text=f"{label_text}:").pack(anchor=tk.W)

        min_val = prop_info.get('min', -9999)
        max_val = prop_info.get('max', 9999)

        var = tk.IntVar(value=int(current_value) if current_value is not None else 0)
        spin = ttk.Spinbox(frame, from_=min_val, to=max_val, textvariable=var)
        spin.pack(fill=tk.X, pady=(2, 0))

        def on_change():
            try:
                widget.set_property(prop_name, var.get())
                if self.on_property_changed:
                    self.on_property_changed(widget)
            except Exception as e:
                print(f"Integer property change error: {e}")

        var.trace('w', lambda *args: on_change())

    def _create_string_editor(self, parent, prop_name, label_text, current_value, widget):
        """Create string editor"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text=f"{label_text}:").pack(anchor=tk.W)

        var = tk.StringVar(value=str(current_value) if current_value is not None else "")
        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(fill=tk.X, pady=(2, 0))

        def on_change():
            try:
                widget.set_property(prop_name, var.get())
                if self.on_property_changed:
                    self.on_property_changed(widget)
            except Exception as e:
                print(f"String property change error: {e}")

        var.trace('w', lambda *args: on_change())

    def _create_clock_properties(self, widget: ClockWidget):
        """Create property editors specific to ClockWidget"""
        self._create_base_properties(widget)

        # Clock-specific properties
        # Basic tab - Time format
        time_format = widget.get_property('time_format', '24')
        time_format_var = tk.StringVar(value=time_format)

        time_frame = ttk.Frame(self.basic_frame)
        time_frame.pack(fill=tk.X, pady=10)

        ttk.Label(time_frame, text="Format:").pack(side=tk.LEFT)

        ttk.Radiobutton(
            time_frame,
            text="24h",
            variable=time_format_var,
            value="24"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            time_frame,
            text="12h",
            variable=time_format_var,
            value="12"
        ).pack(side=tk.LEFT, padx=5)

        # Basic tab - Show seconds
        show_seconds = widget.get_property('show_seconds', False)
        show_seconds_var = tk.BooleanVar(value=show_seconds)
        show_seconds_check = ttk.Checkbutton(
            self.basic_frame,
            text="Show Seconds",
            variable=show_seconds_var
        )
        show_seconds_check.pack(anchor=tk.W, pady=5)

        # Appearance tab - Font size and text color
        font_size = widget.get_property('font_size', 4)
        font_size_var = tk.IntVar(value=font_size)

        font_frame = ttk.Frame(self.appearance_frame)
        font_frame.pack(fill=tk.X, pady=10)

        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        font_spinbox = ttk.Spinbox(
            font_frame,
            from_=2,
            to=8,
            textvariable=font_size_var,
            width=8
        )
        font_spinbox.pack(side=tk.LEFT, padx=5)

        # Text color
        text_color = widget.get_property('text_color', (255, 255, 255))
        self._create_color_editor(self.appearance_frame, 'text_color', 'Text Color', text_color, widget)

        # Bind change events
        def on_clock_change():
            widget.set_property('time_format', time_format_var.get())
            widget.set_property('show_seconds', show_seconds_var.get())
            widget.set_property('font_size', font_size_var.get())

            if self.on_property_changed:
                self.on_property_changed(widget)

        time_format_var.trace('w', lambda *args: on_clock_change())
        show_seconds_var.trace('w', lambda *args: on_clock_change())
        font_size_var.trace('w', lambda *args: on_clock_change())

    def _create_weather_properties(self, widget: WeatherWidget):
        """Create property editors specific to WeatherWidget"""
        self._create_base_properties(widget)

        # Basic tab - Temperature unit
        temp_unit = widget.get_property('temperature_unit', 'C')
        temp_unit_var = tk.StringVar(value=temp_unit)

        temp_frame = ttk.Frame(self.basic_frame)
        temp_frame.pack(fill=tk.X, pady=10)

        ttk.Label(temp_frame, text="Unit:").pack(side=tk.LEFT)

        ttk.Radiobutton(
            temp_frame,
            text="°C",
            variable=temp_unit_var,
            value="C"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            temp_frame,
            text="°F",
            variable=temp_unit_var,
            value="F"
        ).pack(side=tk.LEFT, padx=5)

        # Appearance tab - Font size and text color
        font_size = widget.get_property('font_size', 3)
        font_size_var = tk.IntVar(value=font_size)

        font_frame = ttk.Frame(self.appearance_frame)
        font_frame.pack(fill=tk.X, pady=10)

        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        font_spinbox = ttk.Spinbox(
            font_frame,
            from_=2,
            to=6,
            textvariable=font_size_var,
            width=8
        )
        font_spinbox.pack(side=tk.LEFT, padx=5)

        # Text color
        text_color = widget.get_property('text_color', (255, 255, 255))
        self._create_color_editor(self.appearance_frame, 'text_color', 'Text Color', text_color, widget)

        # Bind change events
        def on_weather_change():
            widget.set_property('temperature_unit', temp_unit_var.get())
            widget.set_property('font_size', font_size_var.get())

            if self.on_property_changed:
                self.on_property_changed(widget)

        temp_unit_var.trace('w', lambda *args: on_weather_change())
        font_size_var.trace('w', lambda *args: on_weather_change())
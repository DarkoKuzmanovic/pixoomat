"""
Property panel for editing widget properties in the GUI
"""
import tkinter as tk
from tkinter import ttk

from widgets.base_widget import BaseWidget


class PropertyPanel:
    """Panel for editing selected widget properties"""

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

        # Create main frame
        self.frame = ttk.Frame(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components"""
        # Title label
        self.title_label = ttk.Label(self.frame, text="No Widget Selected", font=('Arial', 10, 'bold'))
        self.title_label.pack(anchor=tk.W, pady=(0, 10))

        # Property container
        self.property_frame = ttk.Frame(self.frame)
        self.property_frame.pack(fill=tk.BOTH, expand=True)

        # Initial empty message
        self.empty_label = ttk.Label(
            self.property_frame,
            text="Select a widget to edit its properties"
        )
        self.empty_label.pack(pady=20)

    def set_widget(self, widget: BaseWidget = None):
        """
        Set the widget to edit

        Args:
            widget: Widget to edit or None to clear
        """
        self.current_widget = widget

        # Clear current properties
        for child in self.property_frame.winfo_children():
            child.destroy()

        if not widget:
            self.title_label.config(text="No Widget Selected")
            self.empty_label = ttk.Label(
                self.property_frame,
                text="Select a widget to edit its properties"
            )
            self.empty_label.pack(pady=20)
            return

        # Set title
        widget_type = widget.__class__.__name__.replace("Widget", "")
        self.title_label.config(text=f"{widget_type} Properties")

        # Create specific property editors based on widget type
        if hasattr(widget, 'get_property_schema'):
            self._create_dynamic_properties(widget)
        elif widget.__class__.__name__ == 'ClockWidget' or 'Clock' in widget.__class__.__name__:
            self._create_clock_properties(widget)
        elif widget.__class__.__name__ == 'WeatherWidget' or 'Weather' in widget.__class__.__name__:
            self._create_weather_properties(widget)
        else:
            self._create_base_properties(widget)

    def _create_dynamic_properties(self, widget):
        """Create property editors based on widget schema"""
        # First create base properties (position, size, etc.)
        self._create_base_properties(widget)

        # Separator
        ttk.Separator(self.property_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(self.property_frame, text="Widget Settings", font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        schema = widget.get_property_schema()

        for prop_name, prop_info in schema.items():
            label_text = prop_info.get('label', prop_name.capitalize())
            prop_type = prop_info.get('type', 'string')
            description = prop_info.get('description', '')

            # Container for this property
            frame = ttk.Frame(self.property_frame)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(frame, text=f"{label_text}:").pack(anchor=tk.W)

            current_value = widget.get_property(prop_name)
            if current_value is None:
                current_value = prop_info.get('default')

            if prop_type == 'string':
                var = tk.StringVar(value=str(current_value))
                entry = ttk.Entry(frame, textvariable=var)
                entry.pack(fill=tk.X, pady=(2, 0))

                def on_string_change(name=prop_name, v=var):
                    widget.set_property(name, v.get())
                    if self.on_property_changed:
                        self.on_property_changed(widget)

                entry.bind('<FocusOut>', lambda e, n=prop_name, v=var: on_string_change(n, v))
                entry.bind('<Return>', lambda e, n=prop_name, v=var: on_string_change(n, v))

            elif prop_type == 'integer':
                var = tk.IntVar(value=int(current_value) if current_value is not None else 0)

                min_val = prop_info.get('min', -9999)
                max_val = prop_info.get('max', 9999)

                spin = ttk.Spinbox(frame, from_=min_val, to=max_val, textvariable=var)
                spin.pack(fill=tk.X, pady=(2, 0))

                def on_int_change(name=prop_name, v=var):
                    try:
                        widget.set_property(name, v.get())
                        if self.on_property_changed:
                            self.on_property_changed(widget)
                    except:
                        pass

                spin.bind('<FocusOut>', lambda e, n=prop_name, v=var: on_int_change(n, v))
                spin.bind('<Return>', lambda e, n=prop_name, v=var: on_int_change(n, v))
                spin.config(command=lambda n=prop_name, v=var: on_int_change(n, v))

            elif prop_type == 'boolean':
                var = tk.BooleanVar(value=bool(current_value))
                check = ttk.Checkbutton(frame, text=description or label_text, variable=var)
                check.pack(anchor=tk.W)

                def on_bool_change(name=prop_name, v=var):
                    widget.set_property(name, v.get())
                    if self.on_property_changed:
                        self.on_property_changed(widget)

                check.config(command=lambda n=prop_name, v=var: on_bool_change(n, v))

            elif prop_type == 'color':
                # Simple color entry for now (R,G,B)
                if isinstance(current_value, (list, tuple)):
                    color_str = f"{current_value[0]},{current_value[1]},{current_value[2]}"
                else:
                    color_str = "255,255,255"

                var = tk.StringVar(value=color_str)
                entry = ttk.Entry(frame, textvariable=var)
                entry.pack(fill=tk.X, pady=(2, 0))
                ttk.Label(frame, text="Format: R,G,B (e.g. 255,0,0)", font=('Arial', 8)).pack(anchor=tk.W)

                def on_color_change(name=prop_name, v=var):
                    try:
                        parts = [int(x.strip()) for x in v.get().split(',')]
                        if len(parts) == 3:
                            widget.set_property(name, tuple(parts))
                            if self.on_property_changed:
                                self.on_property_changed(widget)
                    except:
                        pass

                entry.bind('<FocusOut>', lambda e, n=prop_name, v=var: on_color_change(n, v))
                entry.bind('<Return>', lambda e, n=prop_name, v=var: on_color_change(n, v))

    def _create_base_properties(self, widget: BaseWidget):
        """Create property editors for base widget properties"""
        # Position
        ttk.Label(self.property_frame, text="Position:").pack(anchor=tk.W, pady=(10, 5))

        pos_frame = ttk.Frame(self.property_frame)
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
        ttk.Label(self.property_frame, text="Size:").pack(anchor=tk.W, pady=(0, 5))

        size_frame = ttk.Frame(self.property_frame)
        size_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(size_frame, text="Width:").pack(side=tk.LEFT)
        width_var = tk.IntVar(value=widget.width)
        width_entry = ttk.Entry(size_frame, textvariable=width_var, width=10)
        width_entry.pack(side=tk.LEFT, padx=(5, 10))

        ttk.Label(size_frame, text="Height:").pack(side=tk.LEFT)
        height_var = tk.IntVar(value=widget.height)
        height_entry = ttk.Entry(size_frame, textvariable=height_var, width=10)
        height_entry.pack(side=tk.LEFT, padx=5)

        # Z-index
        ttk.Label(self.property_frame, text="Z-Index:").pack(anchor=tk.W, pady=(0, 5))
        z_var = tk.IntVar(value=widget.z_index)
        z_spinbox = ttk.Spinbox(
            self.property_frame,
            from_=0,
            to=99,
            textvariable=z_var,
            width=10
        )
        z_spinbox.pack(anchor=tk.W, pady=(0, 10))

        # Update interval
        ttk.Label(self.property_frame, text="Update Interval (seconds):").pack(anchor=tk.W, pady=(0, 5))
        interval_var = tk.IntVar(value=widget.update_interval)
        interval_entry = ttk.Entry(self.property_frame, textvariable=interval_var, width=10)
        interval_entry.pack(anchor=tk.W, pady=(0, 10))

        # Visible checkbox
        visible_var = tk.BooleanVar(value=widget.visible)
        visible_check = ttk.Checkbutton(
            self.property_frame,
            text="Visible",
            variable=visible_var
        )
        visible_check.pack(anchor=tk.W, pady=(0, 10))

        # Bind change events
        def on_change():
            widget.set_position(x_var.get(), y_var.get())
            widget.set_size(width_var.get(), height_var.get())
            widget.z_index = z_var.get()
            widget.update_interval = interval_var.get()
            widget.visible = visible_var.get()

            if self.on_property_changed:
                self.on_property_changed(widget)

        x_var.trace('w', lambda *args: on_change())
        y_var.trace('w', lambda *args: on_change())
        width_var.trace('w', lambda *args: on_change())
        height_var.trace('w', lambda *args: on_change())
        z_var.trace('w', lambda *args: on_change())
        interval_var.trace('w', lambda *args: on_change())
        visible_var.trace('w', lambda *args: on_change())

    def _create_clock_properties(self, widget: BaseWidget):
        """Create property editors specific to ClockWidget"""
        self._create_base_properties(widget)

        # Separator
        ttk.Separator(self.property_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Clock-specific properties
        ttk.Label(self.property_frame, text="Clock Settings:").pack(anchor=tk.W, pady=(0, 10))

        # Time format
        time_format = widget.get_property('time_format', '24')
        time_format_var = tk.StringVar(value=time_format)

        time_frame = ttk.Frame(self.property_frame)
        time_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(time_frame, text="Format:").pack(side=tk.LEFT)

        format_frame = ttk.Frame(time_frame)
        format_frame.pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            format_frame,
            text="24-hour",
            variable=time_format_var,
            value="24"
        ).pack(side=tk.LEFT)

        ttk.Radiobutton(
            format_frame,
            text="12-hour",
            variable=time_format_var,
            value="12"
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Show seconds
        show_seconds = widget.get_property('show_seconds', False)
        show_seconds_var = tk.BooleanVar(value=show_seconds)
        show_seconds_check = ttk.Checkbutton(
            self.property_frame,
            text="Show Seconds",
            variable=show_seconds_var
        )
        show_seconds_check.pack(anchor=tk.W, pady=(0, 10))

        # Font size
        font_size = widget.get_property('font_size', 4)
        font_size_var = tk.IntVar(value=font_size)

        font_frame = ttk.Frame(self.property_frame)
        font_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        font_spinbox = ttk.Spinbox(
            font_frame,
            from_=2,
            to=8,
            textvariable=font_size_var,
            width=10
        )
        font_spinbox.pack(side=tk.LEFT, padx=5)

        # Text color
        text_color = widget.get_property('text_color', (255, 255, 255))
        color_frame = ttk.Frame(self.property_frame)
        color_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(color_frame, text="Text Color:").pack(anchor=tk.W, pady=(0, 5))

        rgb_frame = ttk.Frame(color_frame)
        rgb_frame.pack(fill=tk.X)

        r_var = tk.IntVar(value=text_color[0])
        g_var = tk.IntVar(value=text_color[1])
        b_var = tk.IntVar(value=text_color[2])

        ttk.Label(rgb_frame, text="R:").pack(side=tk.LEFT)
        r_spinbox = ttk.Spinbox(rgb_frame, from_=0, to=255, textvariable=r_var, width=5)
        r_spinbox.pack(side=tk.LEFT, padx=(5, 10))

        ttk.Label(rgb_frame, text="G:").pack(side=tk.LEFT)
        g_spinbox = ttk.Spinbox(rgb_frame, from_=0, to=255, textvariable=g_var, width=5)
        g_spinbox.pack(side=tk.LEFT, padx=5)

        ttk.Label(rgb_frame, text="B:").pack(side=tk.LEFT)
        b_spinbox = ttk.Spinbox(rgb_frame, from_=0, to=255, textvariable=b_var, width=5)
        b_spinbox.pack(side=tk.LEFT, padx=5)

        # Bind change events
        def on_clock_change():
            widget.set_property('time_format', time_format_var.get())
            widget.set_property('show_seconds', show_seconds_var.get())
            widget.set_property('font_size', font_size_var.get())
            widget.set_property('text_color', (r_var.get(), g_var.get(), b_var.get()))

            if self.on_property_changed:
                self.on_property_changed(widget)

        time_format_var.trace('w', lambda *args: on_clock_change())
        show_seconds_var.trace('w', lambda *args: on_clock_change())
        font_size_var.trace('w', lambda *args: on_clock_change())
        r_var.trace('w', lambda *args: on_clock_change())
        g_var.trace('w', lambda *args: on_clock_change())
        b_var.trace('w', lambda *args: on_clock_change())

    def _create_weather_properties(self, widget: BaseWidget):
        """Create property editors specific to WeatherWidget"""
        self._create_base_properties(widget)

        # Separator
        ttk.Separator(self.property_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Weather-specific properties
        ttk.Label(self.property_frame, text="Weather Settings:").pack(anchor=tk.W, pady=(0, 10))

        # Temperature unit
        temp_unit = widget.get_property('temperature_unit', 'C')
        temp_unit_var = tk.StringVar(value=temp_unit)

        temp_frame = ttk.Frame(self.property_frame)
        temp_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(temp_frame, text="Temperature Unit:").pack(side=tk.LEFT)

        unit_frame = ttk.Frame(temp_frame)
        unit_frame.pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(
            unit_frame,
            text="Celsius",
            variable=temp_unit_var,
            value="C"
        ).pack(side=tk.LEFT)

        ttk.Radiobutton(
            unit_frame,
            text="Fahrenheit",
            variable=temp_unit_var,
            value="F"
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Font size
        font_size = widget.get_property('font_size', 3)
        font_size_var = tk.IntVar(value=font_size)

        font_frame = ttk.Frame(self.property_frame)
        font_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        font_spinbox = ttk.Spinbox(
            font_frame,
            from_=2,
            to=6,
            textvariable=font_size_var,
            width=10
        )
        font_spinbox.pack(side=tk.LEFT, padx=5)

        # Text color
        text_color = widget.get_property('text_color', (255, 255, 255))
        color_frame = ttk.Frame(self.property_frame)
        color_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(color_frame, text="Text Color:").pack(anchor=tk.W, pady=(0, 5))

        rgb_frame = ttk.Frame(color_frame)
        rgb_frame.pack(fill=tk.X)

        r_var = tk.IntVar(value=text_color[0])
        g_var = tk.IntVar(value=text_color[1])
        b_var = tk.IntVar(value=text_color[2])

        ttk.Label(rgb_frame, text="R:").pack(side=tk.LEFT)
        r_spinbox = ttk.Spinbox(rgb_frame, from_=0, to=255, textvariable=r_var, width=5)
        r_spinbox.pack(side=tk.LEFT, padx=(5, 10))

        ttk.Label(rgb_frame, text="G:").pack(side=tk.LEFT)
        g_spinbox = ttk.Spinbox(rgb_frame, from_=0, to=255, textvariable=g_var, width=5)
        g_spinbox.pack(side=tk.LEFT, padx=5)

        ttk.Label(rgb_frame, text="B:").pack(side=tk.LEFT)
        b_spinbox = ttk.Spinbox(rgb_frame, from_=0, to=255, textvariable=b_var, width=5)
        b_spinbox.pack(side=tk.LEFT, padx=5)

        # Bind change events
        def on_weather_change():
            widget.set_property('temperature_unit', temp_unit_var.get())
            widget.set_property('font_size', font_size_var.get())
            widget.set_property('text_color', (r_var.get(), g_var.get(), b_var.get()))

            if self.on_property_changed:
                self.on_property_changed(widget)

        temp_unit_var.trace('w', lambda *args: on_weather_change())
        font_size_var.trace('w', lambda *args: on_weather_change())
        r_var.trace('w', lambda *args: on_weather_change())
        g_var.trace('w', lambda *args: on_weather_change())
        b_var.trace('w', lambda *args: on_weather_change())
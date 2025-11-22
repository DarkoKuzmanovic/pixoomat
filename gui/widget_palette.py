"""
Widget palette with grid layout and icons for compact display
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, List, Dict, Any
from widgets import ClockWidget, WeatherWidget, get_plugin_manager


class WidgetPalette:
    """Compact widget palette with grid layout"""

    def __init__(self, parent, on_widget_add: Optional[Callable] = None):
        """
        Initialize widget palette

        Args:
            parent: Parent tkinter widget
            on_widget_add: Callback function when widget is added
        """
        self.parent = parent
        self.on_widget_add = on_widget_add
        self.widgets_info = []

        # Create main frame
        self.frame = ttk.Frame(parent)

        # Create UI components
        self._setup_ui()

        # Load available widgets
        self._load_widgets()

    def _setup_ui(self):
        """Setup UI components"""
        # Title
        title_label = ttk.Label(self.frame, text="Widgets", font=('Arial', 10, 'bold'))
        title_label.pack(anchor=tk.W, pady=(0, 5))

        # Create scrollable frame for widget grid
        canvas = tk.Canvas(self.frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Widget grid frame
        self.grid_frame = ttk.Frame(self.scrollable_frame)
        self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _load_widgets(self):
        """Load available widgets and create grid buttons"""
        # Clear existing widgets
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.widgets_info = []

        # Built-in widgets
        self.widgets_info.extend([
            {
                'name': 'Clock',
                'class': ClockWidget,
                'icon': '⏰',
                'tooltip': 'Add Clock Widget',
                'category': 'Display'
            },
            {
                'name': 'Weather',
                'class': WeatherWidget,
                'icon': '🌤️',
                'tooltip': 'Add Weather Widget',
                'category': 'Data'
            }
        ])

        # Plugin widgets
        try:
            plugin_manager = get_plugin_manager()
            plugin_widgets = plugin_manager.list_plugins()

            for plugin_meta in plugin_widgets:
                self.widgets_info.append({
                    'name': plugin_meta.name,
                    'class': plugin_manager.create_widget,
                    'icon': '🔌',
                    'tooltip': f'Add {plugin_meta.name}',
                    'category': 'Plugin'
                })
        except Exception as e:
            print(f"Warning: Failed to load plugin widgets: {e}")

        # Create grid buttons
        self._create_widget_grid()

    def _create_widget_grid(self):
        """Create grid of widget buttons"""
        row = 0
        col = 0
        max_cols = 3  # 3 columns for compact display

        for widget_info in self.widgets_info:
            # Create button frame
            btn_frame = ttk.Frame(self.grid_frame, relief=tk.RAISED, borderwidth=1)
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            # Icon label (using text as icon substitute)
            icon_label = ttk.Label(
                btn_frame,
                text=widget_info['icon'],
                font=('Arial', 16)
            )
            icon_label.pack(pady=(5, 2))

            # Widget name button
            btn = ttk.Button(
                btn_frame,
                text=widget_info['name'],
                command=lambda wi=widget_info: self._add_widget(wi),
                width=12
            )
            btn.pack(pady=(0, 5))

            # Add tooltip
            self._create_tooltip(btn, widget_info['tooltip'])

            # Grid layout
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Configure grid weights
        for i in range(max_cols):
            self.grid_frame.columnconfigure(i, weight=1)

    def _create_tooltip(self, widget, text):
        """Create tooltip for widget"""
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
                font=('Arial', 9)
            )
            label.pack()

            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _add_widget(self, widget_info):
        """Add widget to layout"""
        try:
            if callable(widget_info['class']):
                # Plugin widget
                widget = widget_info['class'](widget_info['name'])
            else:
                # Built-in widget
                widget = widget_info['class']()

            if self.on_widget_add:
                self.on_widget_add(widget)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create widget: {e}")

    def _on_action(self, action: str):
        """Handle palette action"""
        if self.on_widget_add:
            # Pass action to parent for handling
            self.on_widget_add(('action', action))
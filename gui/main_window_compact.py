"""
Compact main GUI window for Pixoomat with improved layout and accessibility
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import copy
from typing import Optional, Union, Tuple

from layout_manager import LayoutManager
from widgets import get_plugin_manager
from config import PixoomatConfig
from gui.property_panel_compact import CompactPropertyPanel
from gui.device_panel_compact import CompactDevicePanel
from gui.widget_palette import WidgetPalette
from gui.toolbar import MainToolbar
from gui.file_operations import FileOperations
from gui.undo_manager import UndoManager
from weather_service import WeatherService


def run_gui(config: PixoomatConfig) -> int:
    """
    Run compact GUI application

    Args:
        config: PixoomatConfig instance

    Returns:
        Exit code
    """
    root = tk.Tk()
    app = CompactPixoomatGUI(root, config)
    root.mainloop()
    return 0


class CompactPixoomatGUI:
    """Compact main GUI application class with improved layout"""

    def __init__(self, root: tk.Tk, config: PixoomatConfig):
        """
        Initialize compact GUI

        Args:
            root: Tkinter root window
            config: PixoomatConfig instance
        """
        self.root = root
        self.config = config

        # Initialize layout manager
        self.layout_manager = LayoutManager(config.screen_size)

        # GUI elements
        self.selected_widget = None
        self.drag_data = {"x": 0, "y": 0, "widget": None}
        self.pixoo = None
        self.weather_service = WeatherService()

        # Zoom and canvas settings
        self.zoom_level = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0

        # Theme settings
        self.high_contrast = False
        self.theme_colors = {
            'normal': {
                'bg': '#f0f0f0',
                'fg': '#000000',
                'canvas_bg': '#2b2b2b',
                'select': '#0078d4'
            },
            'high_contrast': {
                'bg': '#000000',
                'fg': '#ffffff',
                'canvas_bg': '#000000',
                'select': '#ffff00'
            }
        }

        # Create component managers
        self.property_panel = None
        self.device_panel = None
        self.widget_palette = None
        self.toolbar = None
        self.file_ops = None
        self.undo_manager = UndoManager()

        # Setup window
        self._setup_window()

        # Setup GUI components
        self._setup_menu()
        self._setup_toolbar()
        self._setup_main_area()

        # Load layout if specified
        if config.layout_config:
            self._load_layout(config.layout_config)
        else:
            self._setup_default_layout()

        # Setup keyboard shortcuts
        self._setup_keyboard_shortcuts()

    def _setup_window(self):
        """Setup main window properties"""
        self.root.title("Pixoomat - Compact Layout Designer")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        # Apply theme
        self._apply_theme()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_bar = ttk.Label(self.status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Zoom controls in status bar
        zoom_frame = ttk.Frame(self.status_frame)
        zoom_frame.pack(side=tk.RIGHT, padx=5)

        ttk.Label(zoom_frame, text="Zoom:").pack(side=tk.LEFT)

        self.zoom_var = tk.StringVar(value=f"{int(self.zoom_level * 100)}%")
        self.zoom_label = ttk.Label(zoom_frame, textvariable=self.zoom_var, width=6)
        self.zoom_label.pack(side=tk.LEFT, padx=2)

        ttk.Button(zoom_frame, text="-", command=self._zoom_out, width=3).pack(side=tk.LEFT, padx=1)
        ttk.Button(zoom_frame, text="+", command=self._zoom_in, width=3).pack(side=tk.LEFT, padx=1)
        ttk.Button(zoom_frame, text="⟲", command=self._reset_zoom, width=3).pack(side=tk.LEFT, padx=1)

    def _apply_theme(self):
        """Apply current theme to the window"""
        theme = self.theme_colors['high_contrast' if self.high_contrast else 'normal']
        # Note: ttk themes are more complex to change dynamically
        # This is a placeholder for theme application
        pass

    def _setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Layout", command=self._new_layout, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Layout...", command=self._open_layout, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Layout", command=self._save_layout, accelerator="Ctrl+S")
        file_menu.add_command(label="Save Layout As...", command=self._save_layout_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Save Config...", command=self._save_config)
        file_menu.add_command(label="Load Config...", command=self._load_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self._undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self._redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Duplicate Widget", command=self._duplicate_widget, accelerator="Ctrl+D")
        edit_menu.add_command(label="Delete Widget", command=self._remove_widget, accelerator="Delete")
        edit_menu.add_separator()
        edit_menu.add_command(label="Bring to Front", command=self._bring_to_front, accelerator="Ctrl+Home")
        edit_menu.add_command(label="Send to Back", command=self._send_to_back, accelerator="Ctrl+End")

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self._zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self._zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", command=self._reset_zoom, accelerator="Ctrl+0")
        view_menu.add_separator()
        view_menu.add_checkbutton(label="High Contrast", command=self._toggle_high_contrast)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Left Panel", command=self._toggle_left_panel, accelerator="F9")
        view_menu.add_command(label="Toggle Right Panel", command=self._toggle_right_panel, accelerator="F10")

        # Layout menu
        layout_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Layout", menu=layout_menu)
        layout_menu.add_command(label="Reset Layout", command=self._reset_layout)
        layout_menu.add_command(label="Preview", command=self._preview_layout, accelerator="F5")

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self._show_shortcuts, accelerator="F1")
        help_menu.add_command(label="About", command=self._show_about)

    def _setup_toolbar(self):
        """Setup main toolbar"""
        self.toolbar = MainToolbar(self.root, on_action=self._on_toolbar_action)
        self.toolbar.frame.pack(side=tk.TOP, fill=tk.X)

    def _setup_main_area(self):
        """Setup main area with paned window"""
        # Create main paned window
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left pane (collapsible)
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)

        # Left pane content
        self.widget_palette = WidgetPalette(self.left_frame, on_widget_add=self._on_widget_palette_action)
        self.widget_palette.frame.pack(fill=tk.BOTH, expand=True)

        # Center pane (workspace)
        self.center_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.center_frame, weight=3)

        self._setup_workspace()

        # Right pane (collapsible with tabs)
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=2)

        self._setup_right_panel()

        # Initialize file operations
        self.file_ops = FileOperations(self.root, self.config)
        self.file_ops.set_layout_manager(self.layout_manager)

    def _setup_workspace(self):
        """Setup the combined workspace with preview and active widgets"""
        # Create a vertical paned window for the workspace
        self.workspace_paned = ttk.PanedWindow(self.center_frame, orient=tk.VERTICAL)
        self.workspace_paned.pack(fill=tk.BOTH, expand=True)

        # Top pane: Screen Preview
        self.preview_frame = ttk.Frame(self.workspace_paned)
        self.workspace_paned.add(self.preview_frame, weight=3)
        self._setup_canvas()

        # Bottom pane: Active Widgets
        self.active_widgets_frame = ttk.Frame(self.workspace_paned)
        self.workspace_paned.add(self.active_widgets_frame, weight=1)
        self._setup_active_widgets_list()

    def _setup_canvas(self):
        """Setup dynamic canvas"""
        # Canvas container
        canvas_container = ttk.Frame(self.preview_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)

        # Canvas title
        canvas_label = ttk.Label(canvas_container, text=f"Screen Preview ({self.config.screen_size}x{self.config.screen_size})")
        canvas_label.pack(anchor=tk.W)

        # Canvas with scrollbars
        canvas_frame = ttk.Frame(canvas_container)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="black",
            highlightthickness=1,
            highlightbackground="gray"
        )

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid layout for canvas and scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        # Bind canvas events
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)  # Right click
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # Bind mouse wheel for zoom
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Button-4>", self._on_mouse_wheel)  # Linux
        self.canvas.bind("<Button-5>", self._on_mouse_wheel)  # Linux

    def _setup_active_widgets_list(self):
        """Setup the active widgets list in the workspace"""
        # Title
        active_label = ttk.Label(self.active_widgets_frame, text="Active Widgets", font=('Arial', 9, 'bold'))
        active_label.pack(anchor=tk.W, pady=(5, 5))

        # List frame
        list_frame = ttk.Frame(self.active_widgets_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5)

        self.widget_listbox = tk.Listbox(
            list_frame,
            height=6,
            selectmode=tk.SINGLE,
            exportselection=False
        )
        self.widget_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.widget_listbox.yview)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.widget_listbox.config(yscrollcommand=list_scrollbar.set)

        # Bind listbox selection event
        self.widget_listbox.bind('<<ListboxSelect>>', self._on_widget_list_select)

        # Widget control buttons
        controls_frame = ttk.Frame(self.active_widgets_frame)
        controls_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            controls_frame,
            text="Remove",
            command=self._remove_widget_from_list,
            width=10
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            controls_frame,
            text="Move Up",
            command=self._move_widget_up_in_list,
            width=10
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            controls_frame,
            text="Move Down",
            command=self._move_widget_down_in_list,
            width=10
        ).pack(side=tk.LEFT, padx=2)

    def _setup_right_panel(self):
        """Setup right panel with tabs"""
        # Create notebook for tabs
        self.right_notebook = ttk.Notebook(self.right_frame)
        self.right_notebook.pack(fill=tk.BOTH, expand=True)

        # Properties tab
        self.property_panel = CompactPropertyPanel(self.right_notebook, on_property_changed=self._on_property_changed)
        self.right_notebook.add(self.property_panel.frame, text="Properties")

        # Device tab
        self.device_panel = CompactDevicePanel(self.right_notebook, on_device_connected=self._on_device_connected)
        self.right_notebook.add(self.device_panel.frame, text="Device")

        # Set initial config
        self.device_panel.set_config(self.config)

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-n>', lambda e: self._new_layout())
        self.root.bind('<Control-o>', lambda e: self._open_layout())
        self.root.bind('<Control-s>', lambda e: self._save_layout())
        self.root.bind('<Control-Shift-S>', lambda e: self._save_layout_as())
        self.root.bind('<Control-z>', lambda e: self._undo())
        self.root.bind('<Control-y>', lambda e: self._redo())
        self.root.bind('<Control-d>', lambda e: self._duplicate_widget())
        self.root.bind('<Delete>', lambda e: self._remove_widget())
        self.root.bind('<Control-Home>', lambda e: self._bring_to_front())
        self.root.bind('<Control-End>', lambda e: self._send_to_back())
        self.root.bind('<Control-plus>', lambda e: self._zoom_in())
        self.root.bind('<Control-minus>', lambda e: self._zoom_out())
        self.root.bind('<Control-0>', lambda e: self._reset_zoom())
        self.root.bind('<F1>', lambda e: self._show_shortcuts())
        self.root.bind('<F5>', lambda e: self._preview_layout())
        self.root.bind('<F9>', lambda e: self._toggle_left_panel())
        self.root.bind('<F10>', lambda e: self._toggle_right_panel())

        # Arrow keys for widget movement
        self.root.bind('<Left>', lambda e: self._move_widget(-1, 0))
        self.root.bind('<Right>', lambda e: self._move_widget(1, 0))
        self.root.bind('<Up>', lambda e: self._move_widget(0, -1))
        self.root.bind('<Down>', lambda e: self._move_widget(0, 1))

    def update_status(self, message: str):
        """Update status bar message"""
        self.status_var.set(message)

    def _on_toolbar_action(self, action: str):
        """Handle toolbar action"""
        action_handlers = {
            "new_layout": self._new_layout,
            "open_layout": self._open_layout,
            "save_layout": self._save_layout,
            "undo": self._undo,
            "redo": self._redo,
            "duplicate_widget": self._duplicate_widget,
            "toggle_connection": self._toggle_connection,
            "apply_to_device": self._apply_to_device,
            "zoom_in": self._zoom_in,
            "zoom_out": self._zoom_out,
            "reset_zoom": self._reset_zoom,
            "bring_to_front": self._bring_to_front,
            "send_to_back": self._send_to_back
        }

        if action in action_handlers:
            action_handlers[action]()

    def _on_widget_palette_action(self, action):
        """Handle widget palette action"""
        if isinstance(action, tuple) and action[0] == 'action':
            # Handle widget list actions
            action_name = action[1]
            if action_name == "remove_widget":
                self._remove_widget()
            elif action_name == "move_widget_up":
                self._move_widget_up()
            elif action_name == "move_widget_down":
                self._move_widget_down()
        else:
            # Handle widget addition
            self._add_widget(action)

    def _on_canvas_resize(self, event):
        """Handle canvas resize for dynamic sizing"""
        self._update_canvas()

    def _on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        # Determine scroll direction
        if event.num == 4 or event.delta > 0:
            self._zoom_in()
        elif event.num == 5 or event.delta < 0:
            self._zoom_out()

    def _on_canvas_right_click(self, event):
        """Handle right click on canvas for context menu"""
        # Get canvas coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        # Convert to device coordinates
        device_x, device_y = self._canvas_to_device_coords(canvas_x, canvas_y)

        # Check if clicking on a widget
        widget = self.layout_manager.get_widget_at(device_x, device_y)

        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)

        if widget:
            # Widget-specific menu
            context_menu.add_command(label="Delete", command=self._remove_widget)
            context_menu.add_command(label="Duplicate", command=self._duplicate_widget)
            context_menu.add_separator()
            context_menu.add_command(label="Bring to Front", command=self._bring_to_front)
            context_menu.add_command(label="Send to Back", command=self._send_to_back)
        else:
            # Canvas-specific menu
            context_menu.add_command(label="Add Clock", command=self._add_clock_widget)
            context_menu.add_command(label="Add Weather", command=self._add_weather_widget)

            # Add plugin widgets
            try:
                plugin_manager = get_plugin_manager()
                plugin_widgets = plugin_manager.list_plugins()
                if plugin_widgets:
                    context_menu.add_separator()
                    for plugin_meta in plugin_widgets:
                        context_menu.add_command(
                            label=f"Add {plugin_meta.name}",
                            command=lambda name=plugin_meta.name: self._add_plugin_widget(name)
                        )
            except:
                pass

        # Show menu
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def _canvas_to_device_coords(self, canvas_x: float, canvas_y: float) -> Tuple[int, int]:
        """Convert canvas coordinates to device coordinates"""
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return 0, 0

        # Calculate scale factor
        scale_x = canvas_width / self.config.screen_size
        scale_y = canvas_height / self.config.screen_size
        scale = min(scale_x, scale_y) * self.zoom_level

        # Calculate offset to center the device
        device_width = self.config.screen_size * scale
        device_height = self.config.screen_size * scale
        offset_x = (canvas_width - device_width) / 2
        offset_y = (canvas_height - device_height) / 2

        # Convert coordinates
        device_x = int((canvas_x - offset_x) / scale)
        device_y = int((canvas_y - offset_y) / scale)

        return device_x, device_y

    def _device_to_canvas_coords(self, device_x: int, device_y: int) -> Tuple[float, float]:
        """Convert device coordinates to canvas coordinates"""
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return 0, 0

        # Calculate scale factor
        scale_x = canvas_width / self.config.screen_size
        scale_y = canvas_height / self.config.screen_size
        scale = min(scale_x, scale_y) * self.zoom_level

        # Calculate offset to center the device
        device_width = self.config.screen_size * scale
        device_height = self.config.screen_size * scale
        offset_x = (canvas_width - device_width) / 2
        offset_y = (canvas_height - device_height) / 2

        # Convert coordinates
        canvas_x = device_x * scale + offset_x
        canvas_y = device_y * scale + offset_y

        return canvas_x, canvas_y

    def _update_canvas(self):
        """Update canvas to reflect current layout"""
        # Clear canvas
        self.canvas.delete("all")

        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 600

        # Calculate scale factor
        scale_x = canvas_width / self.config.screen_size
        scale_y = canvas_height / self.config.screen_size
        scale = min(scale_x, scale_y) * self.zoom_level

        # Calculate offset to center the device
        device_width = self.config.screen_size * scale
        device_height = self.config.screen_size * scale
        offset_x = (canvas_width - device_width) / 2
        offset_y = (canvas_height - device_height) / 2

        # Update scroll region
        self.canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))

        # Draw device border
        self.canvas.create_rectangle(
            offset_x, offset_y,
            offset_x + device_width, offset_y + device_height,
            outline="gray", width=2
        )

        # Draw background
        bg_color = self.layout_manager.background_color
        bg_hex = f"#{bg_color[0]:02x}{bg_color[1]:02x}{bg_color[2]:02x}"
        self.canvas.create_rectangle(
            offset_x, offset_y,
            offset_x + device_width, offset_y + device_height,
            fill=bg_hex, outline=""
        )

        # Draw widgets
        for widget in self.layout_manager.widgets:
            if not widget.visible:
                continue

            # Calculate widget position and size on canvas
            x1, y1 = self._device_to_canvas_coords(widget.x, widget.y)
            x2, y2 = self._device_to_canvas_coords(widget.x + widget.width, widget.y + widget.height)

            # Draw widget rectangle
            outline_color = "yellow" if widget == self.selected_widget else "white"
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="", outline=outline_color, width=2,
                tags=f"widget_{id(widget)}"
            )

            # Draw widget label
            widget_type = widget.__class__.__name__.replace("Widget", "")
            self.canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2,
                text=widget_type, fill="white",
                font=("Arial", int(10 * self.zoom_level)),
                tags=f"widget_{id(widget)}"
            )

    def _zoom_in(self):
        """Zoom in canvas"""
        if self.zoom_level < self.max_zoom:
            self.zoom_level = min(self.zoom_level * 1.2, self.max_zoom)
            self.zoom_var.set(f"{int(self.zoom_level * 100)}%")
            self._update_canvas()

    def _zoom_out(self):
        """Zoom out canvas"""
        if self.zoom_level > self.min_zoom:
            self.zoom_level = max(self.zoom_level / 1.2, self.min_zoom)
            self.zoom_var.set(f"{int(self.zoom_level * 100)}%")
            self._update_canvas()

    def _reset_zoom(self):
        """Reset canvas zoom"""
        self.zoom_level = 1.0
        self.zoom_var.set("100%")
        self._update_canvas()

    def _toggle_high_contrast(self):
        """Toggle high contrast theme"""
        self.high_contrast = not self.high_contrast
        self._apply_theme()
        self._update_canvas()

    def _toggle_left_panel(self):
        """Toggle left panel visibility"""
        # This is a simplified toggle - in a full implementation,
        # you would want to remember the previous width
        current_width = self.left_frame.winfo_width()
        if current_width > 50:
            self.main_paned.forget(self.left_frame)
        else:
            self.main_paned.insert(0, self.left_frame)

    def _toggle_right_panel(self):
        """Toggle right panel visibility"""
        # This is a simplified toggle - in a full implementation,
        # you would want to remember the previous width
        current_width = self.right_frame.winfo_width()
        if current_width > 50:
            self.main_paned.forget(self.right_frame)
        else:
            self.main_paned.add(self.right_frame)

    def _show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        shortcuts_text = """
Keyboard Shortcuts:

File:
  Ctrl+N     - New Layout
  Ctrl+O     - Open Layout
  Ctrl+S     - Save Layout
  Ctrl+Shift+S - Save Layout As

Edit:
  Ctrl+Z     - Undo
  Ctrl+Y     - Redo
  Ctrl+D     - Duplicate Widget
  Delete     - Delete Widget
  Ctrl+Home  - Bring to Front
  Ctrl+End   - Send to Back

View:
  Ctrl++     - Zoom In
  Ctrl+-     - Zoom Out
  Ctrl+0     - Reset Zoom
  F9         - Toggle Left Panel
  F10        - Toggle Right Panel

Navigation:
  Arrow Keys - Move Selected Widget
  Mouse Wheel - Zoom In/Out
  Right Click - Context Menu

Other:
  F5         - Preview Layout
  F1         - Show This Help
        """

        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text)

    def _show_about(self):
        """Show about dialog"""
        about_text = """
Pixoomat - Compact Layout Designer
Version 3.0

A compact and accessible GUI for designing
widget layouts for Divoom Pixoo devices.

Features:
• Compact, responsive layout
• Keyboard navigation support
• High contrast theme
• Dynamic canvas sizing
• Tabbed property panels
        """

        messagebox.showinfo("About Pixoomat", about_text)

    # Rest of the methods would be similar to the original GUI but adapted for the compact layout
    # For brevity, I'll include the essential ones and note that others follow the same pattern

    def _on_canvas_click(self, event):
        """Handle canvas click"""
        # Convert canvas coordinates to device coordinates
        device_x, device_y = self._canvas_to_device_coords(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

        # Check if coordinates are within device bounds
        if device_x < 0 or device_x >= self.config.screen_size or \
           device_y < 0 or device_y >= self.config.screen_size:
            return

        # Find widget at position
        widget = self.layout_manager.get_widget_at(device_x, device_y)

        if widget:
            # Select widget
            self.selected_widget = widget
            self.drag_data = {"x": device_x - widget.x, "y": device_y - widget.y, "widget": widget}

            # Update property panel
            self.property_panel.set_widget(widget)
        else:
            # Deselect
            self.selected_widget = None
            self.drag_data = {"x": 0, "y": 0, "widget": None}
            self.property_panel.set_widget(None)

        # Update canvas and widget list
        self._update_canvas()
        self._update_active_widgets_list()

    def _on_canvas_drag(self, event):
        """Handle canvas drag"""
        if not self.drag_data["widget"]:
            return

        # Convert canvas coordinates to device coordinates
        device_x, device_y = self._canvas_to_device_coords(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

        # Calculate new widget position
        widget = self.drag_data["widget"]
        new_x = device_x - self.drag_data["x"]
        new_y = device_y - self.drag_data["y"]

        # Ensure widget stays within bounds
        new_x = max(0, min(new_x, self.config.screen_size - widget.width))
        new_y = max(0, min(new_y, self.config.screen_size - widget.height))

        # Save state for undo on first drag
        if not hasattr(self, '_drag_started') or not self._drag_started:
            layout_state = copy.deepcopy(self.layout_manager.to_dict())
            self.undo_manager.save_state("Moved widget", layout_state)
            self._drag_started = True

        # Update widget position
        widget.set_position(new_x, new_y)

        # Update display
        self._update_canvas()
        self._update_active_widgets_list()

    def _on_canvas_release(self, event):
        """Handle canvas release"""
        self.drag_data = {"x": 0, "y": 0, "widget": None}
        self._drag_started = False

    def _move_widget(self, dx: int, dy: int):
        """Move selected widget by offset"""
        if not self.selected_widget:
            return

        # Save state for undo
        layout_state = copy.deepcopy(self.layout_manager.to_dict())
        self.undo_manager.save_state("Moved widget", layout_state)

        # Update position
        new_x = max(0, min(self.selected_widget.x + dx, self.config.screen_size - self.selected_widget.width))
        new_y = max(0, min(self.selected_widget.y + dy, self.config.screen_size - self.selected_widget.height))

        self.selected_widget.set_position(new_x, new_y)

        # Update display
        self._update_canvas()
        self._update_active_widgets_list()

    def _on_property_changed(self, widget):
        """Handle property change"""
        self._update_canvas()
        self._update_active_widgets_list()

        # Save state for undo
        if widget:
            layout_state = copy.deepcopy(self.layout_manager.to_dict())
            self.undo_manager.save_state(f"Modified {widget.__class__.__name__}", layout_state)

    def _on_device_connected(self, pixoo_or_action):
        """Handle device connection"""
        if isinstance(pixoo_or_action, tuple) and pixoo_or_action[0] == 'apply':
            # Apply layout request
            self._apply_to_device()
        else:
            # Connection state change
            self.pixoo = pixoo_or_action
            if pixoo_or_action:
                self.update_status("Connected to device")
                self.toolbar.set_connection_state(True)
                # Apply current layout to device
                self._apply_to_device()
            else:
                self.update_status("Disconnected from device")
                self.toolbar.set_connection_state(False)

    def _add_widget(self, widget):
        """Add a widget to the layout"""
        # Save state for undo
        layout_state = copy.deepcopy(self.layout_manager.to_dict())

        # Validate and adjust widget dimensions to fit within canvas boundaries
        if widget.width > self.config.screen_size:
            widget.width = self.config.screen_size
            widget.set_property('width', self.config.screen_size)

        if widget.height > self.config.screen_size:
            widget.height = self.config.screen_size
            widget.set_property('height', self.config.screen_size)

        # Random position that fits on screen
        max_x = max(0, self.config.screen_size - widget.width)
        max_y = max(0, self.config.screen_size - widget.height)

        import random
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        widget.set_position(x, y)

        # Add to layout
        self.layout_manager.add_widget(widget)

        # Save undo state
        self.undo_manager.save_state("Added widget", layout_state)

        # Update display
        self._update_canvas()
        self._update_active_widgets_list()

    def _add_clock_widget(self):
        """Add a clock widget"""
        plugin_manager = get_plugin_manager()
        widget = plugin_manager.create_widget("Clock")
        if widget:
            self._add_widget(widget)

    def _add_weather_widget(self):
        """Add a weather widget"""
        plugin_manager = get_plugin_manager()
        widget = plugin_manager.create_widget("Weather")
        if widget:
            # Connect weather service
            if hasattr(widget, 'get_weather_data'):
                widget.get_weather_data = self.weather_service.get_weather
            self._add_widget(widget)

    def _add_plugin_widget(self, plugin_name: str):
        """Add a plugin widget"""
        plugin_manager = get_plugin_manager()
        widget = plugin_manager.create_widget(plugin_name)
        if widget:
            self._add_widget(widget)
        else:
            messagebox.showerror("Error", f"Failed to create widget from plugin: {plugin_name}")

    def _remove_widget(self):
        """Remove selected widget"""
        if not self.selected_widget:
            return

        # Save state for undo
        layout_state = copy.deepcopy(self.layout_manager.to_dict())

        self.layout_manager.remove_widget(self.selected_widget)
        self.selected_widget = None
        self.property_panel.set_widget(None)

        # Save undo state
        self.undo_manager.save_state("Removed widget", layout_state)

        # Update display
        self._update_canvas()
        self._update_active_widgets_list()

    def _move_widget_up(self):
        """Move selected widget up in z-order"""
        selection = self._get_selected_widget_index()
        if selection is not None and selection > 0:
            # Swap widgets
            widgets = self.layout_manager.widgets
            widgets[selection], widgets[selection - 1] = widgets[selection - 1], widgets[selection]

            # Update z-index values
            for i, widget in enumerate(widgets):
                widget.z_index = i

            # Update display
            self._update_canvas()
            self._update_active_widgets_list()
            self._select_widget_in_list(selection - 1)

    def _move_widget_down(self):
        """Move selected widget down in z-order"""
        selection = self._get_selected_widget_index()
        if selection is not None and selection < len(self.layout_manager.widgets) - 1:
            # Swap widgets
            widgets = self.layout_manager.widgets
            widgets[selection], widgets[selection + 1] = widgets[selection + 1], widgets[selection]

            # Update z-index values
            for i, widget in enumerate(widgets):
                widget.z_index = i

            # Update display
            self._update_canvas()
            self._update_active_widgets_list()
            self._select_widget_in_list(selection + 1)

    def _bring_to_front(self):
        """Bring selected widget to front"""
        if self.selected_widget:
            # Set highest z-index
            max_z = max([w.z_index for w in self.layout_manager.widgets])
            self.selected_widget.z_index = max_z + 1

            # Re-sort widgets by z-index
            self.layout_manager.widgets.sort(key=lambda w: w.z_index)

            # Update z-index values
            for i, widget in enumerate(self.layout_manager.widgets):
                widget.z_index = i

            self._update_canvas()
            self._update_active_widgets_list()

    def _send_to_back(self):
        """Send selected widget to back"""
        if self.selected_widget:
            # Set lowest z-index
            min_z = min([w.z_index for w in self.layout_manager.widgets])
            self.selected_widget.z_index = min_z - 1

            # Re-sort widgets by z-index
            self.layout_manager.widgets.sort(key=lambda w: w.z_index)

            # Update z-index values
            for i, widget in enumerate(self.layout_manager.widgets):
                widget.z_index = i

            self._update_canvas()
            self._update_active_widgets_list()

    def _duplicate_widget(self):
        """Duplicate selected widget"""
        if not self.selected_widget:
            return

        # Save state for undo
        layout_state = copy.deepcopy(self.layout_manager.to_dict())

        widget_class = self.selected_widget.__class__

        # Create new widget of same type
        new_widget = widget_class()

        # Copy properties
        new_widget.properties = self.selected_widget.properties.copy()

        # Offset position
        new_x = min(self.selected_widget.x + 10,
                    self.config.screen_size - new_widget.width)
        new_y = min(self.selected_widget.y + 10,
                    self.config.screen_size - new_widget.height)
        new_widget.set_position(new_x, new_y)

        # Add to layout
        self.layout_manager.add_widget(new_widget)

        # Save undo state
        self.undo_manager.save_state("Duplicated widget", layout_state)

        # Update display
        self._update_canvas()
        self._update_active_widgets_list()

    def _reset_layout(self):
        """Reset layout to default"""
        response = messagebox.askyesno("Reset Layout",
                                     "Are you sure you want to reset layout?")
        if response:
            self.layout_manager.widgets.clear()
            self._setup_default_layout()

    def _setup_default_layout(self):
        """Setup default layout for backward compatibility"""
        plugin_manager = get_plugin_manager()

        # Create clock widget
        clock_widget = plugin_manager.create_widget("Clock")
        if clock_widget:
            clock_widget.update_interval = self.config.update_interval
            clock_widget.set_property('time_format', self.config.time_format)
            clock_widget.set_property('text_color', self.config.text_color)

            # Center clock widget
            clock_x = self.config.screen_size // 2 - clock_widget.width // 2
            clock_y = self.config.screen_size // 2 - clock_widget.height // 2
            clock_widget.set_position(clock_x, clock_y)

            # Add to layout
            self.layout_manager.add_widget(clock_widget)

        # Create weather widget if enabled
        if self.config.show_weather:
            weather_widget = plugin_manager.create_widget("Weather")
            if weather_widget:
                weather_widget.set_property('text_color', self.config.text_color)

                # Position weather widget at bottom right
                weather_x = self.config.screen_size - weather_widget.width - 2
                weather_y = self.config.screen_size - weather_widget.height - 2
                weather_widget.set_position(weather_x, weather_y)
                weather_widget.z_index = 1  # Place above clock if overlapping

                # Connect weather service to widget
                if hasattr(weather_widget, 'get_weather_data'):
                    weather_widget.get_weather_data = self.weather_service.get_weather

                # Add to layout
                self.layout_manager.add_widget(weather_widget)

        # Set background color
        self.layout_manager.background_color = self.config.background_color

        # Update display
        self._update_canvas()
        self._update_active_widgets_list()

    def _load_layout(self, layout_config_path: str):
        """Load layout from configuration file"""
        try:
            import json
            with open(layout_config_path, 'r') as f:
                layout_data = json.load(f)

            self.layout_manager = LayoutManager.from_dict(layout_data)

            # Connect weather service to weather widgets
            for widget in self.layout_manager.widgets:
                if widget.__class__.__name__ == 'WeatherWidget' or 'Weather' in widget.__class__.__name__:
                    if hasattr(widget, 'get_weather_data'):
                        widget.get_weather_data = self.weather_service.get_weather

            # Update display
            self._update_canvas()
            self._update_active_widgets_list()

            print(f"Loaded layout from {layout_config_path}")
        except Exception as e:
            print(f"ERROR: Failed to load layout config: {e}")
            print("Falling back to default widgets...")
            self._setup_default_layout()

    # File operations methods (simplified for brevity)
    def _new_layout(self):
        """Create new layout"""
        if self.file_ops:
            if self.file_ops.new_layout():
                self.layout_manager.widgets.clear()
                self._update_canvas()
                self._update_active_widgets_list()
                self.property_panel.set_widget(None)

    def _open_layout(self):
        """Open layout from file"""
        if self.file_ops:
            if self.file_ops.open_layout():
                self._update_canvas()
                self._update_active_widgets_list()
                self.property_panel.set_widget(None)

    def _save_layout(self):
        """Save layout to file"""
        if self.file_ops:
            self.file_ops.save_layout()

    def _save_layout_as(self):
        """Save layout to a new file"""
        if self.file_ops:
            self.file_ops.save_layout_as()

    def _save_config(self):
        """Save configuration to file"""
        if self.file_ops:
            self.file_ops.save_config()

    def _load_config(self):
        """Load configuration from file"""
        if self.file_ops:
            if self.file_ops.open_config():
                self.device_panel.set_config(self.config)

    def _toggle_connection(self):
        """Toggle device connection"""
        if self.device_panel:
            self.device_panel._toggle_connection()

    def _apply_to_device(self):
        """Apply layout to actual device"""
        if not self.pixoo:
            messagebox.showwarning("No Device", "Please connect to a device first")
            return

        self.update_status("Applying layout to device...")

        def apply_task():
            try:
                # Get render data
                render_data = self.layout_manager.get_render_data()

                # Clear screen with background color
                bg_color = render_data['background']['color']
                self.pixoo.fill(bg_color)

                # Draw each widget
                for widget_data in render_data['widgets']:
                    if widget_data['type'] == 'text':
                        self.pixoo.draw_text(
                            widget_data['text'],
                            xy=(widget_data['x'], widget_data['y']),
                            rgb=widget_data['color']
                        )
                    # Future: Handle other render types

                # Push to device
                self.pixoo.push()

                self.root.after(0, lambda: self.update_status("Layout applied successfully"))
                self.root.after(0, lambda: messagebox.showinfo("Success", "Layout applied to device!"))

            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.update_status(f"Error: {error_msg}"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to apply layout: {error_msg}"))

        import threading
        threading.Thread(target=apply_task, daemon=True).start()

    def _preview_layout(self):
        """Preview layout on screen"""
        self._update_canvas()

    def _undo(self):
        """Menu command for undo"""
        operation = self.undo_manager.undo()
        if operation and operation['state']:
            # Restore the layout state
            self.layout_manager = LayoutManager.from_dict(operation['state'])

            # Update display
            self._update_canvas()
            self._update_active_widgets_list()
            self.property_panel.set_widget(None)

    def _redo(self):
        """Menu command for redo"""
        operation = self.undo_manager.redo()
        if operation and operation['state']:
            # Restore the layout state
            self.layout_manager = LayoutManager.from_dict(operation['state'])

            # Update display
            self._update_canvas()
            self._update_active_widgets_list()
            self.property_panel.set_widget(None)

    def _update_active_widgets_list(self):
        """Update the active widgets list"""
        self.widget_listbox.delete(0, tk.END)

        for widget in self.layout_manager.widgets:
            widget_type = widget.__class__.__name__.replace("Widget", "")
            position = f"({widget.x}, {widget.y})"
            self.widget_listbox.insert(tk.END, f"{widget_type} {position}")

    def _get_selected_widget_index(self) -> Optional[int]:
        """Get selected widget index from the listbox"""
        selection = self.widget_listbox.curselection()
        if selection:
            return selection[0]
        return None

    def _on_widget_list_select(self, event):
        """Handle widget selection from the list"""
        index = self._get_selected_widget_index()
        if index is not None and 0 <= index < len(self.layout_manager.widgets):
            widget = self.layout_manager.widgets[index]
            self.selected_widget = widget
            self.property_panel.set_widget(widget)
            self._update_canvas()

    def _select_widget_in_list(self, index: int):
        """Select widget at index in the listbox"""
        self.widget_listbox.selection_clear(0, tk.END)
        if 0 <= index < self.widget_listbox.size():
            self.widget_listbox.selection_set(index)
            self.widget_listbox.see(index)

    def _remove_widget_from_list(self):
        """Remove widget selected in the list"""
        index = self._get_selected_widget_index()
        if index is not None and 0 <= index < len(self.layout_manager.widgets):
            self.selected_widget = self.layout_manager.widgets[index]
            self._remove_widget()

    def _move_widget_up_in_list(self):
        """Move selected widget up in z-order from the list"""
        self._move_widget_up()

    def _move_widget_down_in_list(self):
        """Move selected widget down in z-order from the list"""
        self._move_widget_down()

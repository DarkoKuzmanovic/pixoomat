"""
Widget palette with tree view layout for categorized widgets
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, List, Dict, Any
from widgets import get_plugin_manager


class WidgetPalette:
    """Widget palette with categorized tree view"""

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

        # Create tree widget for categorized display
        self.tree = ttk.Treeview(self.frame, columns=("type",), displaycolumns=())
        self.tree.heading("#0", text="Category")
        self.tree.column("#0", width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind double-click event for adding widgets
        self.tree.bind("<Double-1>", self._on_tree_double_click)

    def _load_widgets(self):
        """Load available widgets and create tree view"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.widgets_info = []

        # Plugin widgets (including clock and weather)
        try:
            plugin_manager = get_plugin_manager()
            plugin_widgets = plugin_manager.list_plugins()

            for plugin_meta in plugin_widgets:
                # Use plugin-specific icons for clock and weather
                icon = '⏰' if plugin_meta.name == 'Clock' else '🌤️' if plugin_meta.name == 'Weather' else '🔌'

                self.widgets_info.append({
                    'name': plugin_meta.name,
                    'class': plugin_manager.create_widget,
                    'icon': icon,
                    'tooltip': f'Add {plugin_meta.name}',
                    'category': plugin_meta.category
                })
        except Exception as e:
            pass

        # Create tree view with categories
        self._create_widget_tree()

    def _create_widget_tree(self):
        """Create tree view of widgets grouped by category"""
        # Group widgets by category
        categories = {}
        for widget_info in self.widgets_info:
            category = widget_info['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(widget_info)

        # Create tree items for each category and its widgets
        for category, widgets in categories.items():
            # Create category node
            category_item = self.tree.insert("", "end", text=category, open=True)

            # Add widgets as children of the category
            for widget_info in widgets:
                widget_item = self.tree.insert(
                    category_item,
                    "end",
                    text=f"{widget_info['icon']} {widget_info['name']}",
                    values=(widget_info['name'],),
                    tags=(widget_info['name'],)
                )
                # Store widget info in the tree item
                self.tree.set(widget_item, "type", widget_info['name'])

    def _on_tree_double_click(self, event):
        """Handle double-click on tree item to add widget"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            parent = self.tree.parent(item)
            if parent:  # Only process widget items (not categories)
                widget_name = self.tree.item(item, "text").split(" ", 1)[1]  # Remove icon
                for widget_info in self.widgets_info:
                    if widget_info['name'] == widget_name:
                        self._add_widget(widget_info)
                        break

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
"""
File operations for saving/loading widget layouts
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

from layout_manager import LayoutManager
from config import PixoomatConfig


class FileOperations:
    """Handles file operations for layouts and configurations"""
    
    def __init__(self, parent, config: PixoomatConfig):
        """
        Initialize file operations manager
        
        Args:
            parent: Parent tkinter widget
            config: PixoomatConfig instance
        """
        self.parent = parent
        self.config = config
        self.layout_manager = None
        
        # File filters
        self.layout_filter = [
            ("JSON files", "*.json"),
            ("All files", "*.*")
        ]
    
    def set_layout_manager(self, layout_manager: LayoutManager):
        """
        Set the layout manager to operate on
        
        Args:
            layout_manager: LayoutManager instance
        """
        self.layout_manager = layout_manager
    
    def new_layout(self) -> bool:
        """
        Create a new layout
        
        Returns:
            True if layout was cleared
        """
        response = messagebox.askyesno(
            "New Layout", 
            "Are you sure you want to create a new layout? Any unsaved changes will be lost."
        )
        if response and self.layout_manager:
            self.layout_manager.widgets.clear()
            self.config.layout_config = None
            return True
        return False
    
    def open_layout(self) -> bool:
        """
        Open a layout from file
        
        Returns:
            True if layout was loaded successfully
        """
        filename = filedialog.askopenfilename(
            title="Open Layout",
            filetypes=self.layout_filter,
            initialdir=os.path.dirname(self.config.layout_config) if self.config.layout_config else None
        )
        
        if not filename:
            return False
        
        try:
            with open(filename, 'r') as f:
                layout_data = json.load(f)
            
            if self.layout_manager:
                self.layout_manager = LayoutManager.from_dict(layout_data)
            
            self.config.layout_config = filename
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open layout: {e}")
            return False
    
    def save_layout(self) -> bool:
        """
        Save current layout to file
        
        Returns:
            True if layout was saved successfully
        """
        if not self.layout_manager:
            messagebox.showwarning("Warning", "No layout to save")
            return False
        
        filename = self.config.layout_config
        
        # If no filename is set, ask for one
        if not filename:
            filename = filedialog.asksaveasfilename(
                title="Save Layout",
                defaultextension=".json",
                filetypes=self.layout_filter
            )
            if not filename:
                return False
        
        return self._save_layout_to_file(filename)
    
    def save_layout_as(self) -> bool:
        """
        Save layout to a new file
        
        Returns:
            True if layout was saved successfully
        """
        if not self.layout_manager:
            messagebox.showwarning("Warning", "No layout to save")
            return False
        
        filename = filedialog.asksaveasfilename(
            title="Save Layout As",
            defaultextension=".json",
            filetypes=self.layout_filter,
            initialdir=os.path.dirname(self.config.layout_config) if self.config.layout_config else None
        )
        
        if not filename:
            return False
        
        if self._save_layout_to_file(filename):
            self.config.layout_config = filename
            return True
        
        return False
    
    def _save_layout_to_file(self, filename: str) -> bool:
        """
        Save layout to specific file
        
        Args:
            filename: Path to save the layout
            
        Returns:
            True if layout was saved successfully
        """
        try:
            # Validate layout before saving
            if self.layout_manager:
                errors = self.layout_manager.validate_layout()
                if errors:
                    error_text = "\\n".join(errors)
                    response = messagebox.askyesno(
                        "Layout Validation Errors",
                        f"The layout has validation errors:\\n{error_text}\\n\\nSave anyway?"
                    )
                    if not response:
                        return False
            
            # Serialize layout
            layout_data = self.layout_manager.to_dict() if self.layout_manager else {}
            
            # Save to file
            with open(filename, 'w') as f:
                json.dump(layout_data, f, indent=2)
            
            messagebox.showinfo("Success", f"Layout saved to {os.path.basename(filename)}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save layout: {e}")
            return False
    
    def save_config(self) -> bool:
        """
        Save Pixoomat configuration to file
        
        Returns:
            True if configuration was saved successfully
        """
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            filetypes=self.layout_filter
        )
        
        if not filename:
            return False
        
        try:
            self.config.to_file(filename)
            messagebox.showinfo("Success", f"Configuration saved to {os.path.basename(filename)}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            return False
    
    def open_config(self) -> bool:
        """
        Open Pixoomat configuration from file
        
        Returns:
            True if configuration was loaded successfully
        """
        filename = filedialog.askopenfilename(
            title="Open Configuration",
            filetypes=self.layout_filter
        )
        
        if not filename:
            return False
        
        try:
            loaded_config = PixoomatConfig.from_file(filename)
            if loaded_config:
                # Copy properties to current config
                self.config.__dict__.update(loaded_config.__dict__)
                messagebox.showinfo("Success", f"Configuration loaded from {os.path.basename(filename)}")
                return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            return False
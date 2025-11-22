"""
Compact device panel for Pixoo device connection and management
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import re

from config import PixoomatConfig
from device_discovery import PixooDiscovery, test_connection


class CompactDevicePanel:
    """Compact panel for managing Pixoo device connection"""

    def __init__(self, parent, on_device_connected=None):
        """
        Initialize compact device panel

        Args:
            parent: Parent tkinter widget
            on_device_connected: Callback function when device connects
        """
        self.parent = parent
        self.on_device_connected = on_device_connected
        self.config = None
        self.pixoo = None

        # Create main frame
        self.frame = ttk.Frame(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components"""
        # Title
        title_label = ttk.Label(self.frame, text="Device", font=('Arial', 10, 'bold'))
        title_label.pack(anchor=tk.W, pady=(0, 5))

        # Connection controls frame
        conn_frame = ttk.Frame(self.frame)
        conn_frame.pack(fill=tk.X, pady=(0, 10))

        # Device selector dropdown
        ttk.Label(conn_frame, text="Device:").pack(anchor=tk.W)

        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(
            conn_frame,
            textvariable=self.device_var,
            state="readonly",
            width=20
        )
        self.device_combo.pack(fill=tk.X, pady=(2, 5))
        self.device_combo.bind('<<ComboboxSelected>>', self._on_device_selected)

        # Manual IP entry
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(conn_frame, textvariable=self.ip_var)
        self.ip_entry.pack(fill=tk.X, pady=(0, 5))
        self.ip_entry.bind('<Return>', lambda e: self._connect_to_device())

        # Port and screen size in same row
        settings_frame = ttk.Frame(conn_frame)
        settings_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(settings_frame, text="Port:").pack(side=tk.LEFT)
        self.port_var = tk.IntVar(value=80)
        self.port_spinbox = ttk.Spinbox(
            settings_frame,
            from_=1,
            to=65535,
            textvariable=self.port_var,
            width=8
        )
        self.port_spinbox.pack(side=tk.LEFT, padx=(5, 10))

        ttk.Label(settings_frame, text="Size:").pack(side=tk.LEFT)
        self.screen_size_var = tk.IntVar(value=64)
        self.screen_size_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.screen_size_var,
            values=["16", "32", "64"],
            state="readonly",
            width=5
        )
        self.screen_size_combo.pack(side=tk.LEFT, padx=5)

        # Discovery button
        self.discover_button = ttk.Button(
            conn_frame,
            text="🔍 Discover",
            command=self._discover_devices,
            width=20
        )
        self.discover_button.pack(fill=tk.X, pady=(0, 5))

        # Connection status with indicator
        status_frame = ttk.Frame(self.frame)
        status_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)

        self.status_canvas = tk.Canvas(status_frame, width=12, height=12, highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=(5, 5))
        self._update_status_indicator("disconnected")

        self.status_var = tk.StringVar(value="Disconnected")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT)

        # Connect/Disconnect button
        self.connect_button = ttk.Button(
            self.frame,
            text="🔌 Connect",
            command=self._toggle_connection,
            width=20
        )
        self.connect_button.pack(fill=tk.X, pady=(0, 5))

        # Apply button
        self.apply_button = ttk.Button(
            self.frame,
            text="✓ Apply Layout",
            command=self._apply_to_device,
            state=tk.DISABLED,
            width=20
        )
        self.apply_button.pack(fill=tk.X)

    def _update_status_indicator(self, status: str):
        """Update connection status indicator"""
        self.status_canvas.delete("all")

        if status == "connected":
            color = "#00aa00"  # Green
        elif status == "connecting":
            color = "#ffaa00"  # Orange
        else:
            color = "#aa0000"  # Red

        self.status_canvas.create_oval(2, 2, 10, 10, fill=color, outline="")

    def set_config(self, config: PixoomatConfig):
        """
        Set the configuration to use

        Args:
            config: PixoomatConfig instance
        """
        self.config = config

        # Update UI with config values
        self.ip_var.set(config.ip_address or "")
        self.port_var.set(config.port)
        self.screen_size_var.set(config.screen_size)

    def _on_device_selected(self, event):
        """Handle device selection from dropdown"""
        selection = self.device_var.get()
        if selection and selection != "Manual IP Entry":
            # Extract IP from selection text "Device Name (192.168.1.100)"
            match = re.search(r'\(([\d\.]+)\)', selection)
            if match:
                ip = match.group(1)
                self.ip_var.set(ip)

    def _discover_devices(self):
        """Discover Pixoo devices on the network"""
        self.status_var.set("Discovering...")
        self._update_status_indicator("connecting")
        self.device_combo['values'] = []
        self.device_var.set("")

        def discover_in_background():
            try:
                discovery = PixooDiscovery(timeout=5)
                devices = discovery.discover()

                # Update UI in main thread
                self.parent.after(0, lambda: self._update_device_list(devices))
            except Exception as e:
                self.parent.after(0, lambda: self._on_discovery_failed(str(e)))

        import threading
        thread = threading.Thread(target=discover_in_background)
        thread.daemon = True
        thread.start()

    def _update_device_list(self, devices):
        """Update the device list with discovered devices"""
        if not devices:
            self.status_var.set("No devices found")
            self._update_status_indicator("disconnected")
            return

        device_names = []
        for device in devices:
            device_name = device.get('name', 'Unknown')
            device_ip = device.get('ip', 'N/A')
            display_text = f"{device_name} ({device_ip})"
            device_names.append(display_text)

        # Add manual entry option
        device_names.append("Manual IP Entry")

        self.device_combo['values'] = device_names
        self.device_combo.set(device_names[0])

        self.status_var.set(f"Found {len(devices)} device(s)")
        self._update_status_indicator("disconnected")

    def _on_discovery_failed(self, error: str):
        """Handle discovery failure"""
        self.status_var.set(f"Discovery failed: {error}")
        self._update_status_indicator("disconnected")

    def _toggle_connection(self):
        """Toggle connection to device"""
        if not self.pixoo:
            # Connect to device
            self._connect_to_device()
        else:
            # Disconnect from device
            self._disconnect_from_device()

    def _connect_to_device(self):
        """Connect to selected device"""
        # Get device IP from selection or entry
        self._on_device_selected(None)  # Update IP from dropdown if needed

        ip = self.ip_var.get().strip()
        port = self.port_var.get()
        screen_size = self.screen_size_var.get()

        if not ip:
            messagebox.showerror("Error", "Please enter or select a device IP address")
            return

        self.status_var.set("Connecting...")
        self._update_status_indicator("connecting")
        self.connect_button.config(state=tk.DISABLED)

        def connect_in_background():
            try:
                from pixoo_client import CustomPixoo
                self.pixoo = CustomPixoo(
                    ip,
                    size=screen_size,
                    debug=self.config.debug if self.config else False,
                    refresh_connection_automatically=True,
                    port=port
                )

                # Test connection
                self.pixoo.fill((0, 0, 0))
                self.pixoo.push()

                # Update config with connection info
                if self.config:
                    self.config.ip_address = ip
                    self.config.port = port
                    self.config.screen_size = screen_size

                # Update UI in main thread
                self.parent.after(0, lambda: self._on_connected(ip))

            except Exception as e:
                self.parent.after(0, lambda: self._on_connection_failed(str(e)))

        import threading
        thread = threading.Thread(target=connect_in_background)
        thread.daemon = True
        thread.start()

    def _on_connected(self, ip: str):
        """Handle successful connection"""
        self.status_var.set(f"Connected to {ip}")
        self._update_status_indicator("connected")
        self.connect_button.config(text="🔌 Disconnect", state=tk.NORMAL)
        self.apply_button.config(state=tk.NORMAL)

        if self.on_device_connected:
            self.on_device_connected(self.pixoo)

    def _on_connection_failed(self, error: str):
        """Handle connection failure"""
        self.status_var.set(f"Connection failed: {error}")
        self._update_status_indicator("disconnected")
        self.connect_button.config(state=tk.NORMAL)
        self.pixoo = None

    def _disconnect_from_device(self):
        """Disconnect from current device"""
        if self.pixoo:
            # Clear the device screen
            try:
                self.pixoo.fill((0, 0, 0))
                self.pixoo.push()
            except:
                pass

        self.pixoo = None
        self.status_var.set("Disconnected")
        self._update_status_indicator("disconnected")
        self.connect_button.config(text="🔌 Connect", state=tk.NORMAL)
        self.apply_button.config(state=tk.DISABLED)

        if self.on_device_connected:
            self.on_device_connected(None)

    def _apply_to_device(self):
        """Apply current layout to device"""
        if not self.pixoo:
            messagebox.showwarning("No Device", "Please connect to a device first")
            return

        if self.on_device_connected:
            # Signal to parent to apply layout
            self.on_device_connected(('apply', self.pixoo))

    def get_pixoo(self):
        """Get the connected Pixoo instance"""
        return self.pixoo
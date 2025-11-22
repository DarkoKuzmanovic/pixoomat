"""
Device panel for Pixoo device connection and management
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import re

from config import PixoomatConfig
from device_discovery import PixooDiscovery, test_connection
from weather_service import WeatherService


class DevicePanel:
    """Panel for managing Pixoo device connection"""

    def __init__(self, parent, on_device_connected=None):
        """
        Initialize device panel

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
        title_label = ttk.Label(self.frame, text="Device Connection", font=('Arial', 10, 'bold'))
        title_label.pack(anchor=tk.W, pady=(0, 10))

        # IP Address section
        ip_frame = ttk.LabelFrame(self.frame, text="Device Address")
        ip_frame.pack(fill=tk.X, pady=(0, 10))

        # IP input
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(ip_frame, textvariable=self.ip_var)
        self.ip_entry.pack(fill=tk.X, padx=10, pady=5)

        # Port input
        port_frame = ttk.Frame(ip_frame)
        port_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(port_frame, text="Port:").pack(side=tk.LEFT)

        self.port_var = tk.IntVar(value=80)
        self.port_spinbox = ttk.Spinbox(
            port_frame,
            from_=1,
            to=65535,
            textvariable=self.port_var,
            width=10
        )
        self.port_spinbox.pack(side=tk.LEFT, padx=5)

        # Screen size
        screen_frame = ttk.Frame(ip_frame)
        screen_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(screen_frame, text="Screen Size:").pack(side=tk.LEFT)

        self.screen_size_var = tk.IntVar(value=64)
        self.screen_size_combo = ttk.Combobox(
            screen_frame,
            textvariable=self.screen_size_var,
            values=[16, 32, 64],
            state="readonly",
            width=8
        )
        self.screen_size_combo.pack(side=tk.LEFT, padx=5)

        # Discovery section
        discover_frame = ttk.LabelFrame(self.frame, text="Auto Discovery")
        discover_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            discover_frame,
            text="Discover Devices",
            command=self._discover_devices
        ).pack(fill=tk.X, padx=10, pady=5)

        # Device list
        list_frame = ttk.Frame(discover_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.device_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            height=6
        )
        self.device_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.device_listbox.yview)

        # Connection status
        status_frame = ttk.LabelFrame(self.frame, text="Connection Status")
        status_frame.pack(fill=tk.X, pady=(0, 10))

        self.status_var = tk.StringVar(value="Not connected")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(padx=10, pady=5)

        # Connection button
        self.connect_button = ttk.Button(
            status_frame,
            text="Connect",
            command=self._toggle_connection
        )
        self.connect_button.pack(padx=10, pady=5)

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

    def _discover_devices(self):
        """Discover Pixoo devices on the network"""
        self.status_var.set("Discovering devices...")
        self.device_listbox.delete(0, tk.END)

        def discover_in_background():
            try:
                discovery = PixooDiscovery(timeout=5)
                devices = discovery.discover()

                # Update UI in main thread
                self.parent.after(0, lambda: self._update_device_list(devices))
            except Exception as e:
                self.parent.after(0, lambda: self.status_var.set(f"Discovery failed: {e}"))

        import threading
        thread = threading.Thread(target=discover_in_background)
        thread.daemon = True
        thread.start()

    def _update_device_list(self, devices):
        """Update the device list with discovered devices"""
        self.device_listbox.delete(0, tk.END)

        if not devices:
            self.status_var.set("No devices found")
            return

        for device in devices:
            device_name = device.get('name', 'Unknown')
            device_ip = device.get('ip', 'N/A')
            display_text = f"{device_name} ({device_ip})"
            self.device_listbox.insert(tk.END, display_text)

        self.status_var.set(f"Found {len(devices)} device(s)")

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
        selected = self.device_listbox.curselection()
        if selected:
            selection_text = self.device_listbox.get(selected[0])
            # Extract IP from selection text "Device Name (192.168.1.100)"
            import re
            match = re.search(r'\(([\d\.]+)\)', selection_text)
            if match:
                ip = match.group(1)
                self.ip_var.set(ip)

        ip = self.ip_var.get().strip()
        port = self.port_var.get()
        screen_size = self.screen_size_var.get()

        if not ip:
            messagebox.showerror("Error", "Please enter or select a device IP address")
            return

        self.status_var.set("Connecting...")
        self.connect_button.config(state=tk.DISABLED)

        def connect_in_background():
            try:
                from pixoo_client import CustomPixoo
                self.pixoo = CustomPixoo(ip, size=screen_size, debug=self.config.debug if self.config else False, refresh_connection_automatically=True, port=port)

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
        self.connect_button.config(text="Disconnect", state=tk.NORMAL)

        if self.on_device_connected:
            self.on_device_connected(self.pixoo)

    def _on_connection_failed(self, error: str):
        """Handle connection failure"""
        self.status_var.set(f"Connection failed: {error}")
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
        self.connect_button.config(text="Connect", state=tk.NORMAL)

        if self.on_device_connected:
            self.on_device_connected(None)

    def get_pixoo(self):
        """Get the connected Pixoo instance"""
        return self.pixoo
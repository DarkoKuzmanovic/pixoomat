"""
Device discovery functionality for Pixoomat
"""
import socket
import time
from typing import List, Optional
from zeroconf import ServiceBrowser, Zeroconf


class PixooDiscovery:
    """Discovers Divoom Pixoo devices on the network"""

    # Pixoo devices typically use this service name
    SERVICE_TYPE = "_http._tcp.local."
    DEVICE_NAME_PREFIX = "Pixoo"

    def __init__(self, timeout: int = 10, port: int = 80):
        self.timeout = timeout
        self.port = port
        self.discovered_devices = []
        self.zeroconf = None
        self.browser = None

    def _get_local_network_prefix(self) -> str:
        """Get the local network prefix (e.g. 192.168.1)"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Doesn't need to be reachable
            s.connect(('8.8.8.8', 1))
            local_ip = s.getsockname()[0]
            s.close()
            return '.'.join(local_ip.split('.')[:-1])
        except Exception:
            return "192.168.1"

    def scan_network_range(self, network_prefix: Optional[str] = None) -> List[str]:
        """Scan network range for Pixoo devices (fallback method)"""
        if network_prefix is None:
            network_prefix = self._get_local_network_prefix()

        print(f"Scanning network {network_prefix}.0/24...")
        found_ips = []

        for i in range(1, 255):
            ip = f"{network_prefix}.{i}"
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)

            try:
                result = sock.connect_ex((ip, self.port))
                if result == 0:
                    # Try to identify if it's a Pixoo device
                    if self._is_pixoo_device(ip):
                        found_ips.append(ip)
                        print(f"Found potential Pixoo device at {ip}")
            except Exception:
                pass
            finally:
                sock.close()

        return found_ips

    def discover_mdns(self) -> List[dict]:
        """Discover devices using mDNS/Bonjour"""
        print("Discovering Pixoo devices using mDNS...")

        class PixooListener:
            def __init__(self):
                self.devices = []

            def add_service(self, zeroconf, service_type, name):
                if self.DEVICE_NAME_PREFIX in name:
                    try:
                        info = zeroconf.get_service_info(service_type, name)
                        if info and info.addresses:
                            ip = socket.inet_ntoa(info.addresses[0])
                            print(f"Found device: {name} at {ip}")
                            self.devices.append({'name': name, 'ip': ip})
                        else:
                            print(f"Found device: {name} (IP unknown)")
                            self.devices.append({'name': name})
                    except Exception as e:
                        print(f"Error resolving service info for {name}: {e}")

            def remove_service(self, zeroconf, service_type, name):
                pass

            def update_service(self, zeroconf, service_type, name):
                pass

        listener = PixooListener()

        try:
            self.zeroconf = Zeroconf()
            self.browser = ServiceBrowser(
                self.zeroconf,
                self.SERVICE_TYPE,
                listener
            )

            # Wait for devices to be discovered
            time.sleep(self.timeout)

            return listener.devices

        except Exception as e:
            print(f"mDNS discovery failed: {e}")
            return []
        finally:
            if self.browser:
                self.browser.cancel()
            if self.zeroconf:
                self.zeroconf.close()

    def discover(self, use_mdns: bool = True, network_prefix: Optional[str] = None) -> List[dict]:
        """Main discovery method combining mDNS and network scanning"""
        devices = []

        if use_mdns:
            devices = self.discover_mdns()

        # Fallback to network scan if mDNS fails or finds nothing
        if not devices:
            print("mDNS discovery found no devices, trying network scan...")
            ips = self.scan_network_range(network_prefix)
            devices = [{'name': f'Pixoo-{ip}', 'ip': ip} for ip in ips]

        self.discovered_devices = devices
        return devices

    def _is_pixoo_device(self, ip: str) -> bool:
        """Check if device at IP is a Pixoo device"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, self.port))

            # Simple HTTP GET to check response
            request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip)
            sock.send(request.encode())

            response = sock.recv(1024).decode()
            sock.close()

            # Check if response contains Pixoo identifiers
            return any(keyword in response.lower() for keyword in ['pixoo', 'divoom'])

        except Exception:
            return False

    def get_device_ip(self, device_name: str) -> Optional[str]:
        """Get IP address for discovered device"""
        for device in self.discovered_devices:
            if device.get('name') == device_name:
                return device.get('ip')
        return None

    def list_discovered_devices(self) -> None:
        """Print list of discovered devices"""
        if not self.discovered_devices:
            print("No Pixoo devices found.")
            return

        print("\nDiscovered Pixoo devices:")
        print("-" * 40)
        for i, device in enumerate(self.discovered_devices, 1):
            name = device.get('name', 'Unknown')
            ip = device.get('ip', 'N/A')
            print(f"{i}. {name} ({ip})")
        print("-" * 40)


def test_connection(ip: str) -> bool:
    """Test if we can connect to a Pixoo device at given IP"""
    try:
        from pixoo import Pixoo
        device = Pixoo(ip, debug=False)
        # Try to get device info as a connection test
        device.fill(0, 0, 0)  # Clear screen
        device.push()
        print(f"✅ Successfully connected to Pixoo at {ip}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to {ip}: {e}")
        return False
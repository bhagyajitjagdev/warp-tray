#!/usr/bin/env python3
"""warp-tray: System tray indicator for Cloudflare WARP"""

import gi
import subprocess
import os

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, AppIndicator3, GLib

ICON_ON = "network-vpn-symbolic"
ICON_OFF = "network-vpn-disabled-symbolic"
AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
AUTOSTART_FILE = os.path.join(AUTOSTART_DIR, "warp-tray.desktop")
AUTOSTART_ENTRY = """[Desktop Entry]
Type=Application
Name=WARP Tray
Comment=Cloudflare WARP tray indicator
Exec=/usr/bin/warp-tray
Icon=network-vpn-symbolic
Terminal=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
"""

POLL_INTERVAL = 5  # seconds


class WarpTray:
    def __init__(self):
        self._connected = False
        self._indicator = AppIndicator3.Indicator.new(
            "warp-tray",
            ICON_OFF,
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES,
        )
        self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self._indicator.set_title("WARP")
        self._update_status()
        self._rebuild_menu()
        self._ensure_autostart()

        # Poll WARP status
        GLib.timeout_add_seconds(POLL_INTERVAL, self._poll)

    def _is_connected(self):
        try:
            result = subprocess.run(
                ["warp-cli", "status"],
                capture_output=True, text=True, timeout=5,
            )
            return "connected" in result.stdout.lower() and "disconnected" not in result.stdout.lower()
        except Exception:
            return False

    def _update_status(self):
        self._connected = self._is_connected()
        if self._connected:
            self._indicator.set_icon(ICON_ON)
        else:
            self._indicator.set_icon(ICON_OFF)

    def _poll(self):
        old = self._connected
        self._update_status()
        if old != self._connected:
            self._rebuild_menu()
        return True  # keep polling

    def _rebuild_menu(self):
        menu = Gtk.Menu()

        # Status label
        status_item = Gtk.MenuItem(
            label=f"Status: {'Connected' if self._connected else 'Disconnected'}"
        )
        status_item.set_sensitive(False)
        menu.append(status_item)

        menu.append(Gtk.SeparatorMenuItem())

        # Connect / Disconnect
        if self._connected:
            item = Gtk.MenuItem(label="Disconnect")
            item.connect("activate", self._on_disconnect)
        else:
            item = Gtk.MenuItem(label="Connect")
            item.connect("activate", self._on_connect)
        menu.append(item)

        menu.append(Gtk.SeparatorMenuItem())

        # Autostart toggle
        item_autostart = Gtk.CheckMenuItem(label="Start on login")
        item_autostart.set_active(os.path.exists(AUTOSTART_FILE))
        item_autostart.connect("toggled", self._on_toggle_autostart)
        menu.append(item_autostart)

        menu.append(Gtk.SeparatorMenuItem())

        # Quit
        item_quit = Gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self._on_quit)
        menu.append(item_quit)

        menu.show_all()
        self._indicator.set_menu(menu)

    def _on_connect(self, _):
        subprocess.Popen(
            ["warp-cli", "connect"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        GLib.timeout_add(1500, self._after_toggle)

    def _on_disconnect(self, _):
        subprocess.Popen(
            ["warp-cli", "disconnect"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        GLib.timeout_add(1500, self._after_toggle)

    def _after_toggle(self):
        self._update_status()
        self._rebuild_menu()
        return False  # run once

    def _on_toggle_autostart(self, widget):
        if widget.get_active():
            os.makedirs(AUTOSTART_DIR, exist_ok=True)
            with open(AUTOSTART_FILE, "w") as f:
                f.write(AUTOSTART_ENTRY)
        else:
            try:
                os.unlink(AUTOSTART_FILE)
            except OSError:
                pass

    def _ensure_autostart(self):
        if not os.path.exists(AUTOSTART_FILE):
            os.makedirs(AUTOSTART_DIR, exist_ok=True)
            with open(AUTOSTART_FILE, "w") as f:
                f.write(AUTOSTART_ENTRY)

    def _on_quit(self, _):
        Gtk.main_quit()


def main():
    WarpTray()
    Gtk.main()


if __name__ == "__main__":
    main()

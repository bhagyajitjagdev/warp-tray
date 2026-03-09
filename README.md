# WARP Tray

A lightweight system tray indicator for [Cloudflare WARP](https://developers.cloudflare.com/warp-client/) on Linux (GNOME/Wayland).

## Features

- Shows VPN connection status in the system tray
- Connect/disconnect WARP from the tray menu
- Optional autostart on login
- No external Python dependencies — uses system GTK3 and AppIndicator3

## Prerequisites

- [Cloudflare WARP client](https://developers.cloudflare.com/warp-client/get-started/linux/) installed and registered
- GNOME desktop with AppIndicator support (e.g. [AppIndicator extension](https://extensions.gnome.org/extension/615/appindicator-support/))

## Install

Download the latest RPM from [Releases](https://github.com/bhagyajitjagdev/warp-tray/releases):

```bash
sudo dnf install ./warp-tray-*.noarch.rpm
```

## Usage

Launch from your application menu or run:

```bash
warp-tray
```

Right-click the tray icon for options:

- **Status** — current connection state
- **Connect / Disconnect** — toggle WARP
- **Start on login** — enable/disable autostart
- **Quit** — close the tray indicator

## Build RPM locally

```bash
sudo dnf install rpm-build rpmdevtools
rpmdev-setuptree
mkdir warp-tray-1.0.0 && cp warp-tray.py warp-tray.desktop LICENSE warp-tray-1.0.0/
tar czf ~/rpmbuild/SOURCES/warp-tray-1.0.0.tar.gz warp-tray-1.0.0
rpmbuild -bb warp-tray.spec
```

## License

[MIT](LICENSE)

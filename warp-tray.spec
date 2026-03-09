Name:           warp-tray
Version:        1.0.0
Release:        1%{?dist}
Summary:        System tray indicator for Cloudflare WARP

License:        MIT
URL:            https://github.com/bhagyajitjagdev/warp-tray
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       python3
Requires:       python3-gobject
Requires:       libappindicator-gtk3
Requires:       cloudflare-warp

%description
A lightweight system tray indicator for Cloudflare WARP on Linux.
Shows VPN connection status and lets you connect/disconnect from the tray.

%prep
%autosetup

%install
install -Dm755 warp-tray.py %{buildroot}%{_bindir}/warp-tray
install -Dm644 warp-tray.desktop %{buildroot}%{_datadir}/applications/warp-tray.desktop
install -Dm644 warp-tray-autostart.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/warp-tray.desktop

%files
%license LICENSE
%{_bindir}/warp-tray
%{_datadir}/applications/warp-tray.desktop
%{_sysconfdir}/xdg/autostart/warp-tray.desktop

%changelog
* Mon Mar 09 2026 Bhagyajit Jagdev - 1.0.0-1
- Initial release

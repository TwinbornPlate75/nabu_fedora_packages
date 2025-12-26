%global debug_package %{nil}
%global pkg_release 1

Name:           nabu-fedora-configs-niri
Version:        0.1.16
Release:        %{pkg_release}%{?dist}
Summary:        Configurations for Fedora for Nabu with niri Composer
License:        MIT
URL:            https://github.com/jhuang6451/nabu_fedora_packages
Source0:        %{url}/archive/refs/tags/%{name}-%{version}-%{pkg_release}.tar.gz
BuildArch:      noarch
BuildRequires:  systemd-rpm-macros

Requires:       pipewire-pulseaudio
Requires:       wireplumber

%description
This package contains configurations specific for Fedora for Nabu with niri composer

%prep
%autosetup -n nabu_fedora_packages-%{name}-%{version}-%{pkg_release}

%build
# Nothing to build

%install
cd nabu-fedora-configs-niri

cp -a etc %{buildroot}/
cp -a usr %{buildroot}/

%files
# General Configs
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/locale.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/environment.d/99-im.conf
%attr(644, root, root) %{_prefix}/lib/systemd/system/fcitx5-autostart.service
%attr(644, root, root) %{_presetdir}/91-fcitx5-autostart.preset
%attr(644, root, root) %{_presetdir}/92-greetd.preset

# Wallpapers Dir
%defattr(644, root, root, 755)
%{_sysconfdir}/skel/Pictures/Wallpapers

%post
# ----------------------------------------------------------------------
# appending to bashrc 
if [ -f /etc/skel/.bashrc ]; then
    echo "Appending custom configurations to /etc/skel/.bashrc"
    cat << 'EOF' >> /etc/skel/.bashrc

# ---- Added by nabu-fedora-configs-niri ----
alias code='code --ozone-platform=wayland'
fastfetch
# ---- End of nabu-fedora-configs-niri section ----
EOF
fi

# ----------------------------------------------------------------------
# greetd config
# ----------------------------------------------------------------------
CONFIG_FILE="/etc/greetd/config.toml"

if [ ! -d "/etc/greetd" ]; then
    echo "creating /etc/greetd ..."
    mkdir -p /etc/greetd
fi

cat > "$CONFIG_FILE" <<EOF
[terminal]
vt = 1

[default_session]
user = "greeter"
command = "dms-greeter --command niri"
EOF

if [ $? -eq 0 ]; then
    echo "greetd config updated."

# ----------------------------------------------------------------------
# pipewire user services
#
# This script handles the systemd user services for PipeWire.
# We use 'systemctl --global' to enable/disable services for all
# users on the system.
#
# The changes will take effect for each user upon their next login.
# ----------------------------------------------------------------------

# 1. Mask the legacy pulseaudio services to prevent conflicts.
#    This ensures that pipewire-pulse can take over without issues.
#    The '|| :' part ensures the command doesn't fail if the service
#    doesn't exist on the system.
echo "Masking conflicting PulseAudio user services for all users..."
systemctl --global mask pulseaudio.service pulseaudio.socket || :

# 2. Enable the core PipeWire services for all users.
echo "Enabling PipeWire user services for all users..."
systemctl --global enable pipewire.service pipewire-pulse.service wireplumber.service || :


%postun
# ----------------------------------------------------------------------
# Post-uninstall script
#
# This runs if the package is being uninstalled (not upgraded).
# The '$1' argument is 0 on final removal, and >= 1 on upgrade.
# ----------------------------------------------------------------------
if [ $1 -eq 0 ] ; then
    # This is a final uninstall, not an upgrade.
    echo "Disabling PipeWire user services for all users..."
    systemctl --global disable pipewire.service pipewire-pulse.service wireplumber.service || :

    echo "Unmasking PulseAudio user services for all users..."
    systemctl --global unmask pulseaudio.service pulseaudio.socket || :
fi

%changelog
* Fri Dec 26 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1.11-1
- Pre-installing DankMaterialShell. 

* Thu Oct 16 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1.10-1
- Add postinstall script for pipwire user services.

* Thu Oct 16 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1.6-1
- Remove deploy_user_configs.sh.

* Thu Oct 16 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1.4-1
- Fix fcitx5-autostart systemd preset name.

* Thu Oct 16 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1.3-1
- Postinstall script and some config updates.

* Sun Oct 12 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1.2-1
- Initial release.
%global debug_package %{nil}

# 直接从维护仓库 (release 分支) clone 源码, 与 fork 文件树保持同步
%global PKG_REPO https://github.com/TwinbornPlate75/nabu_fedora_packages.git
%global PKG_BRANCH release

Name:           nabu-fedora-configs-core
Version:        0.5.10
Release:        1%{?dist}
Summary:        Core configuration files for Fedora on Xiaomi Pad 5 (nabu)
License:        MIT
URL:            https://github.com/TwinbornPlate75/nabu_fedora
BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
BuildRequires:  tar
Requires:       dracut
Requires:       systemd-ukify
Requires:       rmtfs
Requires:       tqftpserv
Requires:       alsa-ucm
Requires:       qbootctl
Requires:       plymouth
Requires:       plymouth-plugin-script
Requires:       plymouth-plugin-two-step
Requires:       iwd

%description
This package contains the essential configuration files for running Fedora on the Xiaomi Pad 5 (nabu)

%prep
rm -rf nabu-packages-src
git clone --depth 1 --branch %{PKG_BRANCH} %{PKG_REPO} nabu-packages-src

%build
# Nothing to build

%install
cd nabu-packages-src/%{name}
cp -a etc %{buildroot}/
cp -a usr %{buildroot}/
chmod +x %{buildroot}%{_bindir}/nabu-regenerate-uki.sh

# install plymouth theme.
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/fedora-mac-style
tar -xf fedora-mac-style.tar.xz -C %{buildroot}%{_datadir}/plymouth/themes/fedora-mac-style --strip-components=1

%files
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/dracut.conf.d/99-nabu-generic.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/fstab
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/systemd/ukify.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/systemd/zram-generator.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/NetworkManager/conf.d/10-iwd.conf
%attr(644, root, root) %{_prefix}/lib/systemd/system/ath10k-shutdown.service
%attr(644, root, root) %{_presetdir}/80-nabu-core.preset
%attr(644, root, root) %{_presetdir}/81-qbootctl.preset
%attr(644, root, root) %{_presetdir}/82-disable-wpa_supplicant.preset
%attr(644, root, root) %{_datadir}/alsa/ucm2/conf.d/sm8150/sm8150.conf
%attr(644, root, root) %{_datadir}/alsa/ucm2/Xiaomi/nabu/HiFi.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/pulse/daemon.conf.d/89-xiaomi_nabu.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/pulse/default.pa.d/nabu.pa
%{_datadir}/plymouth/themes/fedora-mac-style/
%attr(755, root, root) %{_bindir}/nabu-regenerate-uki.sh

%post
# Create the EFI directory as a mount point for the ESP.
# This is required for UKI generation and bootloader installation.
mkdir -p /boot/efi || :

# Set plymouth theme. 
plymouth-set-default-theme fedora-mac-style || :

# Trigger UKI regeneration for installed kernels."
/usr/bin/nabu-regenerate-uki.sh || :
echo "--- UKI regeneration process finished. ---"

%systemd_post ath10k-shutdown.service

%preun
%systemd_preun ath10k-shutdown.service

%postun
%systemd_postun_with_restart ath10k-shutdown.service

%changelog
* Wed Oct 22 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.5.10-1
- Change WLAN backend to iwd.

* Fri Oct 10 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.5.5-1
- Force check dtb when regenerate UKI.

* Fri Oct 10 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.5.4-1
- Add execute permission for "nabu-regenerate-uki.sh".

* Fri Oct 10 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.5.3-1
- Standardize status statement against systemd services.

* Fri Oct 10 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.5.2-1
- Add UKI regeneration logic.

* Fri Oct 10 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.5.1-1
- Fix plymouth theme installation.

* Sat Oct 4 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.4-2
- Added plymouth theme and updated kernel cmdline.

* Sat Oct 4 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.3-2
- Moved some configs from extra to core.

* Sat Oct 4 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.2-2
- Removed "os-release".

* Tue Sep 30 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.2-1
- Added services, move os-release to a seperate package.

* Tue Sep 30 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1-1
- Initial release

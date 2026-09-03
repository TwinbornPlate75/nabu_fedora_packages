%global debug_package %{nil}

# 直接从维护仓库 (release 分支) clone 源码, 与 fork 文件树保持同步
%global PKG_REPO https://github.com/TwinbornPlate75/nabu_fedora_packages.git
%global PKG_BRANCH release

Name:           nabu-fedora-configs-gnome
Version:        0.4.7
Release:        1%{?dist}
Summary:        Configurations for Fedora for Nabu with Gnome DE
License:        MIT
URL:            https://github.com/TwinbornPlate75/nabu_fedora
BuildArch:      noarch
BuildRequires:  systemd-rpm-macros

%description
This package contains configurations specific for Fedora for Nabu builds with Gnome DE

%prep
rm -rf nabu-packages-src
git clone --depth 1 --branch %{PKG_BRANCH} %{PKG_REPO} nabu-packages-src

%build
# Nothing to build

%install
cd nabu-packages-src/%{name}
cp -a var %{buildroot}/
cp -a etc %{buildroot}/
cp -a usr %{buildroot}/

%files
%attr(644, gdm, gdm) %config(noreplace) %{_sharedstatedir}/gdm/.config/monitors.xml.default
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/locale.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/environment.d/99-im.conf
%attr(644, root, root) %{_prefix}/lib/systemd/system/fcitx5-autostart.service
%attr(644, root, root) %{_presetdir}/91-fcitx5-autostart.preset

%post
if [ ! -f %{_sharedstatedir}/gdm/.config/monitors.xml ]; then
    install -D -p -m 644 -o gdm -g gdm %{_sharedstatedir}/gdm/.config/monitors.xml.default %{_sharedstatedir}/gdm/.config/monitors.xml
fi

%systemd_post fcitx5-autostart.service

%preun
%systemd_preun fcitx5-autostart.service

%postun
%systemd_postun_with_restart fcitx5-autostart.service

%changelog
* Thu Oct 16 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.4.7-1
- Fix fcitx5-autostart systemd preset name.

* Fri Oct 10 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.4.5-1
- Better way to install gdm monitor settings.

* Fri Oct 10 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.4.3-1
- Add fcitx5 autostart service.

* Sat Oct 04 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.3-1
- Fix error.

* Sat Oct 04 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.2-1
- Added fcitx5 envs and locale.conf.

* Wed Oct 01 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1-1
- Initial release.
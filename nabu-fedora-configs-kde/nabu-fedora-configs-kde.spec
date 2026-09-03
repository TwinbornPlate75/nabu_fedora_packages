%global debug_package %{nil}

# 直接从维护仓库 (release 分支) clone 源码, 与 fork 文件树保持同步
%global PKG_REPO https://github.com/TwinbornPlate75/nabu_fedora_packages.git
%global PKG_BRANCH release

Name:           nabu-fedora-configs-kde
Version:        0.2
Release:        1%{?dist}
Summary:        Configurations for Fedora for Nabu with KDE Plasma DE
License:        MIT
URL:            https://github.com/TwinbornPlate75/nabu_fedora
BuildArch:      noarch

%description
This package contains configurations specific for Fedora for Nabu builds with kde DE

%prep
rm -rf nabu-packages-src
git clone --depth 1 --branch %{PKG_BRANCH} %{PKG_REPO} nabu-packages-src

%build
# Nothing to build

%install
cd nabu-packages-src/%{name}
cp -a etc %{buildroot}/

%files
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/locale.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/environment.d/99-im.conf

%changelog
* Sat Oct 04 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.2-1
- Fix error.

* Sat Oct 04 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1-1
- Initial release.
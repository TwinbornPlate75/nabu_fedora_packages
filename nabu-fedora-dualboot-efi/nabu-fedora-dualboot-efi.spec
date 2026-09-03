%global debug_package %{nil}

# 直接从维护仓库 (release 分支) clone 源码, 与 fork 文件树保持同步
%global PKG_REPO https://github.com/TwinbornPlate75/nabu_fedora_packages.git
%global PKG_BRANCH release

Name:           nabu-fedora-dualboot-efi
Version:        0.1
Release:        1%{?dist}
BuildArch:      aarch64
Summary:        rEFInd boot manager files for dual-booting on Xiaomi Pad 5 (nabu)
License:        GPLv3+ and others
URL:            https://github.com/TwinbornPlate75/nabu_fedora

%description
This package installs the rEFInd boot manager and theme files to the EFI
System Partition for dual-booting Fedora and Android on the Xiaomi Pad 5 (nabu).
It doesn't contain the UKI file needed to boot fedora, however,
for that's built during the kernel installing process.

%prep
rm -rf nabu-packages-src
git clone --depth 1 --branch %{PKG_BRANCH} %{PKG_REPO} nabu-packages-src

%build
# Nothing to build, we are just packaging files.

%install
# The source tree contains the 'boot' directory under the package dir.
# We copy it into the buildroot.
cd nabu-packages-src/%{name}
cp -a boot %{buildroot}/

%files
%defattr(644, root, root, 755)
# Own the directories we are shipping to the ESP
/boot/efi/EFI/Android
/boot/efi/EFI/BOOT

%changelog
* Tue Sep 30 2025 jhuang6451 <xplayerhtz123@outlook.com> - 0.1-1
- Initial package creation

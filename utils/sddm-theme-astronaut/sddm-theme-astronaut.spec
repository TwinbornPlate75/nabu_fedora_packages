%define theme_name sddm-astronaut-theme

Name:           %{theme_name}
Version:        1.0
Release:        1%{?dist}
Summary:        A beautiful SDDM theme

License:        GPL-3.0
URL:            https://github.com/Keyitdev/sddm-astronaut-theme
Source0:        astronaut-theme.conf

BuildRequires:  git-core
BuildArch:      noarch
Requires:       sddm qt6-qtsvg qt6-qtvirtualkeyboard qt6-qtmultimedia

%description
%{summary}

%prep
git clone -b master --depth 1 %{url} %{theme_name}

%build
# This package does not require a build step as it only consists of assets.

%install
# 1. Create the destination directory for the theme inside the buildroot.
install -d %{buildroot}%{_datadir}/sddm/themes/%{theme_name}
# 2. Copy the contents of the cloned git repository into the theme directory.
cp -a %{theme_name}/* %{buildroot}%{_datadir}/sddm/themes/%{theme_name}/
# 3. Font installation.
install -d %{buildroot}%{_datadir}/fonts/sddm-astronaut-theme-fonts
cp -a %{theme_name}/Fonts/* %{buildroot}%{_datadir}/fonts/sddm-astronaut-theme-fonts/
# 4. Install configuration files.
install -d %{buildroot}%{_sysconfdir}/sddm.conf.d
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/sddm.conf.d/astronaut-theme.conf

# Optional: change default theme
sed -i 's#^ConfigFile=.*#ConfigFile=Themes/pixel_sakura.conf#' %{buildroot}%{_datadir}/sddm/themes/%{theme_name}/metadata.desktop

%files
%defattr(644, root, root, 755)
%{_datadir}/sddm/themes/%{theme_name}
%{_datadir}/fonts/sddm-astronaut-theme-fonts
%license %{theme_name}/LICENSE
%{_sysconfdir}/sddm.conf.d/astronaut-theme.conf


%changelog
* Tue Oct 14 2025 jhuang6451 <xplayerhtz123@outlook.com> - 1.0-1
- Initial release
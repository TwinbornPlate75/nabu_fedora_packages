%undefine        _debugsource_packages
%global packagereleasever 3
%global kernelpatchver 1
%global kernelextraver -sm8150-%{kernelpatchver}
%global devicename nabu
Version:         6.17.0
Release:         sm8150.%{kernelpatchver}.%{packagereleasever}%{?dist}
ExclusiveArch:   aarch64
Name:            kernel-sm8150
Summary:         Mainline Linux kernel for sm8150 devices
License:         GPLv2
URL:             https://github.com/jhuang6451/Linux
Source0:         %{url}/archive/v%{version}%{kernelextraver}.tar.gz
Source1:         extra-sm8150.config
Patch0:          0001-dts-nabu-add-panel-rotation-property.patch

BuildRequires:   bc bison dwarves diffutils elfutils-devel findutils gcc gcc-c++ git-core hmaccalc hostname make openssl-devel perl-interpreter rsync tar which flex bzip2 xz zstd python3 python3-devel python3-pyyaml rust rust-src bindgen rustfmt clippy opencsd-devel net-tools dracut

Provides:        kernel               = %{version}-%{release}
Provides:        kernel-core          = %{version}-%{release}
Provides:        kernel-modules       = %{version}-%{release}
Provides:        kernel-modules-core  = %{version}-%{release}

%global uname_r %{version}-%{release}

%description
Mainline kernel for sm8150 (Qualcomm Snapdragon 855/860), packaged for standard Fedora systems with UEFI boot support

%prep
%autosetup -p1 -n Linux-%{version}%{kernelextraver}

# 准备默认配置
make defconfig sm8150.config

%build
# 移除既有的 CONFIG_LOCALVERSION，通过 make 命令的参数来控制它
sed -i '/^CONFIG_LOCALVERSION=/d' .config
# 追加额外的配置
cat %{SOURCE1} >> .config
# 确保没有 localversion 文件影响版本号
rm -f localversion*

make olddefconfig
# 使用 EXTRAVERSION 和空的 LOCALVERSION 来精确构建内核版本号
make EXTRAVERSION="%{kernelextraver}" LOCALVERSION= -j%{?_smp_build_ncpus} Image modules dtbs

%install

# 1. 安装内核模块
# INSTALL_MOD_PATH 指向 %{buildroot}/usr，这会将模块安装到 %{buildroot}/usr/lib/modules/%{uname_r}/
make EXTRAVERSION="%{kernelextraver}" LOCALVERSION= \
    INSTALL_MOD_PATH=%{buildroot}/usr \
    modules_install

# 2. 安装内核镜像、System.map 和配置文件到 /boot 目录
install -Dm644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
install -Dm644 System.map %{buildroot}/boot/System.map-%{uname_r}
install -Dm644 .config    %{buildroot}/boot/config-%{uname_r}

# 3. 安装设备树文件 (DTB)
# kernel-install 会自动在 /usr/lib/modules/%{uname_r}/dtb/ 路径下寻找 DTB 文件
install -d %{buildroot}/usr/lib/modules/%{uname_r}/dtb/qcom
install -Dm644 arch/arm64/boot/dts/qcom/sm8150-xiaomi-%{devicename}.dtb %{buildroot}/usr/lib/modules/%{uname_r}/dtb/qcom/sm8150-xiaomi-%{devicename}.dtb


%files
/boot/vmlinuz-%{uname_r}
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/usr/lib/modules/%{uname_r}


%posttrans
# ==============================================================================
# This script runs after the package's files are installed.
# It drives the UKI generation process. Static config is read from files,
# while version-specific paths are passed as arguments for robustness.
# ==============================================================================
set -e
uname_r=%{uname_r}

# --- 为新内核生成模块依赖 ---
depmod -a "${uname_r}"

echo "--- Generating UKI for ${uname_r} using dracut + ukify ---"

# --- 定义路径 ---
UKI_DIR="/boot/efi/EFI/fedora"
INITRD_PATH="/boot/initramfs-${uname_r}.img"
KERNEL_PATH="/boot/vmlinuz-${uname_r}"
DTB_PATH="/usr/lib/modules/${uname_r}/dtb/qcom/sm8150-xiaomi-%{devicename}.dtb"

UKI_OUTPUT_PATH="${UKI_DIR}/fedora-${uname_r}.efi"
mkdir -p "$UKI_DIR"

# --- 步骤 1: 使用 dracut 生成 initramfs ---
echo "Generating initramfs with dracut..."
# dracut 会从 /etc/dracut.conf.d/ 读取配置
dracut --kver "${uname_r}" --force
if [ ! -f "${INITRD_PATH}" ]; then
    echo "CRITICAL: dracut failed to generate initramfs at ${INITRD_PATH}" >&2
    exit 1
fi
echo "Initramfs generated at ${INITRD_PATH}"

# --- 步骤 2: 使用 systemd-ukify 生成 UKI ---
echo "Generating UKI with systemd-ukify..."
# ukify 会从 /etc/systemd/ukify.conf 读取静态配置 (Cmdline, Stub)
# 我们为确保健壮性，直接提供版本相关的路径。
ukify build \
    --linux="${KERNEL_PATH}" \
    --initrd="${INITRD_PATH}" \
    --devicetree="${DTB_PATH}" \
    --output="${UKI_OUTPUT_PATH}"

if [ ! -f "${UKI_OUTPUT_PATH}" ]; then
    echo "CRITICAL: ukify failed to generate UKI at ${UKI_OUTPUT_PATH}" >&2
    # 清理失败的中间产物
    rm -f "${INITRD_PATH}"
    exit 1
fi
echo "SUCCESS: UKI generated at ${UKI_OUTPUT_PATH}"

# --- 步骤 3: 清理独立的 initramfs ---
echo "Cleaning up standalone initramfs..."
rm -f "${INITRD_PATH}"

echo "--- UKI generation complete for ${uname_r} ---"

%postun

%changelog
* Wed Dec 2 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.17.0-2.nabu
- Switch source to https://github.com/jhuang6451/Linux.

* Thu Oct 16 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.17.0-1.nabu
- Initial release of 6.17.

* Mon Oct 13 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.16.0-6.sm8150
- Add screen rotation property patch to dts.

* Fri Oct 10 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.16.0-5.sm8150
- Change UKI name.
- Change UKI output directory to "/boot/efi/EFI/fedora".

* Thu Sep 25 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.16.0-4.sm8150
- Switched UKI generation to a dracut + systemd-ukify two-step process.
- dracut is now only responsible for creating the initramfs.
- systemd-ukify is used to assemble the kernel, initramfs, cmdline, and DTB into the final UKI.

* Thu Sep 25 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.16.0-3.sm8150
- Replaced `kernel-install` with a direct `dracut` call in %posttrans scriptlet.
- This fixes a critical bug where the device tree (DTB) was not being
  included in the generated UKI, ensuring the kernel is bootable.

* Sat Sep 20 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.16.0-2.sm8150
- Aligned post-install script with kernel-install framework for consistent UKI generation.
- Removed redundant dracut call from %posttrans.

* Sat Sep 13 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.16-1.sm8150
- Modified spec for standard Fedora systems, removing ostree logic.
- Adopted standard file paths (/boot) and kernel-install for UEFI/bootloader integration.

* Fri Sep 12 2025 jhuang6451 <xplayerhtz123@outlook.com> - 6.16.0-0.sm8150
- Added post-transaction script to copy kernel and DTB to ESP for UEFI boot.

* Fri Jul 25 2025 gmanka 6.16.0
- update to 6.16.0
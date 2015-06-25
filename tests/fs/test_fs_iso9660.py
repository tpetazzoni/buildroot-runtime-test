import basetest
import subprocess
import os

class TestIso9660Base(basetest.BRTest):
    basic_config = """
BR2_x86_pentium4=y
BR2_TOOLCHAIN_EXTERNAL=y
BR2_TOOLCHAIN_EXTERNAL_CUSTOM=y
BR2_TOOLCHAIN_EXTERNAL_DOWNLOAD=y
BR2_TOOLCHAIN_EXTERNAL_URL="http://autobuild.buildroot.org/toolchains/tarballs/br-i386-pentium4-full-2015.05.tar.bz2"
BR2_TOOLCHAIN_EXTERNAL_HEADERS_3_2=y
BR2_TOOLCHAIN_EXTERNAL_LOCALE=y
# BR2_TOOLCHAIN_EXTERNAL_HAS_THREADS_DEBUG is not set
BR2_TOOLCHAIN_EXTERNAL_INET_RPC=y
BR2_TOOLCHAIN_EXTERNAL_CXX=y
BR2_TARGET_GENERIC_GETTY_PORT="ttyS0"
BR2_TARGET_GENERIC_GETTY_BAUDRATE_115200=y
BR2_LINUX_KERNEL=y
BR2_LINUX_KERNEL_CUSTOM_VERSION=y
BR2_LINUX_KERNEL_CUSTOM_VERSION_VALUE="4.0"
BR2_LINUX_KERNEL_USE_CUSTOM_CONFIG=y
BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE="%s/conf/minimal-x86-qemu-kernel.config"
# BR2_TARGET_ROOTFS_TAR is not set
""" % os.getcwd()

    def run_external(self):
        self.s.boot(arch="i386",
                    options=["-cdrom", os.path.join(self.builddir, "images", "rootfs.iso9660")])
        self.s.login()
        (r, s) = self.s.run("mount | grep '/dev/root on / type iso9660'")
        self.assertEqual(s, 0)
        (r, s) = self.s.run("touch test")
        self.assertEqual(s, 1)

    def run_internal(self):
        self.s.boot(arch="i386",
                    options=["-cdrom", os.path.join(self.builddir, "images", "rootfs.iso9660")])
        self.s.login()
        (r, s) = self.s.run("mount | grep 'rootfs on / type rootfs'")
        self.assertEqual(s, 0)
        (r, s) = self.s.run("touch test")
        self.assertEqual(s, 0)

#
# Grub 2
#

class TestIso9660Grub2External(TestIso9660Base):
    config = TestIso9660Base.basic_config + """
BR2_TARGET_ROOTFS_ISO9660=y
# BR2_TARGET_ROOTFS_ISO9660_INITRD is not set
BR2_TARGET_GRUB2=y
BR2_TARGET_GRUB2_BOOT_PARTITION="cd"
BR2_TARGET_GRUB2_BUILTIN_MODULES="boot linux ext2 fat part_msdos part_gpt normal biosdisk iso9660"
BR2_TARGET_ROOTFS_ISO9660_BOOT_MENU="%s/conf/grub2.cfg"
""" % os.getcwd()
    def test_run(self):
        self.run_external()

class TestIso9660Grub2Internal(TestIso9660Base):
    config = TestIso9660Base.basic_config + """
BR2_TARGET_ROOTFS_ISO9660=y
BR2_TARGET_ROOTFS_ISO9660_INITRD=y
BR2_TARGET_GRUB2=y
BR2_TARGET_GRUB2_BOOT_PARTITION="cd"
BR2_TARGET_GRUB2_BUILTIN_MODULES="boot linux ext2 fat part_msdos part_gpt normal biosdisk iso9660"
BR2_TARGET_ROOTFS_ISO9660_BOOT_MENU="%s/conf/grub2.cfg"
""" % os.getcwd()
    def test_run(self):
        self.run_internal()

#
# Grub
#

class TestIso9660GrubExternal(TestIso9660Base):
    config = TestIso9660Base.basic_config + """
BR2_TARGET_ROOTFS_ISO9660=y
# BR2_TARGET_ROOTFS_ISO9660_INITRD is not set
BR2_TARGET_GRUB=y
BR2_TARGET_ROOTFS_ISO9660_BOOT_MENU="%s/conf/grub-menu.lst"
""" % os.getcwd()
    def test_run(self):
        self.run_external()

class TestIso9660GrubInternal(TestIso9660Base):
    config = TestIso9660Base.basic_config + """
BR2_TARGET_ROOTFS_ISO9660=y
BR2_TARGET_GRUB=y
BR2_TARGET_ROOTFS_ISO9660_BOOT_MENU="%s/grub-menu.lst"
""" % os.getcwd()
    def test_run(self):
        self.run_internal()

#
# Syslinux
#

class TestIso9660SyslinuxExternal(TestIso9660Base):
    config = TestIso9660Base.basic_config + """
BR2_TARGET_ROOTFS_ISO9660=y
# BR2_TARGET_ROOTFS_ISO9660_INITRD is not set
BR2_TARGET_ROOTFS_ISO9660_HYBRID=y
BR2_TARGET_ROOTFS_ISO9660_BOOT_MENU="%s/isolinux.cfg"
BR2_TARGET_SYSLINUX=y
""" % os.getcwd()
    def test_run(self):
        self.run_external()

class TestIso9660SyslinuxInternal(TestIso9660Base):
    config = TestIso9660Base.basic_config + """
BR2_TARGET_ROOTFS_ISO9660=y
BR2_TARGET_ROOTFS_ISO9660_INITRD=y
BR2_TARGET_ROOTFS_ISO9660_HYBRID=y
BR2_TARGET_ROOTFS_ISO9660_BOOT_MENU="%s/isolinux.cfg"
BR2_TARGET_SYSLINUX=y
""" % os.getcwd()
    def test_run(self):
        self.run_internal()

from basetest import BRTest
import subprocess
import os
import basetest

class TestDropbear(BRTest):
    config = basetest.basic_toolchain_config + """
BR2_TARGET_GENERIC_ROOT_PASSWD="root"
BR2_SYSTEM_DHCP="eth0"
BR2_PACKAGE_DROPBEAR=y
BR2_TARGET_ROOTFS_CPIO=y
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        img = os.path.join(self.builddir, "images", "rootfs.cpio")
        self.s.boot(arch="armv5", kernel="builtin",
                    options=["-initrd", img, "-net", "nic",
                             "-net", "user,hostfwd=tcp::2222-:22"])
        self.s.login("root")
        (r, s) = self.s.run("netstat -ltn 2>/dev/null | grep -q 0.0.0.0:22")
        self.assertEqual(s, 0)
        # Would be useful to try to login through SSH here, through
        # localhost:2222, though it is not easy to pass the ssh
        # password on the command line.

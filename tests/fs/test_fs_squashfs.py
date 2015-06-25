import basetest
import subprocess
import os

class TestSquashfs(basetest.BRTest):
    config = basetest.basic_toolchain_config + """
BR2_TARGET_ROOTFS_SQUASHFS=y
# BR2_TARGET_ROOTFS_SQUASHFS4_GZIP is not set
BR2_TARGET_ROOTFS_SQUASHFS4_LZ4=y
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        out = subprocess.check_output(["host/usr/bin/unsquashfs", "-s",
                                       "images/rootfs.squashfs"],
                                      cwd = self.builddir,
                                      env = {"LANG" : "C" })
        out = out.splitlines()
        self.assertEqual(out[0],
                         "Found a valid SQUASHFS 4:0 superblock on images/rootfs.squashfs.")
        self.assertEqual(out[3],
                         "Compression lz4")
        img = os.path.join(self.builddir, "images", "rootfs.squashfs")
        subprocess.call(["truncate", "-s", "%1M", img])
        self.s.boot(arch="armv7", kernel="builtin",
                    options=["-drive", "file=%s,if=sd" % img],
                    append=["root=/dev/mmcblk0", "rootfstype=squashfs"])
        self.s.login()
        (r, s) = self.s.run("mount | grep '/dev/root on / type squashfs'")
        self.assertEqual(s, 0)

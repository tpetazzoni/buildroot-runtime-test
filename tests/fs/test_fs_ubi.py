import basetest
import subprocess
import os

class TestUbi(basetest.BRTest):
    config = basetest.basic_toolchain_config + """
BR2_TARGET_ROOTFS_UBIFS=y
BR2_TARGET_ROOTFS_UBIFS_LEBSIZE=0x7ff80
BR2_TARGET_ROOTFS_UBIFS_MINIOSIZE=0x1
BR2_TARGET_ROOTFS_UBI=y
BR2_TARGET_ROOTFS_UBI_PEBSIZE=0x80000
BR2_TARGET_ROOTFS_UBI_SUBSIZE=1
"""

    # TODO: if you boot Qemu twice on the same UBI image, it fails to
    # attach the image the second time, with "ubi0 error:
    # ubi_read_volume_table: the layout volume was not found". To be
    # investigated.
    def test_run(self):
        img = os.path.join(self.builddir, "images", "rootfs.ubi")
        out = subprocess.check_output(["file", img],
                                      cwd = self.builddir,
                                      env = {"LANG" : "C" })
        out = out.splitlines()

        subprocess.call(["truncate", "-s 128M", img])

        self.s.boot(arch="armv7", kernel="builtin",
                    options=["-drive", "file=%s,if=pflash" % img],
                    append=["root=ubi0:rootfs", "ubi.mtd=0", "rootfstype=ubifs"])
        self.s.login()
        (r, s) = self.s.run("mount | grep 'ubi0:rootfs on / type ubifs'")
        self.assertEqual(s, 0)

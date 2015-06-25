import basetest
import subprocess
import os

def jffs2dump_find_file(flist, fname):
    for f in flist:
        f = f.strip()
        if f.startswith("Dirent") and f.endswith(fname):
            return True
    return False

class TestJffs2(basetest.BRTest):
    config = basetest.basic_toolchain_config + """
BR2_TARGET_ROOTFS_JFFS2=y
BR2_TARGET_ROOTFS_JFFS2_CUSTOM=y
BR2_TARGET_ROOTFS_JFFS2_CUSTOM_EBSIZE=0x80000
BR2_TARGET_ROOTFS_JFFS2_NOCLEANMARKER=y
BR2_TARGET_ROOTFS_JFFS2_PAD=y
BR2_TARGET_ROOTFS_JFFS2_PADSIZE=0x4000000
# BR2_TARGET_ROOTFS_TAR is not set
"""

    # TODO: there are some scary JFFS2 messages when one starts to
    # write files in the rootfs: "jffs2: Newly-erased block contained
    # word 0x0 at offset 0x046c0000". To be investigated.

    def test_run(self):
        img = os.path.join(self.builddir, "images", "rootfs.jffs2")
        out = subprocess.check_output(["host/usr/sbin/jffs2dump", "-c", img],
                                      cwd = self.builddir,
                                      env = {"LANG" : "C" })
        out = out.splitlines()
        self.assertTrue(jffs2dump_find_file(out, "busybox"))

        self.s.boot(arch="armv7", kernel="builtin",
                    options=["-drive", "file=%s,if=pflash" % img],
                    append=["root=/dev/mtdblock0", "rootfstype=jffs2"])
        self.s.login()
        (r, s) = self.s.run("mount | grep '/dev/root on / type jffs2'")
        self.assertEqual(s, 0)

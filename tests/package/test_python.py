from basetest import BRTest
import subprocess
import os
import basetest

class TestPythonBase(BRTest):
    config = basetest.basic_toolchain_config + """
BR2_PACKAGE_PYTHON=y
BR2_TARGET_ROOTFS_CPIO=y
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        self.s.boot(arch="armv5", kernel="builtin",
                    options=["-initrd", os.path.join(self.builddir, "images", "rootfs.cpio")])
        self.s.login()
        (r, s) = self.s.run("python --version 2>&1 | grep -q '^Python 2'")
        self.assertEqual(s, 0)
        (r, s) = self.s.run("python -c 'import math; math.floor(12.3)'")
        self.assertEqual(s, 0)
        (r, s) = self.s.run("python -c 'import ctypes; libc = ctypes.cdll.LoadLibrary(\"libc.so.0\"); print libc.time(None)'")
        self.assertEqual(s, 0)
        (r, s) = self.s.run("python -c 'import zlib'")
        self.assertEqual(s, 1)

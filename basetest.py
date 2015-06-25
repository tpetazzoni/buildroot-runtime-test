import unittest
import os
import subprocess
import configtest
import datetime

from builder import Builder
from system import System

basic_toolchain_config = """
BR2_arm=y
BR2_TOOLCHAIN_EXTERNAL=y
BR2_TOOLCHAIN_EXTERNAL_CUSTOM=y
BR2_TOOLCHAIN_EXTERNAL_DOWNLOAD=y
BR2_TOOLCHAIN_EXTERNAL_URL="http://autobuild.buildroot.org/toolchains/tarballs/br-arm-full-2015.05.tar.bz2"
BR2_TOOLCHAIN_EXTERNAL_HEADERS_4_0=y
BR2_TOOLCHAIN_EXTERNAL_LOCALE=y
# BR2_TOOLCHAIN_EXTERNAL_HAS_THREADS_DEBUG is not set
BR2_TOOLCHAIN_EXTERNAL_INET_RPC=y
BR2_TOOLCHAIN_EXTERNAL_CXX=y
"""

minimal_config = """
BR2_INIT_NONE=y
BR2_SYSTEM_BIN_SH_NONE=y
# BR2_PACKAGE_BUSYBOX is not set
# BR2_TARGET_ROOTFS_TAR is not set
"""

class BRTest(unittest.TestCase):
    def showMsg(self, msg):
        print "[%s/%s/%s] %s" % (self.testname, self.testinstance,
                                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 msg)
    def setUp(self):
        if os.getenv("REUSE_BUILD"):
            self.builddir = os.getenv("REUSE_BUILD").rstrip("/")
            skip_build = True
        else:
            skip_build = False
            b = subprocess.check_output(["mktemp", "-d", "buildroot.XXXXX"],
                                        cwd=configtest.builddir)
            b = b.strip()
            self.builddir = os.path.join(configtest.builddir, b)
        self.testname = self.__class__.__name__
        self.testinstance = os.path.basename(self.builddir)
        self.buildlog = self.builddir + "-build.log"
        self.runlog = self.builddir + "-run.log"
        self.s = None
        self.showMsg("Starting")
        self.b = Builder(self.__class__.config, self.builddir, self.buildlog)
        if not skip_build:
            self.showMsg("Building")
            self.b.build()
            self.showMsg("Building done")
        self.s = System(self.runlog)

    def tearDown(self):
        self.showMsg("Cleaning up")
        if self.s:
            self.s.stop()
        if self.b and os.getenv("KEEP_BUILD"):
            self.b.delete()

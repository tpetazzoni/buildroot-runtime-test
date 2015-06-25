import os
import shutil
import subprocess
import configtest

class Builder:
    def __init__(self, config, builddir, buildlog):
        self.config = config
        self.builddir = builddir
        self.buildlog = buildlog
        self.fbuildlog = open(buildlog, "w+")

    def build(self):
        f = open(os.path.join(self.builddir, ".config"), "w+")
        f.write(self.config)
        f.close()
        cmd = ["make", "-C", configtest.srcdir, "O=%s" % self.builddir, "olddefconfig"]
        ret = subprocess.call(cmd, stdout=self.fbuildlog, stderr=self.fbuildlog)
        if ret != 0:
            raise SystemError("Cannot olddefconfig")
        cmd = ["make", "-C", self.builddir]
        ret = subprocess.call(cmd, stdout=self.fbuildlog, stderr=self.fbuildlog)
        if ret != 0:
            raise SystemError("Build failed")

    def delete(self):
        shutil.rmtree(self.builddir)

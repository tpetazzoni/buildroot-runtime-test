import telnetlib
import subprocess
import socket

class System:
    # runlog: path to the log file
    def __init__(self, runlog):
        self.qemu = None
        self.__tn = None
        self.log = ""
        self.flog = open(runlog, "w+")

    # Start Qemu to boot the system
    #
    # arch: Qemu architecture to use
    #
    # kernel: path to the kernel image, or the special string
    # 'builtin' in which case a pre-built kernel image will be used
    # (so far only armv5 and armv7 kernels are available). If None,
    # then no kernel is used, and we assume a bootable device will be
    # specified.
    #
    # options: array of command line options to pass to Qemu
    #
    # append: array of kernel arguments to pass to Qemu -append option
    #
    def boot(self, arch, kernel=None, options=None, append=None):
        qemu_cmd = []
        qemu_args = []
        qemu_arch = arch
        kappend = []

        if kernel:
            machine = None
            if kernel == "builtin":
                if arch == "armv7":
                    kernel = "kernels/kernel-vexpress"
                    machine = "vexpress-a9"
                    kappend.append("console=ttyAMA0")
                    qemu_args += [ "-dtb", "kernels/vexpress-v2p-ca9.dtb"]
                    qemu_arch = "arm"
                elif arch == "armv5":
                    kernel = "kernels/kernel-versatile"
                    machine = "versatilepb"
                    kappend.append("console=ttyAMA0")
                    qemu_arch = "arm"

            qemu_args += ["-kernel", kernel]
            if machine:
                qemu_args += ["-M", machine]

        if append:
            kappend += append

        if kappend:
            qemu_args += ["-append", " ".join(kappend)]

        if options:
            qemu_args += options

        qemu_cmd += ["qemu-system-%s" % qemu_arch,
                    "-serial", "telnet::1234,server",
                    "-display", "none"] + qemu_args

        self.flog.write("> starting qemu with '%s'\n" % " ".join(qemu_cmd))

        self.qemu = subprocess.Popen(qemu_cmd, stdout=self.flog, stderr=self.flog)

        # Wait for the telnet port to appear and connect to it.
        while True:
            try:
                self.__tn = telnetlib.Telnet("localhost", 1234)
                if self.__tn:
                    break
            except socket.error:
                continue

    def __read_until(self, waitstr, timeout=5):
        r = self.__tn.read_until(waitstr, timeout)
        self.log += r
        self.flog.write(r)
        return r

    def __write(self, wstr):
        self.__tn.write(wstr)

    # Wait for the login prompt to appear, and then login as root with
    # the provided password, or no password if not specified.
    def login(self, password=None):
        self.flog.write("> waiting for login\n")
        self.__read_until("buildroot login:", 10)
        if not "buildroot login:" in self.log:
            print "==> System does not boot"
            raise SystemError("System does not boot")
        self.flog.write("> log in\n")
        self.__write("root\n")
        if password:
            self.__read_until("Password:")
            self.__write(password + "\n")
        self.__read_until("# ")

    # Run the given 'cmd' on the target, and return a tuple (r, s),
    # where r is the standard output of the command, and s is the
    # return code.
    def run(self, cmd):
        self.flog.write("> running '%s'\n" % cmd)
        self.__write(cmd + "\n")
        r = self.__read_until("# ")
        r = r.strip().split("\n")
        r = r[1:len(r)-1]
        self.__write("echo $?\n")
        s = self.__read_until("# ")
        s = int(s.strip().split("\n")[1])
        self.flog.write("> command terminated, status %d\n" % s)
        return (r, s)

    def stop(self):
        if self.qemu:
            self.qemu.terminate()
            self.qemu.kill()

    def showlog(self):
        print "=== Full log ==="
        print self.log
        print "================"

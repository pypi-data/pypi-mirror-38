from __future__ import print_function

import os
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile

try:
    from urllib.request import urlretrieve
except:
    from urllib import urlretrieve

def chmod_x(filename):
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

def prepare_dest(dest):
    destdir = os.path.dirname(dest)
    if not os.path.exists(destdir):
        os.makedirs(destdir)

def install_bin_from_tar(tar, member, dest):
    fd = tar.extractfile(member)
    print("installing %s" % dest)
    prepare_dest(dest)
    with open(dest, "wb") as o:
        o.write(fd.read())
    fd.close()
    chmod_x(dest)

def install_from_tarurl(url, match_member, args):
    localfile = urlretrieve(url)[0]
    with tarfile.open(localfile, "r:gz") as t:
        for m in t:
            if match_member(m):
                dest = os.path.join(args.prefix, "bin", os.path.basename(m.name))
                install_bin_from_tar(t, m, dest)
    os.unlink(localfile)

class Tool(object):
    @classmethod
    def is_installed(self, *args):
        if hasattr(self, "exe"):
            if sys.version_info[0] < 3:
                paths = os.environ["PATH"].split(os.pathsep)
                for p in paths:
                    if os.path.exists(os.path.join(p, self.exe)):
                        return True
                return False
            return shutil.which(self.exe) is not None
    @classmethod
    def name(self):
        return self.__name__.lower()


class NuSMV(Tool):
    exe = "NuSMV"
    url_pat = "http://nusmv.fbk.eu/distrib/NuSMV-2.6.0-%s.tar.gz"
    binfile = {
        "linux64": url_pat % "linux64",
        "linux32": url_pat % "linux32",
        "darwin": url_pat % "macosx64",
        "windows": url_pat % "win32",
    }

    @classmethod
    def install(self, system, args):
        binfile = self.binfile[system]
        def match_entry(m):
            return m.name.endswith("bin/NuSMV") \
                or  m.name.endswith("bin/NuSMV.exe")
        install_from_tarurl(binfile, match_entry, args)

class Dot(Tool):
    exe = "dot"
    binfile = {
        "windows": "https://graphviz.gitlab.io/_pages/Download/windows/graphviz-2.38.zip",
    }

    @classmethod
    def install(self, system, args):
        if system == "windows":
            dest = os.path.join(args.prefix, "bin")
            localfile = urlretrieve(self.binfile[system])[0]
            with zipfile.ZipFile(localfile) as t:
                t.extractall(dest)
            os.rename(os.path.join(dest, "release"), os.path.join(dest, "dot"))
        if system == "darwin":
            print("!! Il faut installer graphviz ; voir instructions sur\nhttp://macappstore.org/graphviz-2/")
        else:
            print("!! Il faut installer graphviz (http://graphviz.org)\nSur ubuntu: apt install graphviz")

tools = [NuSMV, Dot]

if __name__ == "__main__":
    system = platform.system().lower()
    if system == "linux":
        system = "%s%s" % (system, platform.architecture()[0][:2])
    assert system in ["linux64", "linux32", "darwin", "windows"], \
        "Plaform %s is not supported" % system

    prefix = os.path.expanduser("~")

    from argparse import ArgumentParser
    parser = ArgumentParser(prog=sys.argv[0])
    for t in tools:
        n = t.name()
        parser.add_argument("--no-%s" % n, dest=n, action="store_false",
                default=True)
    parser.add_argument("--prefix", default=prefix)
    args = parser.parse_args()

    for t in tools:
        if not getattr(args, t.name()):
            continue
        if t.is_installed(args):
            print("# %s is already installed" % t.__name__)
            continue
        print("%s Installing %s " % ("#"*5, t.__name__))
        t.install(system, args)


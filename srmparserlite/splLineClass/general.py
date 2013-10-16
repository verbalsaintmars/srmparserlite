if __name__ == "__main__" and __package__ is None:
   __package__ = "srmLogParserLite.splLineClass"

from ..splGeneral.deco import VersionDeco

import re


@VersionDeco(1)
class VersionParser(object):
   __slots__ = ["versionFmt"]

   def __init__(this):
      this.versionFmt = r".*?version=(?P<VERSION>\d\.\d\.\d)"

   def getVersionFmt(this):
      return this.versionFmt
   VERSIONFMT = property(getVersionFmt)


def tester():
   tmphead = r"Section for VMware vCenter Site Recovery Manager, pid=2344, version=5.0.1, build=build-633117, option=Release"
   ver = VersionParser()
   v_m = re.match(ver.VERSIONFMT, tmphead)
   if v_m is not None:
      print(v_m.string)
      print(v_m.group("VERSION"))
   else:
      print("test fail")

if __name__ == '__main__':  # Only when run
   tester()

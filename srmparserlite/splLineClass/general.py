__package__ = "srmparserlite.splLineClass"

from ..splGeneral.deco import VersionDeco


@VersionDeco(1)
class VersionFmt(object):
   __slots__ = ["versionFmt"]

   def __init__(this):
      this.versionFmt = r".*?version=(?P<VERSION>\d\.\d\.\d)"

   def getVersionFmt(this):
      return this.versionFmt
   VERSIONFMT = property(getVersionFmt)

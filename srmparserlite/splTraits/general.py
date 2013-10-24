__package__ = "srmparserlite.splTraits"

from ..splGeneral.deco import VersionDeco


@VersionDeco(1)
class GeneralFmt(object):
   __slots__ = [
         "versionFmt",
         "timeFmt"]

   def __init__(this):
      this.versionFmt = r".*?version=(?P<VERSION>\d\.\d\.\d)"

      this.timeFmt = \
         r"(?P<TIME>^\d{4}-\d{2}-\d{2}T|t\d{2}:\d{2}:\d{2}\.\d{3}[\+\-]" \
         r"\d{2}:\d{2})"

   def getVersionFmt(this):
      return this.versionFmt

   def getTimeFmt(this):
      return this.timeFmt

   VERSIONFMT = property(getVersionFmt)
   TIMEFMT = property(getTimeFmt)

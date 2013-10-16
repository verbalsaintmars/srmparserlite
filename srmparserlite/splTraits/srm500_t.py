"""
TODO 1. change lower case with instance variable
"""
__package__ = "srmparserlite.splTraits"

from ..splGeneral.deco import VersionDeco


@VersionDeco(500)  # Have class variable ClassVersion
class SrmTrait(object):
   __slots__ = [
         "headerFmt",
         "lineRegexFmt",
         "timeFmt",
         "infoFmt",
         "typeFmt",
         "dataFmt",
         "bundleFmt"]

   def __init__(this):
      this.headerFmt = r".*,\s*pid=(?P<PID>\d+),\s*version=(?P<VERSION>\d\.\d\.\d),\s*" \
                       "build=build-(?P<BUILD>\d+),\s*option=(?P<OPTION>\w+)"
      this.lineRegexFmt = r"(?P<TIME>.*?)\s(?P<INFO>(?:\[.*?\]\s))" \
                          "(?P<TYPE>\[.*?\]\s)?(?P<DATA>.*)"
      this.timeFmt = "%Y-%m-%dT%H:%M:%S.%f"
      # Will have other ID in it.
      this.infoFmt = r"\[(?P<TID>\d+)\s(?P<LOGINFO>\w+)\s\'(?P<CLASS>\w+)\'" \
                     "\s?(?:connID=(?P<CONNID>.*?))?\s?(?:opID=(?P<OPID>.*?))?\]"
      this.typeFmt = r"\[(?P<TYPE>\w+)\]"
      this.dataFmt = r""
      this.bundleFmt = r"^-->"

   def getHeaderFmt(this):
      return this.headerFmt

   def getLineRegexFmt(this):
      return this.lineRegexFmt

   def getTimeFmt(this):
      return this.timeFmt

   def getInfoFmt(this):
      return this.infoFmt

   def getTypeFmt(this):
      return this.typeFmt

   def getDataFmt(this):
      return this.dataFmt

   def getBundleFmt(this):
      return this.bundleFmt

   def GetTrailOffSet(this):
      if hasattr(this, 'trailOffSet'):
         return this.trailOffSet
      else:
         return 0

   HEADERFMT = property(getHeaderFmt)
   LINEFMT = property(getLineRegexFmt)
   TIMEFMT = property(getTimeFmt)
   INFOFMT = property(getHeaderFmt)
   TYPEFMT = property(getInfoFmt)
   DATAFMT = property(getDataFmt)
   BUNDLEFMT = property(getBundleFmt)
   TRAILOFFSET = property(GetTrailOffSet)


def tester():
   srml = SrmTrait()
   print(srml.__version__)

if __name__ == '__main__':  # Only when run
   tester()

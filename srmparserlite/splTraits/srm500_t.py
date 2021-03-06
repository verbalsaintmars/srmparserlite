"""
DONE 1. change lower case with instance variable
DONE 2. update ctx text
"""
__package__ = "srmparserlite.splTraits"

from ..splGeneral.deco import VersionDeco


@VersionDeco(500)  # To have class variable __version__
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

      this.headerFmt = \
         r".*,\s*pid=(?P<PID>\d+),\s*version=(?P<VERSION>\d\.\d\.\d),\s*" \
         r"build=build-(?P<BUILD>\d+),\s*option=(?P<OPTION>\w+)"

      this.lineRegexFmt = \
         r"(?P<TIME>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[\+\-]" \
         r"\d{2}:\d{2})" \
         r"\s" \
         r"(?:\[(?P<INFO>(?P<TID>\d+)\s(?P<LOGINFO>\w+)\s" \
         r"\'(?P<CLASS>.*?)\'\s?(?P<OTHERINFO>.*?))\])\s?" \
         r"(?:\[(?P<TYPE>.*?)\])?\s?" \
         r"(?P<DATA>.*)"

      this.timeFmt = {
         "Format": "%Y-%m-%dT%H:%M:%S.%f",
         "TimeZoneOffSet": -6}  # for capturing the utc timezone data

      this.infoFmt = r"\[" \
                     r"(?P<TID>\d+)\s" \
                     r"(?P<LOGINFO>\w+)\s" \
                     r"\'(?P<CLASS>\w+)\'\s?" \
                     r"(?:connID=(?P<CONNID>.*?))?\s?" \
                     r"(?:ctxID=(?P<CTXID>.*?))?\s?" \
                     r"(?:opID=(?P<OPID>.*?))?\]"
      this.typeFmt = r"\[(?P<TYPE>\w+)\]"
      this.dataFmt = r""
      this.bundleFmt = r"(?P<BUNDLE>(?:^-->.*)|(?:^\[#\d+\] -->.*))"

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
   INFOFMT = property(getInfoFmt)
   TYPEFMT = property(getTypeFmt)
   DATAFMT = property(getDataFmt)
   BUNDLEFMT = property(getBundleFmt)
   TRAILOFFSET = property(GetTrailOffSet)

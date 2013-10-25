__package__ = "srmparserlite.splTraits"
from ..splGeneral.deco import VersionDeco


@VersionDeco(1)
def DefaultYamlFile():
   return "splconfig.yml"


@VersionDeco(500)
def SrmLogFileNameFormater():
   return r"vmware-dr-(?P<NUM>\d+)\.log"


@VersionDeco(500)
def SrmLogGzFileNameFormater():
   return r"vmware-dr-(?P<NUM>\d+)\.log\.gz"


@VersionDeco(1)
def DefaultUnsupportFileName():
   return r"UnsupportFormat"


@VersionDeco(1)
def DefaultResultFileName():
   return r"splResult"


@VersionDeco(1)
def OneBigLogFileName():
   return r"OneBigLog.log"


@VersionDeco(1)
class ResultFileFormater(object):
   #splresult_{nu}.log
   __slots__ = [
      "numFormat",
      "defaultReplaceFormat",
      "defaultFileName",
      "unsupportedReplaceFormat",
      "unsupportedFilename"]

   def __init__(this, a_baseFileName):
      this.numFormat = a_baseFileName.strip() + r"_(?P<NUM>\d+)\.log"
      this.defaultReplaceFormat = r"(" + a_baseFileName.strip() + ")_\d+(\.log)"
      this.defaultFileName = a_baseFileName.strip() + "_0.log"
      this.unsupportedReplaceFormat = \
         r"(" + a_baseFileName.strip() + r")_" + \
         r"\d+_" + r"(" + DefaultUnsupportFileName() + r")(\.log)"
      this.unsupportedFilename = a_baseFileName.strip() + r"_" + \
                                 r"0_" + DefaultUnsupportFileName() + r".log"

   def getUNReplaceformat(this):
      return this.unsupportedReplaceFormat

   def getUNFileName(this):
      return this.unsupportedFilename

   def getNumFormat(this):
      return this.numFormat

   def getReplaceFormat(this):
      return this.defaultReplaceFormat

   def getFileName(this):
      return this.defaultFileName

   NUMFORMAT = property(getNumFormat)
   REPLACEFORMAT = property(getReplaceFormat)
   FILENAME = property(getFileName)
   UNREPLACEFORMAT = property(getUNReplaceformat)
   UNFILENAME = property(getUNFileName)

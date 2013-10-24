__package__ = "srmparserlite.splTraits"
from ..splGeneral.deco import VersionDeco


@VersionDeco(1)
def DefaultYamlFile():
   return "splconfig.yml"


@VersionDeco(500)
def SrmLogFileNameFormater():
   return r"vmware-dr-\d+\.log"


@VersionDeco(500)
def SrmLogGzFileNameFormater():
   return r"vmware-dr-\d+\.log\.gz"


@VersionDeco(1)
def DefaultUnsupportFileName():
   return r"_UnsupportFormat"


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
      "replaceFormat",
      "fileName"]

   def __init__(this, a_baseFileName):
      this.numFormat = a_baseFileName.strip() + r"_(?P<NUM>\d+)\.log"
      this.replaceFormat = r"(" + a_baseFileName.strip() + ")_\d+(\.log)"
      this.fileName = a_baseFileName.strip() + "_0.log"

   def getNumFormat(this):
      return this.numFormat

   def getReplaceFormat(this):
      return this.replaceFormat

   def getFileName(this):
      return this.fileName

   NUMFORMAT = property(getNumFormat)
   REPLACEFORMAT = property(getReplaceFormat)
   FILENAME = property(getFileName)

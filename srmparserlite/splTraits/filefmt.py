from ..splGeneral.deco import VersionDeco


@VersionDeco(500)
def SrmLogFileNameFormater():
   return r"vmware-dr-\d+\.log"


@VersionDeco(500)
def SrmLogGzFileNameFormater():
   return r"vmware-dr-\d+\.log\.gz"


def OneBigLogFileName():
   return r"OneBigLog.log"

if __name__ == "__main__" and __package__ is None:
   __package__ = "srmLogParserLite.splLineClass"

from ..splGeneral.deco import VersionDeco

"""
TODO 1. __str__ for each class
"""

#Section for VMware vCenter Site Recovery Manager, pid=2344, version=5.0.1, build=build-633117, option=Release
@VersionDeco(500)
class HeadLineClass(object):
   __slots__ = [
         "processedFlag",
         "hlcPid",
         "hlcVersion",
         "hlcBuild",
         "hlcOption"]

   def __init__(this):
      this.processedFlag = False

   def setPF(this, a_pf):
      this.processedFlag = a_pf

   def getPF(this):
      return this.processedFlag

   def setPid(this, a_pid):
      this.hlcPid = a_pid

   def getPid(this):
      return this.hlcPid

   def setVersion(this, a_version):
      this.hlcVersion = a_version

   def getVersion(this):
      return this.hlcVersion

   def setBuild(this, a_build):
      this.hlcBuild = a_build

   def getBuild(this):
      return this.hlcBuild

   def setOption(this, a_option):
      this.hlcOption = a_option

   def getOption(this):
      return this.hlcOption

   PROCESSEDFLAG = property(getPF, setPF)
   PID = property(getPid, setPid)
   VERSION = property(getVersion, setVersion)
   BUILD = property(getBuild, setBuild)
   OPTION = property(getOption, setOption)


#2013-07-23T20:30:09.705+02:00 [04116 verbose 'DatastoreGroupManager' opID=528a0d41] Processing virtual machine 'vm-6150'
@VersionDeco(500)
class LineClass(object):
   __slots__ = [
         "bundleFlag",
         "lcTime",
         "lcInfo",
         "lcType",
         "lcData",
         "lcBundle"]

   def __init__(this):
      this.bundleFlag = False

   def setBundleFlag(this, a_flg):
      this.bundleFlag = a_flg

   def getBundleFlag(this):
      return this.bundleFlag

   def setTime(this, a_time):
      this.lcTime = a_time

   def getTime(this):
      return this.lcTime

   def setInfo(this, a_info):
      this.lcInfo = a_info

   def getInfo(this):
      return this.lcInfo

   def setType(this, a_type):
      this.lcType = a_type

   def getType(this):
      return this.lcType

   def setData(this, a_data):
      this.lcData = a_data

   def getData(this):
      return this.lcData

   def setBundle(this, a_bundle):
      """
         Make Bundle into list for better search, instead of one long string with newline
      """
      if hasattr(this, "lcbundle"):
         this.lcBundle.append(a_bundle)
      else:
         this.setBundleFlag(True)
         this.lcBundle = [a_bundle]

   def getBundle(this):
      return this.lcBundle

   BUNDLEFLAG = property(getBundleFlag, setBundleFlag)
   TIME = property(getTime, setTime)
   INFO = property(getInfo, setInfo)
   TYPE = property(getType, setType)
   DATA = property(getData, setData)
   BUNDLE = property(getBundle, setBundle)


def tester():
   pass

if __name__ == '__main__':  # Only when run
   tester()

__package__ = "srmparserlite.splFilter"
from ..splGeneral.deco import VersionDeco
from ..splTraits.traits import Traits
import datetime
import importlib

r"""
TODO: 1. a set contains {time, info, type, (data, bundle)}
   info : (tid, loginfo, class, ctxID, connId)

TODO: 2. if no time, will match first dir's start time agaist second dir's start time
   then apply rest of the criteria

TODO: 3. if only one time for first dir, will match the time against the second dir then
   apply rest of the criteria

TODO: 4. if both have time, then find the rest of the criteria against these period of
   time

TODO: 5. AND SET : info.tid and info.loginfo and info.class and info.ctxID and info.connID
   and type and datastring (data & bundle)

TODO: 6. OR SET : all ors

TODO: 7. combine "AND" and "OR" sets


TODO: 8. criteria file:
   if read from *.spl , then result would be *_spl.log

----------
TODO: 9. if no user input from command line , spl will
   1. use current dir as 1st dir and find 2nd dir by ../SecondSiteLog
   2. use 1st dir to generate onebigfile and use it's start time as pivot for the 2nd dir

TODO: 10. if only search string provided, spl will
   1. use current dir as 1st dir and output search results
      (search against opID,data+bundle)
   2. try to use ../SecondSiteLog as 2nd dir and output search results.
   3. the time pivot is based on 1st dir.

TODO: 11. Use .spl config file.
   1. user provide -sql argument to the script and spl will look for every *.sql
      configs and generate *_sql.log result
"""

r"""
TIME : 2013-07-23T20:30:09.705+02:00 (will compare as utc timestamp)
INFO : [04116 verbose 'DatastoreGroupManager' opID=528a0d41]
TYPE : [PCM]
DATA : Processing virtual machine 'vm-6150'
BUNDLE : list of strings
-->    dynamicType = <unset>, 

-->    faultCause = (vmodl.MethodFault) null, 

-->    object = 'vim.VirtualMachine:vm-996', 

-->    privilegeId = "System.View", 

-->    msg = "Permission to perform this operation was denied.", 

--> }
"""



r"""
splParser.Parser will passes in srm traits version for filters to construct proper
object with correct SRM version traits

Filters will be used and constructed in splParser.Parser class

splConfig class will contains the sifting criteria input from either user or spl itself

Time {"TimeStr" : "2013-07-05T14:26:15.182-02:00",
      "FilterFlag" : "year,month, date,hour,min,sec, milisec"}

"""


def ApplyTimeZone(a_datetime, a_timezone):
   zoneData = datetime.datetime.strptime(a_timezone[1:], "%H:%M")
   timeDiff = datetime.timedelta(hours=zoneData.hour, minutes=zoneData.minute)
   if (a_timezone[0] == "+"):
      return a_datetime - timeDiff
   else:
      return a_datetime + timeDiff


@VersionDeco(1)
class TimeFilter(object):
   __slots__ = [
      "srmVersion",
      "dateTime",
      "filterFlag",
      "trait"]
   CodeMapping

   @staticmethod
   def GenYearDatatime(a_dateTime):
      return datetime.datetime(year=a_dateTime.year)

   @staticmethod
   def GenMonthDatatime(a_dateTime):
      return datetime.datetime(year=a_dateTime.year)

   @staticmethod
   def GenDayDatatime(a_dateTime):
      return datetime.datetime(year=a_dateTime.year)

   @staticmethod
   def GenHourDatatime(a_dateTime):
      return datetime.datetime(year=a_dateTime.year)

   @staticmethod
   def GenMinDatatime(a_dateTime):
      return datetime.datetime(year=a_dateTime.year)

   @staticmethod
   def GenSecDatatime(a_dateTime):
      return datetime.datetime(year=a_dateTime.year)

   @staticmethod
   def GenMilliSecDatatime(a_dateTime):
      return datetime.datetime(year=a_dateTime.year)

   def __init__(this, a_srmVersion, a_timeStr, a_filterFlag):
      """
      a_timeStr is the criteria for time
      """
      this.srmVersion = a_srmVersion
      this.filterFlag = a_filterFlag
      l_traitModule = importlib.import_module(Traits[this.srmVersion], __package__)
      this.trait = l_traitModule.SrmTrait()
      l_timezone = a_timeStr[this.trait.TIMEFMT["TimeZoneOffSet"]:]
      this.dateTime = datetime.datetime.strptime(
         a_timeStr[:this.trait.TIMEFMT["TimeZoneOffSet"]],
         this.trait.TIMEFMT["Format"])
      this.dateTime = ApplyTimeZone(this.dateTime, l_timezone)  # might have trouble

   def Apply(this, a_timeStr):
      l_timezone = a_timeStr[this.trait.TIMEFMT["TimeZoneOffSet"]:]
      l_dateTime = datetime.datetime.strptime(
         a_timeStr[:this.trait.TIMEFMT["TimeZoneOffSet"]],
         this.trait.TIMEFMT["Format"])
      l_dateTime = ApplyTimeZone(l_dateTime, l_timezone)  # might have trouble







      


class InfoFilter(object):
   pass


class TypeFilter(object):
   pass


class DataFilter(object):
   pass


class BundleFilter(object):
   pass

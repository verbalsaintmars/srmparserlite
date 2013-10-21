__package__ = "srmparserlite.splFilter"
from ..splGeneral.deco import VersionDeco
from ..splTraits.traits import Traits
import importlib
from datetime import tzinfo
from datetime import datetime
from datetime import timedelta


class TimeZone(tzinfo):
   __slots__ = ["timeDelta"]

   def __init__(this, a_offsetStr):
      super(tzinfo, this).__init__()
      zoneData = datetime.strptime(a_offsetStr[1:], "%H:%M")

      if (a_offsetStr[0] == "+"):
         this.timeDelta = timedelta(hours=zoneData.hour, minutes=zoneData.minute)

      else:
         this.timeDelta = -timedelta(hours=zoneData.hour, minutes=zoneData.minute)

   def utcoffset(this, dt):
      return this.timeDelta

   def dst(self, dt):
      return timedelta(0)

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


def GenYearDatatime(a_dateTime):
   return datetime(
      year=a_dateTime.year,
      month=1,
      day=1,
      tzinfo=a_dateTime.tzinfo)


def GenMonthDatatime(a_dateTime):
   return datetime(
      year=a_dateTime.year,
      month=a_dateTime.month,
      day=1,
      tzinfo=a_dateTime.tzinfo)


def GenDayDatatime(a_dateTime):
   return datetime(
      year=a_dateTime.year,
      month=a_dateTime.month,
      day=a_dateTime.day,
      tzinfo=a_dateTime.tzinfo)


def GenHourDatatime(a_dateTime):
   return datetime(
      year=a_dateTime.year,
      month=a_dateTime.month,
      day=a_dateTime.day,
      hour=a_dateTime.hour,
      tzinfo=a_dateTime.tzinfo)


def GenMinDatatime(a_dateTime):
   return datetime(
      year=a_dateTime.year,
      month=a_dateTime.month,
      day=a_dateTime.day,
      hour=a_dateTime.hour,
      minute=a_dateTime.minute,
      tzinfo=a_dateTime.tzinfo)


def GenSecDatatime(a_dateTime):
   return datetime(
      year=a_dateTime.year,
      month=a_dateTime.month,
      day=a_dateTime.day,
      hour=a_dateTime.hour,
      minute=a_dateTime.minute,
      second=a_dateTime.second,
      tzinfo=a_dateTime.tzinfo)


def GenMilliSecDatatime(a_dateTime):
   return datetime(
      year=a_dateTime.year,
      month=a_dateTime.month,
      day=a_dateTime.day,
      hour=a_dateTime.hour,
      minute=a_dateTime.minute,
      second=a_dateTime.second,
      microsecond=a_dateTime.microsecond,
      tzinfo=a_dateTime.tzinfo)

TimeFilterMap = {
   "year": GenYearDatatime,
   "month": GenMonthDatatime,
   "day": GenDayDatatime,
   "hour": GenHourDatatime,
   "min": GenMinDatatime,
   "sec": GenSecDatatime,
   "milli": GenMilliSecDatatime}


@VersionDeco(1)
class TimeFilter(object):
   __slots__ = [
      "srmVersion",
      "dateTime",
      "filterFlag",
      "trait"]

   def __init__(this, a_srmVersion, a_timeStr, a_filterFlag):
      """
      a_timeStr is the criteria for time
      """
      this.srmVersion = a_srmVersion
      this.filterFlag = a_filterFlag

      l_traitModule = importlib.import_module(Traits[this.srmVersion], __package__)
      this.trait = l_traitModule.SrmTrait()

      l_timezone = a_timeStr[this.trait.TIMEFMT["TimeZoneOffSet"]:]

      this.dateTime = datetime.strptime(
         a_timeStr[:this.trait.TIMEFMT["TimeZoneOffSet"]],
         this.trait.TIMEFMT["Format"])

      this.dateTime = this.dateTime.replace(tzinfo=TimeZone(l_timezone))
      this.dateTime = TimeFilterMap[this.filterFlag](this.dateTime)

   def ApplyLessEq(this, a_timeStr):
      """
         Apply Less Equal
      """
      l_timezone = a_timeStr[this.trait.TIMEFMT["TimeZoneOffSet"]:]
      l_dateTime = datetime.strptime(
         a_timeStr[:this.trait.TIMEFMT["TimeZoneOffSet"]],
         this.trait.TIMEFMT["Format"])
      l_dateTime = l_dateTime.replace(tzinfo=TimeZone(l_timezone))
      l_dateTime = TimeFilterMap[this.filterFlag](l_dateTime)

      return this.dateTime <= l_dateTime


class InfoFilter(object):
   pass


class TypeFilter(object):
   pass


class DataFilter(object):
   pass


class BundleFilter(object):
   pass

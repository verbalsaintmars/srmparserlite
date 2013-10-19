import datetime

v_testTime1 = "2014-07-05T14:26:15.182-08:00"  # minimum to seconds
v_testTime2 = "2014-07-05T14:26:15.182-05:00"  # minimum to seconds
MilliFormat = "%Y-%m-%dT%H:%M:%S.%f"
SecFormat = "%Y-%m-%dT%H:%M:%S"
MinFormat = "%Y-%m-%dT%H:%M"
HrFormat = "%Y-%m-%dT%H"
DateFormat = "%Y-%m-%d"
MonthFormat = "%Y-%m"
YearFormat = "%Y"

TimeFormat = {
   "Milli": ("%Y-%m-%dT%H:%M:%S.%f", -6),
   "Sec": ("%Y-%m-%dT%H:%M:%S", -10),
   "Min": ("%Y-%m-%dT%H:%M", -13),
   "Hour": ("%Y-%m-%dT%H", -16),
   "Date": ("%Y-%m-%d", -19),
   "Month": ("%Y-%m", -22),
   "Year": ("%Y", -25)}


srm_datetime1 = datetime.datetime.strptime(
   v_testTime1[:TimeFormat["Milli"][1]],
   TimeFormat["Milli"][0])

srm_datetime2 = datetime.datetime.strptime(
   v_testTime2[:TimeFormat["Milli"][1]],
   TimeFormat["Milli"][0])

srm_timezone1 = v_testTime1[-6:]
srm_timezone2 = v_testTime2[-6:]


def ApplyTimeZone(a_datetime, a_timezone):
   zoneData = datetime.datetime.strptime(a_timezone[1:], "%H:%M")
   timeDiff = datetime.timedelta(hours=zoneData.hour, minutes=zoneData.minute)
   if (a_timezone[0] == "+"):
      return a_datetime - timeDiff
   else:
      return a_datetime + timeDiff


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

tz1 = TimeZone(srm_timezone1)
tz2 = TimeZone(srm_timezone2)

srm_datetime1 = srm_datetime1.replace(tzinfo=tz1)
srm_datetime2 = srm_datetime2.replace(tzinfo=tz2)

print(srm_datetime1 > srm_datetime2)


print("------------")

Time11 = {
   "start": "Time11",
   "end": "2013-07-05T14:28:15.182-02:00",
   "flag": "milli"}

Time12 = {
   "start": "Time12",
   "end": "2013-07-05T14:28:15.182-02:00",
   "flag": "milli"}

Time21 = {
   "start": "Time21",
   "end": "2013-07-05T14:28:15.182-02:00",
   "flag": "milli"}

Time22 = {
   "start": "Time22",
   "end": "2013-07-05T14:28:15.182-02:00",
   "flag": "milli"}

Info1 = {
   "tid": "03440",
   "loginfo": "error",
   "class": "EventDomain"}  # all inside is "and"

# 04116 verbose 'DatastoreGroupManager' opID=528a0d41
Info2 = {
   "tid": "04116",
   "loginfo": "verbose",
   "class": "DatastoreGroupManager",
   "opid": "528a0d41"}  # all inside is "and"

Type1 = {}
Type2 = {}

Data1 = ()
Data2 = ()

Bundle1 = ()
Bundle2 = ()

"""
site1pack1 = {
      "time": Time,
      "info": (Info1, Info2),  # or here
      "type": (Type1, Type2),  # or here
      "data": (Data1, Data2),  # or here
      "bundle": (Bundle1, Bundle2)}  # or here
"""

site1pack11 = {
      "time": Time11,
      "info": (Info1, Info2)}

site1pack12 = {
      "time": Time12,
      "info": (Info1, Info2)}

site1pack21 = {
      "time": Time21,
      "info": (Info1, Info2)}

Site1 = {
      "dir": r"/myfiles/Source/vsProject/srmparserlite/pplog/",
      "criteria": (site1pack11, site1pack12),
      "type": "config",  # ignore other parameter. gen same splsync_{nu}.log on each site
      "dayoffset": 1}  # more than 1 day will regenerate the one big file, 0 will always
                       # generate

Site2 = {
      "dir": r"/myfiles/Source/vsProject/srmparserlite/sslog/",
      "criteria": (site1pack21,),
      "type": "sync",  # ignore other parameter. gen same splsync_{nu}.log on each site
      "dayoffset": 1}  # more than 1 day will regenerate the one big file, 0 will always
"""
syncSite2 = {
      "dir": r"/myfiles/Source/vsProject/srmparserlite/sslog/",
      "condition": site1pack,
      "type": "sync",
      "dayoffset": 1,  # more than 1 day will regenerate
      "forceflag": True}
"""
singleSite = (Site1, Site2)


class PrepareConfig(object):
   __slots__ = ["sites", "syncState", "syncTime"]

   def __init__(this, a_sites):
      this.sites = a_sites
      this.syncTime = []
      this.syncState = False

   def CheckModifyState(this):
      v_tmpConfig = None

      for l_site in this.sites:

         if l_site["type"] == "sync":

            if this.syncState is False:

               for l_criteria in l_site["criteria"]:
                  this.syncTime.append(l_criteria["time"])

               this.syncState = True
               v_tmpConfig = l_site
               break

      if this.syncState is True:

         for l_site in this.sites:
            if l_site is v_tmpConfig:
               continue
            i = 0
            for l_criteria in l_site["criteria"]:
               try:
                  l_criteria["time"] = this.syncTime[i]
                  i += 1
               except IndexError:
                  break

pp = PrepareConfig(singleSite)
pp.CheckModifyState()
print(singleSite[0]["criteria"][1]["time"]["start"])


print("------------------------------")
import multiprocessing.pool as mpo

class TEST(object):
   def __call__(this, a_in):
      print(a_in)

l_tpool = mpo.ThreadPool(processes=mpo.cpu_count())
l_result = l_tpool.map_async(TEST(), (1,2,3), 1)
l_result.get()

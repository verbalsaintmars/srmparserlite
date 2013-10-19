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


import re

#     this.infoFmt = r"\[" \
#                    r"(?P<TID>\d+)\s" \
#                    r"(?P<LOGINFO>\w+)\s" \
#                    r"\'(?P<CLASS>\w+)\'\s" \
#                    r"(?:connID=(?P<CONNID>.*?))?\s" \
#                    r"(?:ctxID=(?P<CTXID>.*?))?\s" \
#                    r"(?:opID=(?P<OPID>.*?))?\]"
#     this.typeFmt = r"\[(?P<TYPE>\w+)\]"

#ss = r"2013-07-23T20:30:09.780-02:00 [04116 verbose 'DatastoreGroupManager'" \
#   " opID=528a0d41] [XXXX] Processing virtual machine 'vm-6152'"
ss = r"2013-07-23T20:30:09.780-02:00 [04116 verbose 'DatastoreGroupManager' opID=sdfsf ctxID=123" \
   "] Processing virtual machine 'vm-6152'"

infoss = r"[04116 verbose 'DatastoreGroupManager' connID=123321 opID=528a0d41]"

print(ss)

lineRegexFmt = \
   r"(?P<TIME>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[\+\-]\d{2}:\d{2})" \
   r"\s" \
   r"(?:\[(?P<INFO>(?P<TID>\d+)\s(?P<LOGINFO>\w+)\s\'" \
   r"(?P<CLASS>\w+)\'\s?(?P<OTHERINFO>.*?))\])\s?" \
   r"(?:\[(?P<TYPE>.*?)\])?\s?" \
   r"(?P<DATA>.*)"


class TEST(object):
   def ha(this):
      this.lineRegexFmt = \
         r"(?P<TIME>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[\+\-]\d{2}:\d{2})" \
         r"\s" \
         r"(?:\[(?P<INFO>(?P<TID>\d+)\s(?P<LOGINFO>\w+)\s\'" \
         r"(?P<CLASS>\w+)\'\s?(?P<OTHERINFO>.*?))\])\s?" \
         r"(?:\[(?P<TYPE>.*?)\])?\s?" \
         r"(?P<DATA>.*)"


inforeg = r"(?P<INFO>(?:\[\d+\s\w+\s\'\w+\'.*?\]))"


l_m = re.match(lineRegexFmt, ss)
#l_m = re.match(inforeg, infoss)

print(l_m.group("TIME"))
print(l_m.group("INFO"))
print(l_m.group("TID"))
print(l_m.group("LOGINFO"))
print(l_m.group("CLASS"))
print(l_m.group("OTHERINFO"))
print(l_m.group("TYPE"))
print(l_m.group("DATA").strip())

#print(l_m.group("TIME"))
#print(l_m.group("INFO"))
#print(l_m.group("TYPE"))
#print(l_m.group("DATA"))

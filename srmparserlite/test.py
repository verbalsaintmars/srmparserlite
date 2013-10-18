import datetime

v_testTime1 = "2014-07-05T14:26:15.182-02:00"  # minimum to seconds
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

print (ApplyTimeZone(srm_datetime1, srm_timezone1))


tmp1 = ApplyTimeZone(srm_datetime1, srm_timezone1)
tmp2 = ApplyTimeZone(srm_datetime2, srm_timezone2)

com1 = datetime.datetime(year=tmp1.year, month=tmp1.month, day=tmp1.day)
com2 = datetime.datetime(year=tmp2.year, month=tmp2.month, day=tmp2.day)
print(com1 > com2)

print("-----------")


class TEST(object):
   TMP = 10

   @staticmethod
   def HA():
      print(TEST.TMP)

TEST.HA()

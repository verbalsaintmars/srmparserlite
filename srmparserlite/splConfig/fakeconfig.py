__package__ = "srmparserlite.splConfig"
"""
.spl file:

Time {"TimeStr" : "2013-07-05T14:26:15.182-02:00",
      "FilterFlag" : "year,month, day,hour,min,sec, milli"}

"""

Time = {
   "start": "2013-07-05T14:26:15.182-02:00",
   "end": "2013-07-05T14:28:15.182-02:00",
   "flag": "milli"}

Info1 = {}  # all inside is "and"

Type1 = {}

Data1 = ()

Bundle1 = ()

Info2 = {}

Type2 = {}

Data2 = ()

Bundle2 = ()

Info3 = {}

Type3 = {}

Data3 = ()

Bundle3 = ()


site1pack = {
      "time": Time,
      "info": (Info1, Info2, Info3),  # or here
      "type": (Type1, Type2, Type3),  # or here
      "data": (Data1, Data2, Data3),  # or here
      "bundle": (Bundle1, Bundle2, Bundle3)}  # or here


Site1 = {
      "dir": r"/myfiles/Source/vsProject/srmparserlite/pplog/",
      "condition": site1pack,
      "dayoffset": 1,  # more than 1 day will regenerate
      "forceflag": True}



Sites = (Site1,)

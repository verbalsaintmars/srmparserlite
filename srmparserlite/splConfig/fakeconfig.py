__package__ = "srmparserlite.splConfig"
"""
Time {"TimeStr" : "2013-07-05T14:26:15.182-02:00",
      "FilterFlag" : "year,month, day,hour,min,sec, milli"}

type : sync , config
"""

Time11 = {
   "start": "2013-07-23T20:30:09.780+02:00",
   "end": "2013-07-23T23:26:02.931+02:00", #not included [,)
   "flag": "milli"}

Time12 = {
   "start": "2013-07-23T21:34:35.182+02:00",
   "end": "2013-07-23T23:26:02.837+02:00",
   "flag": "milli"}

Time21 = {
   "start": "2013-07-23T21:34:35.182+02:00",
   "end": "2013-07-23T23:26:02.837+02:00",
   "flag": "milli"}

Time22 = {
   "start": "Time22",
   "end": "2013-07-05T14:28:15.182-02:00",
   "flag": "milli"}

Info1 = ("03440", "error", "EventDomain")

# 04116 verbose 'DatastoreGroupManager' opID=528a0d41
Info2 = ("verbose",)

Type1 = ("PCM",)
Type2 = ("HAH",)

Data1 = ("vm-6152",)
Data2 = ("vm-6150",)

Bundle1 = ("vm-4005",)
Bundle2 = ("vm-2614",)

"""
site1pack11 = {
      "name": "Site_1_pack11",
      "time": Time11,
      "info": (Info1, Info2),  # inside info it's OR , between info/type/data/bundle is
                               # AND
      "type": (Type1, Type2),  # or here
      "data": (Data1, Data2),  # or here
      "bundle": (Bundle1, Bundle2),  # or here
      "logfilename": "my_result_pack1"}  # must end with _ , reader will take care of this
"""

site1pack11 = {
      "name": "Site_1_pack11",
      "time": Time11,
      "info": (Info1, Info2),
      "type": (Type1, Type2),  # or here
      "data": (),  # or here
      "bundle": (Bundle1, Bundle2),  # or here
      "logfilename": "my_result_pack1"}  # must end with _ , reader will take care of this

site1pack12 = {
      "name": "Site_1_pack12",
      "time": Time12,
      "info": (Info1, Info2),
      "logfilename": "my_result_pack2"}  # must end with _ , reader will take care of this

site1pack21 = {
      "name": "Site_1_pack21",
      "time": Time21,
      "info": (Info1, Info2),
      "logfilename": "your_result_pack1"}
       # must end with _ , reader will take care of this

Site1 = {
      "name": "Site_1",
      "dir": r"/myfiles/Source/vsProject/srmparserlite/pplog/",
      "criteria": (site1pack11,),
      "type": "config",  # ignore other parameter. gen same splsync_{nu}.log on each site
      "dayoffset": 1}

Site2 = {
      "name": "Site_2",
      "dir": r"/myfiles/Source/vsProject/srmparserlite/sslog/",
      "criteria": (site1pack21,),
      "type": "config",  # ignore other parameter. gen same splsync_{nu}.log on each site
      "dayoffset": 1}  # more than 1 day will regenerate the one big file, 0 will always
"""
syncSite2 = {
      "dir": r"/myfiles/Source/vsProject/srmparserlite/sslog/",
      "condition": site1pack,
      "type": "sync",
      "dayoffset": 1,  # more than 1 day will regenerate
      "forceflag": True}
"""
singleSite = (Site1,)
doubleSite = (Site2, Site1)

__package__ = "srmparserlite.splConfig"
"""
Time {"TimeStr" : "2013-07-05T14:26:15.182-02:00",
      "FilterFlag" : "year,month, day,hour,min,sec, milli"}

type : sync , config
"""

Time11 = {
   "start": "2013-07-23T21:34:35.182+02:00",
   "end": "2013-07-23T23:26:02.837+02:00",
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
      "info": (Info1, Info2),
      "logfilename": "my_result_pack1"}  # must end with _ , reader will take care of this

site1pack12 = {
      "time": Time12,
      "info": (Info1, Info2),
      "logfilename": "my_result_pack2"}  # must end with _ , reader will take care of this

site1pack21 = {
      "time": Time21,
      "info": (Info1, Info2),
      "logfilename": "your_result_pack1"}
       # must end with _ , reader will take care of this

Site1 = {
      "dir": r"/myfiles/Source/vsProject/srmparserlite/pplog/",
      "criteria": (site1pack11, site1pack12),
      "type": "config",  # ignore other parameter. gen same splsync_{nu}.log on each site
      "dayoffset": 1}

Site2 = {
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

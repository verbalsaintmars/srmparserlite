__package__ = "srmparserlite.splConfig"

Time11 = {
   "start": "2013-07-23T20:30:09.780+02:00",
   "end": "2014-07-23T23:26:02.930+02:00",  # not included [,)
   "flag": "milli"}  # milli sec min hour day month year

Time12 = {
   "start": "2013-07-23T20:30:09.780+02:00",
   "end": "2013-07-23T23:26:02.837+02:00",
   "flag": "milli"}

Info1 = ("03528", "error",)  # it's an AND search

# 04116 verbose 'DatastoreGroupManager' opID=528a0d41
Info2 = ("04300",)

Type1 = ("XXX",)
Type2 = ("PCM",)

Data1 = ("com.vmware.vcDr.ProtectedVmRemovedEvent",)
Data2 = ("vm-6150",)

Bundle1 = ()
Bundle2 = ("System.Read",)


# Criterion inside time, info, type, data, bundle is OR
# time & info & type & data & bundle is AND
site1pack11 = {
      "name": "Site_1_pack11",
      "time": Time12,
      "info": (),  # or inside 'info'
      "type": (),  # or insude 'type'
      "data": (Data1,),  # or here
      "bundle": (Bundle2,),  # or here
      "logfilename": "HA_result_pack1"}  # must end with _ , reader will take care of this

site1pack12 = {
      "name": "Site_1_pack12",
      "time": Time12,
      "info": (),  # or inside 'info'
      "type": (),  # or insude 'type'
      "data": (Data1,),  # or here
      "bundle": (Bundle2,),  # or here
      "logfilename": "my_result_pack2"}  # must end with _ , reader will take care of this


Site1 = {
      "name": "Site_1",
      "dir": r"/myfiles/Source/vsProject/srmparserlite/pplog/",
      "criteria": (site1pack12, site1pack11),
      "type": "config",  # ignore other parameter. gen same splsync_{nu}.log on each site
      "dayoffset": 1}

Site2 = {
      "name": "Site_2",
      "dir": r"/myfiles/Source/vsProject/srmparserlite/sslog/",
      "criteria": (site1pack12, site1pack11),
      "type": "config",  # ignore other parameter. gen same splsync_{nu}.log on each site
      "dayoffset": 1}

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

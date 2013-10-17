#!/usr/bin/env python
import sys
import re
from datetime import datetime
from datetime import timedelta

#global variable  : srm_
#arguments        : a_
#private variable : _X
#mangling         : __X
#tmp variable     : v_
#local variable   : l_

print("testing " + sys.argv[0])
#srmparserlite pp_stime~pp_etime ss_stime~ss_etime pp_dir  ss_dir {OpID, Thread, Cat, Loginfo} regex


#2013-07-05T14:26:14.182+02:00
v_testTime = "2013-07-05T14:26:14.182-02:00"
logTimeFormat = "%Y-%m-%dT%H:%M:%S.%f"
srm_datetime = datetime.strptime(v_testTime[:-6], logTimeFormat)
srm_timezone = v_testTime[-6:]


tmphead = r"Section for VMware vCenter Site Recovery Manager, pid=2344, version=5.0.1, build=build-633117, option=Release"

tmpstr1 = r"2013-07-23T20:30:09.705+02:00 [04116 verbose 'DatastoreGroupManager' opID=528a0d41] Processing virtual machine 'vm-6150'"

tmpstr2 = r"2013-07-23T20:30:31.089+02:00 [03992 error 'EventDomain'] Failed to re-post'com.vmware.vcDr.ProtectedVmRemovedEvent' event: (vim.fault.NoPermission) {"

"""
-->    dynamicType = <unset>, 

-->    faultCause = (vmodl.MethodFault) null, 

-->    object = 'vim.VirtualMachine:vm-4005', 

-->    privilegeId = "System.Read", 

-->    msg = "Permission to perform this operation was denied.", 

--> }"""


tmpstr3 = r"2013-07-23T20:31:13.300+02:00 [04328 warning 'LocalVC' connID=vc-admin-7b48 opID=344383e1:ef6] [PCM] CreateFilter failed for token '94' after '63507' attempts."


tmpstr4 = r"-->    faultCause = (vmodl.MethodFault) null, "
tmpstr5 = r"i-->    faultCause = (vmodl.MethodFault) null, "

tmpStrs = [tmphead, tmpstr1, tmpstr2, tmpstr3, tmpstr4]

"""
Reason: (vim.fault.NoPermission) {"
-->    dynamicType = <unset>, 

-->    faultCause = (vmodl.MethodFault) null, 

-->    object = 'vim.VirtualMachine:vm-996', 

-->    privilegeId = \"System.View\", 

-->    msg = \"Permission to perform this operation was denied.\", 

--> }"""



def ApplyTimeZone(a_datetime, a_timezone):
   zoneData = datetime.strptime(a_timezone[1:], "%H:%M")
   timeDiff = timedelta(hours=zoneData.hour, minutes=zoneData.minute)
   if (a_timezone[0] == "+"):
      return a_datetime - timeDiff
   else:
      return a_datetime + timeDiff

print (ApplyTimeZone(srm_datetime, srm_timezone))

#headertmp = r"Section for VMware vCenter Site Recovery Manager, pid=2344, version=5.0.1, build=build-633117, option=Release"


headertmp = r"vmware-dr-4254.log"

#headertmp = r"test"

lineRegexFormat = r".*?-(?P<FNUM>\d+)\.log"

#lineRegexFormat = r"2013-07-23T20:31:13.300+02:00 [04328 warning 'LocalVC' " \
#"connID=vc-admin-7b48 opID=344383e1:ef6] [PCM] CreateFilter failed for token '94' after '63507' attempts."


v_m = re.match(lineRegexFormat, headertmp)

if v_m is not None:
   print(v_m.string)
   print(v_m.group("FNUM"))
else:
   pass

"""
TODO: 1. Read one large file line by line through SrmParser and apply filter
TODO: 2. Filter OR mechanism

TODO: 3. sites with different time.
Compare with UTC time
e.g
local time      12:00      9:00
utc time        10:00      10:00
User input local time will convert to utc time and compare against utc time inside the log
User can input just hour or hour:min or hour:min:sec or hour:min:sec:microsec

User can input only one site's time, parser will match secondary site's time
and generate proper time section

TODO: 4. search INFO : TID OPID LOGTYPE Data Bundle

"""






@VersionDeco(1)
class SrmParser(object):
   """
      Per thread per file.
      By line.
      Input a line to SrmParser, SrmParser will generate a
      HeadLineClass or LineClass

      SrmParser can be used to parse again with the final output single large file
      to do the second/third etc phase scan (because the bundle could be cut into
      different files, so rescan again with the single file could help)
   """
   # An iterator class
   __slots__ = [
         "LineClass",
         "HeadLineClass",
         "LineObj",
         "HeadLineObj",
         "HandleClass",
         "HandleObj",
         "FilterClass",
         "FilterObj",
         "LineBuffer",
         "FileName"]

   def __init__(this, a_fileName, a_lineClass, a_headlineClass, a_handleClass):
      this.FileName = a_fileName
      this.LineClass = a_lineClass
      this.HeadLineClass = a_headlineClass
      this.HeadLineObj = this.HeadLineClass()
      this.HandleClass = a_handleClass
      this.HandleObj = this.HandleClass(this.FileName)
      this.LineBuffer = []

   def ApplyTimeZone(this, a_datetime, a_timezone):
      zoneData = datetime.strptime(a_timezone[1:], "%H:%M")
      timeDiff = timedelta(hours=zoneData.hour, minutes=zoneData.minute)
      if (a_timezone[0] == "+"):
         return a_datetime - timeDiff
      else:
         return a_datetime + timeDiff

   def TakeLine(this, a_line):
      """
      If line starts with "-->" , SrmParser will retain previous LineClass object
      and put this line into previous LineClass object's Data property

      If next line still starts with "-->" , SrmParser will add/append this line into
      previous LineClass object's Data property
      """

      """
      r"2013-07-23T20:31:13.300+02:00 [04328 warning 'LocalVC' connID=vc-admin-7b48
      opID=344383e1:ef6] [PCM] CreateFilter failed for token '94' after '63507' attempts."

r"Section for VMware vCenter Site Recovery Manager, pid=2344, version=5.0.1, build=build-633117, option=Release"
      """
      print("SrmParser.TakeLine : " + a_line)

      if not this.HeadLineObj.PROCESSEDFLAG:
         l_match = re.match(this.HeadLineClass.Formater.HEADERFMT, a_line)

         if l_match is not None:
            this.HeadLineObj.PROCESSEDFLAG = True
            this.HeadLineObj.PID = l_match.group("PID")
            this.HeadLineObj.VERSION = l_match.group("VERSION")
            this.HeadLineObj.BUILD = l_match.group("BUILD")
            this.HeadLineObj.OPTION = l_match.group("OPTION")
            print(this.HeadLineObj.PID)
            print(this.HeadLineObj.VERSION)
            print(this.HeadLineObj.BUILD)
            print(this.HeadLineObj.OPTION)
            #TODO: write to tmp_{nu}.ltmp file

         else:
            raise NoHeaderLineException()

      else:
         l_match = re.match(this.LineClass.Formater.LINEFMT, a_line)

         if l_match is not None:
            this.LineObj = this.LineClass()
            this.LineObj.TIME = l_match.group("TIME")
            this.LineObj.INFO = l_match.group("INFO")
            this.LineObj.TYPE = l_match.group("TYPE")
            this.LineObj.DATA = l_match.group("DATA")
            """
               Algorithm:
               in LINEFMT
                  if LineBuffer is empty, insert new one into it.
                  else let HandleObj to handle it and pop it out of LineBuffer
                     and insert this new one

               in BUNDLEFMT
                  if LineBuffer is empty, insert new one and add this bundle to it.
                  else append bundle to the existing LineObj inside the LineBuffer

               Till end of reading file, flush out the LineBuffer to HandleObj
            """
            try:
               l_LineObj = this.LineBuffer.pop()
               """
                  TODO: HandleObj handle output
               """



               this.LineBuffer += this.LineObj
            except:
               this.LineBuffer += this.LineObj

            print(this.LineObj.TIME)
            print(this.LineObj.INFO)
            print(this.LineObj.TYPE)
            print(this.LineObj.DATA)

         else:
            l_match = re.match(this.LineClass.Formater.BUNDLEFMT, a_line)

            if l_match is not None:
               try:
                  this.LineBuffer[0].BUNDLE = l_match.string
               except:
                  l_LineObj = this.LineClass()
                  l_LineObj.BUNDLE = l_match.string
                  this.LineBuffer += l_LineObj

               print(this.LineObj.BUNDLE)

            else:
               #TODO: Write into a file {readfile name, line, data} that the parser
               # does not know it's format
               raise UnSupportFormatException(a_line)



@VersionDeco(1)
class HandleClass(object):

   def __init__(this):
      pass

   def Execute(this):
      this.Run()




SpParameters = (LineClass501, HeadLineClass501)

sp = SrmParser(*SpParameters)


for strs in tmpStrs:
   sp.TakeLine(strs)

"""
------------------------
"""
import argparse
parser = argparse.ArgumentParser(description='SRM Log Parser Lite')

parser.add_argument("pp_start_time", help="Start Time of Primary Site Log Section")
parser.add_argument("pp_end_time", help="End Time of Primary Site Log Section")
parser.add_argument("ss_start_time", help="Start Time of Secondary Site Log Section")
parser.add_argument("ss_end_time", help="End Time of Secondary Site Log Section")

parser.add_argument("pp_dir", help="Primary Site Log Directory")
parser.add_argument("ss_dir", help="Secondary Site Log Directory")

parser.add_argument("tag_keys", help="Secondary Site Log Directory")
parser.add_argument("search_regex", help="Secondary Site Log Directory")

parser.parse_args()

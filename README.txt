===============
SRM Parser Lite
===============
Purpose of creating Srm Parser Lite
While debugging through the logs, it's a burden for engineers to grep the log with
keywords in a certain range of time and criteria.

Engineers need a better tool that could help them to parse the log in a synced log time
between sites (including VC's log), and also giving the criteria that needed through
parsing.

With Srm Parser Lite, we could extremely reduce the engineer's time from combing around
several logs between sites, and only focus on certain time range and criteria that
engineers need for debugging.


Features
========
* Designed to deal with different version of SRM's log. (VC's log will be implemented on
Phase II)
* Handles gz files.
* Uses single yaml file to config.
* Deals with multiple sites(1 and up), each site can have multiple search criteria.
(Explain below)
* Will log down the SRM log with wrong/not supported format.
* Run in parallel.

Install
========
InstallDownload source code from github: https://github.com/verbalsaintmars/srmparserlite
Put the directory that source code resides into the $PYTHONPATH environment variable,
or put the source under python's local
./site-packages directory

Note: Will introduce a .egg format installation.

Run
===
srmparser.py : main script. This file can be put under any path which is in $PATH
environment variable.

When srmparser.py runs, it will by default read splconfig.yml under current directory
(i.e the directory where srmparser.py is being called)

Srm Parser Lite will generate these files in each site directory:
* FileName_{num}.log  : FileName is defined in yaml file per criterion. The result log file.
* FileName_UnsupportFormat_{num}.log  : The log file contains lines that are not recognized
by Srm Parser Lite.
* OneBigLog.log  : log of all {gz} or {log}

If the directory contains gz and log format files, Srm Parser Lite will use gz format
files to generate OneBigLog.log


Config
======
Sample splconfig.yml_ file
.. _splconfig.yml: http://goo.gl/hKtGKZ

yaml is a key : value based config format.
Srm Parser Lite will start parsing from key : **sites**
i.e sites: ["srmSite1", "srmSite2"]

As we can see, there are 2 sites will be configured.
The name of sites doesn't matter, it's only a key name.
However, key name under:
* Each site
* Each criterion
* Each Time
must go by specified defines, otherwise Srm Parser Lite could not know information that it
needs.

Here's the detail of those static key name under each category:


Each site
   - name : the site name (for error log purpose)
   - dir  : the log location (contains gz or log format logs. gz format go by
            vmware-dr-{number}.log.gz , log format go by vmware-dr-{number}.log
            The format can be changed from *srmparserlite/splTraits/filefmt.py* file
   - criteria : each site can have multiple criteria. Each criterion is independent
                from each other. Explain below.
   - type  : can be 'config' or 'sync'. If any one of the sites it's type is 'sync'
             (first come, fist as pivot), Srm Parser Lite will sync other sites' time
             with this site's criteria. if this site has 2 criteria, every other site
             which has criteria less equal then 2 will be synced with this site's time
             criteria.
             If the type is 'config', each site will go by it's own time criteria.
   - dayoffset : if it's set to 0, the OneBigLog.log will be generated always.
                 If it's set > 0, it's unit is day, which means 1 means if the current
                 OneBigLog.log file is older than 1 day, it will be regenerated.
                 OneBigLog.log file name can be
                 changed in *srmparserlite/splTraits/filefmt.py*


For explaination purpose, here's a sample log line:

2013-10-04T18:23:41.979-07:00 [06324 verbose 'HttpConnectionPool-000000'] [PCM]
HttpConnectionPoolImpl created. maxPoolConnections = 40; idleTimeout = 900000000;
maxOpenConnections = 10; maxConnectionAge = 0 { 
--> dynamicType = <unset>, 
--> faultCause = (vmodl.MethodFault) null, 
--> object = 'vim.VirtualMachine:vm-2614', 
--> privilegeId = "System.View", 
--> msg = "Permission to perform this operation was denied.", 
--> }

Each criterion

   - name : the name of this criteria. For log and debug purpose.
   - time : time object. Explain below.
   - info : giving criteria to search in [06324 verbose 'HttpConnectionPool-000000']
            section.
            The rule is as follows:
               - info1: ["06324 ", "verbose"] it's an AND.
                 which means that any log which has info '06324' AND 'verbose' will
                 pass the filter.

               - info2: ["HttpConnectionPool-000000"] , under info,
                 we can have *info: [info1, info2]* , this is a OR,
                 which means the log either has ["06324 ", "verbose"] OR
                 ["HttpConnectionPool-000000"] will pass the filter.
                 This provides the flexibility of filtering.

   - type : give criteria to search in [PCM] section. Same rule as info.
   - data : give criteria to search in "HttpConnectionPoolImpl created.
            maxPoolConnections = 40; idleTimeout = 900000000; maxOpenConnections = 10;
            maxConnectionAge = 0" section. Same rule as info.
   - bundle : give criteria to search in "-->" or "[#2] -->" section. Same rule as info.
   - logfilename : The log file name that user want this criterion be logged as.
                   Srm Parser Lite will generate logs with "logfilename_{number}.log"
                   under each site's dir.

All of these matching regex can be modified/added in *srmparserlite/splTraits*
srm500_t.py is used for SRM version 5.0.0.
This file is the root trait for all SRM version 5.0.x.
SRM version 5.0.3 can inherit 5.0.0 base trait. example in srm503_t.py

Each Time
   - start : the start time criterion. Must be in 2013-10-04T18:23:41.979-07:00 format
            (i.e including UTC offset)
            Srm Parser Lite is comparing time in UTC time. Which means, if each site is
            in different time zone, the time comparison won't be affected.
            Srm Parser Lite will compare the time in UTC.

   - end : the end time criterion. Must be in 2013-10-04T18:23:41.979-07:00 format
            (i.e including UTC offset)

   - flag : there are 'year' , 'month' , 'day' , 'hour' , 'min' , 'sec' , 'milli' flags.
            If it's 'milli', Srm Parser Lite will compare the whole time into ms.
            'month' will compare 'yeah' and 'month'. 'hour' will compare down to
            'year month day hour' etc.

The Time filter module is here : *srmparserlite/splFilter/filterr.py*
With this design, we could setup the same criteria for different sites, different sites'
different criteria easily without redundant settings.


Source code explain
===================
- srmparserlite/splTraits : All the traits are under this dir. Different version,
              general file format etc.
-- srmparserlite/splTraits/traits.py : has the mapping of "version" : "whichTrait.py"
                         and "version" : "whichLineClass.py"
- srmparserlite/splLineClass : log line format. Seperate with different version.

- srmparserlite/splParser : parsing logic

- srmparserlite/splGeneral : decoration class and exception class

- srmparserlite/splFilter : filter class

- srmparserlite/splFileManager : handles all file io

- srmparserlite/splConfig : yaml config handle and fakeconfig in .py format

- bin/spl.py : main entry file.

- srmparserlite/unit_test/test.py : unit test.
                                    It tests each major function in Srm Parser Lite


TODO List
=========
- VC support
- Command line argument support
- Web based Srm Parser Lite support / backend db support
- SPL server to support more and faster log parsing

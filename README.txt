===============
SRM Parser Lite
===============
Purpose of creating Srm Parser Lite
During debugging through the logs, it's a burden for engineers to grep the log with
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
========
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
========
Sample splconfig.yml file
yaml is a key : value based config format.
Srm Parser Lite will start parsing from key : sites
sites: ["srmSite1", "srmSite2"]
As we can see, there are 2 sites will be configured. The name of sites doesn't matter, it's only a key name. However, key name under




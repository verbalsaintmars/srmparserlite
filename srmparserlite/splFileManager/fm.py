"""
DONE: 1. scan given directories for files , 1 primary, 1 secondary / provide filefmt.py
DONE: 2. If contains zipped file, unzip it into one large file, if the large file exist,
         skip unzipping, skip checking .log files, always unzip gz files first
DONE: 3. If contains .log files, concat it into one large file
TODO: 4. Mix, dir contains zipped and log files. sort zipped and log file into list.
         unzip zip file , concat with log files, all into one large file
"""
__package__ = "srmparserlite.splFileManager"

from ..splGeneral.deco import VersionDeco
from ..splTraits import filefmt
import os.path
import threading


@VersionDeco(1)
class ReadBigFile(object):
   """
   Thread safe
   """
   __slots__ = ["dirRoot"]

   def __init__(this, a_dirRoot):
      this.dirRoot = a_dirRoot

   def Read(this):
      import os
      with open(
            os.path.join(
               os.path.normpath(this.dirRoot),
               filefmt.OneBigLogFileName())) as l_bfileObj:

               for l_line in l_bfileObj:
                  yield l_line



@VersionDeco(1)
class GenBigFile(object):
   __slots__ = [
         "firstDir",
         "secDir",
         "firstGzFiles",
         "secGzFiles",
         "firstLogFiles",
         "secLogFiles"]

   def __init__(this):
      this.firstGzFiles = []
      this.secGzFiles = []
      this.firstLogFiles = []
      this.secLogFiles = []

   def ScanDir(this, a_1dir, a_2dir=None):
      """
      Passes in first and second dir root
      """
      import glob
      import re
      this.firstDir = os.path.normpath(a_1dir)

      l_firstGi = glob.iglob(
            os.path.join(
               this.firstDir, "*.gz"))

      for gzfn in l_firstGi:
         l_m = re.match(filefmt.SrmLogGzFileNameFormater(), os.path.basename(gzfn))
         if l_m is not None:
            this.firstGzFiles.append(gzfn)

      if this.firstGzFiles.__len__() == 0:
         this.firstGzFiles = None

         l_firstLi = glob.iglob(
            os.path.join(
               this.firstDir, "*.log"))

         for logfn in l_firstLi:
            l_m = re.match(filefmt.SrmLogFileNameFormater(), os.path.basename(logfn))
            if l_m is not None:
               this.firstLogFiles.append(logfn)

         print(this.firstLogFiles)

         if this.firstLogFiles.__len__() == 0:
            this.firstLogFiles = None
            this.firstDir = None
      else:
         this.firstLogFiles = None

      if a_2dir is not None:
         this.secDir = os.path.normpath(a_2dir)
         l_secGi = glob.iglob(
            os.path.join(
               this.secDir, "*.gz"))

         for gzfn in l_secGi:
            l_m = re.match(filefmt.SrmLogGzFileNameFormater(), os.path.basename(gzfn))
            if l_m is not None:
               this.secGzFiles.append(gzfn)

         if this.secGzFiles.__len__() == 0:
            this.secGzFiles = None

            l_secLi = glob.iglob(
               os.path.join(
                  this.secDir, "*.log"))

            for logfn in l_secLi:
               l_m = re.match(filefmt.SrmLogFileNameFormater(), os.path.basename(logfn))
               if l_m is not None:
                  this.secLogFiles.append(logfn)

            print(this.secLogFiles)

            if this.secLogFiles.__len__() == 0:
               this.secDir = None
               this.secLogFiles = None
         else:
            this.secLogFiles = None

   def GzThread(this, a_dirName, a_gzlist):
      import zipper
      l_unzipper = zipper.Unzipper()
      with open(os.path.join(a_dirName, filefmt.OneBigLogFileName()), "w") as fh:
         for fn in a_gzlist:
            l_unzipper.Decompress(fn, fh)

   def LogThread(this, a_dirName, a_loglist):
      import logger
      l_logger = logger.ConcatLog()
      with open(os.path.join(a_dirName, filefmt.OneBigLogFileName()), "w") as fh:
         for fn in a_loglist:
            l_logger.TakeFile(fn, fh)

   def GenSingleFile(this):
      l_firstDir = None
      l_secDir = None

      if this.firstGzFiles is not None:
         this.firstGzFiles.sort()  # Sort files! Important!
         l_args = (this.firstDir, this.firstGzFiles)
         l_firstDir = threading.Thread(target=this.GzThread, args=l_args)
         l_firstDir.start()
      elif this.firstLogFiles is not None:
         this.firstLogFiles.sort()  # Sort files! Important!
         l_args = (this.firstDir, this.firstLogFiles)
         l_firstDir = threading.Thread(target=this.LogThread, args=l_args)
         l_firstDir.start()

      if hasattr(this, "secDir"):
         if this.secGzFiles is not None:
            this.secGzFiles.sort()  # Sort files! Important!
            l_args = (this.secDir, this.secGzFiles)
            l_secDir = threading.Thread(target=this.GzThread, args=l_args)
            l_secDir.start()
         elif this.secLogFiles is not None:
            this.secLogFiles.sort()  # Sort files! Important!
            l_args = (this.secDir, this.secLogFiles)
            l_secDir = threading.Thread(target=this.LogThread, args=l_args)
            l_secDir.start()

      if l_secDir:
         print("----l_secDir")
         l_secDir.join()
      if l_firstDir:
         print("----l_firstDir")
         l_firstDir.join()

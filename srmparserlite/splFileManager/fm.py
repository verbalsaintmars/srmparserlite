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
import threading

class FileManager(object):
   __slots__ = [
         "firstDir",
         "secDir",
         "firstGzFiles",
         "secGzFiles",
         "fistLogFiles",
         "secLogFiles"]

   def __init__(this):
      pass

   def ScanDir(this, a_1dir, a_2dir=None):
      import glob
      import os.path
      this.firstDir = a_1dir

      this.firstGzFiles = glob.glob(os.path.join(
         os.path.normpath(a_1dir),
         filefmt.SrmLogGzFileNameFormater()))

      if this.firstGzFiles.__len__() == 0:
         this.firstGzFiles = None
         this.firstLogFiles = glob.glob(os.path.join(
            os.path.normpath(a_1dir),
            filefmt.SrmLogFileNameFormater()))
         if this.firstLogFiles.__len__() == 0:
            this.firstLogFiles = None
      else:
         this.firstLogFiles = None

      if a_2dir is not None:
         this.secDir = a_2dir
         this.secGzFiles = glob.glob(os.path.join(
            os.path.normpath(a_2dir),
            filefmt.SrmLogGzFileNameFormater()))
         if this.secGzFiles.__len__() == 0:
            this.secGzFiles = None
            this.secLogFiles = glob.glob(os.path.join(
               os.path.normpath(a_2dir),
               filefmt.SrmLogFileNameFormater()))
            if this.secLogFiles.__len__() == 0:
               this.secLogFiles = None
         else:
            this.secLogFiles = None

      l_firstDir = threading.Thread(target=)
      l_secDir = threading.Thread(target=)

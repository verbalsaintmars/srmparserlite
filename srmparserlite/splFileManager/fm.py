"""
DONE: 1. scan given directories for files , 1 primary, 1 secondary / provide filefmt.py
DONE: 2. If contains zipped file, unzip it into one large file, if the large file exist,
         skip unzipping, skip checking .log files, always unzip gz files first
DONE: 3. If contains .log files, concat it into one large file
DONE: 4. time in the spl will be compare as epoch utc time in seconds
"""
__package__ = "srmparserlite.splFileManager"

from ..splGeneral.deco import VersionDeco
from ..splTraits import filefmt
from ..splGeneral.exceptions import NoFileToGenException
import multiprocessing.pool as mpo
import os.path
import glob
import re
import time
import datetime


@VersionDeco(1)
class ReadBigFile(object):
   """
   Thread safe
   """
   __slots__ = ["rootDir"]

   def __init__(this, a_rootDir):
      this.rootDir = a_rootDir

   def Read(this):
      with open(
            os.path.join(
               os.path.normpath(this.rootDir),
               filefmt.OneBigLogFileName())) as l_bfileObj:

               for l_line in l_bfileObj:
                  yield l_line


@VersionDeco(1)
class GenBigFile(object):
   """
   Generate one big log file
   """
   __slots__ = [
         "timeFlag"]

   def __init__(this, a_timeFlag):
      this.timeFlag = a_timeFlag  # 0 is always generate, 1 is 1 day

   def TmpScan(this, a_rootDir):
      print(a_rootDir)
      return (1, 2, 3)

   def TmpGen(this, (a, b, c)):
      print(a)
      print(b)
      print(c)

   def Start(this, *a_rootDirs):
      l_tpool = mpo.ThreadPool(processes=mpo.cpu_count())
      l_result = l_tpool.map_async(this.ScanDir, a_rootDirs, 1)
      l_result.get()

   def ScanDir(this, a_rootDir):
      """
      Passes in dir that want to scan
      """
      l_normRootDir = os.path.normpath(a_rootDir)
      l_gzFiles = []
      l_logFiles = []

      l_globIter = glob.iglob(
            os.path.join(
               l_normRootDir, "*.gz"))

      for gzfn in l_globIter:
         l_m = re.match(filefmt.SrmLogGzFileNameFormater(), os.path.basename(gzfn))
         if l_m is not None:
            l_gzFiles.append(gzfn)

      if l_gzFiles.__len__() == 0:
         l_gzFiles = None
      else:
         l_gzFiles.sort()

      l_globIter = glob.iglob(
         os.path.join(
            l_normRootDir, "*.log"))

      for logfn in l_globIter:
         l_m = re.match(filefmt.SrmLogFileNameFormater(), os.path.basename(logfn))
         if l_m is not None:
            l_logFiles.append(logfn)

      if l_logFiles.__len__() == 0:
         l_logFiles = None
      else:
         l_logFiles.sort()

      this.GenSingleFile(l_normRootDir, l_gzFiles, l_logFiles)

   def CheckBigFile(this, a_rootDir):
      """
      Return True is new file need to be generated , else no.
      """
      if this.timeFlag == 0 or this.timeFlag < 0:
         return True

      try:
         """
         Compare file time with current time against this.timeFlag
         """
         l_bigFileLocation = os.path.join(a_rootDir, filefmt.OneBigLogFileName())
         l_bigFileMTime = os.path.getmtime(l_bigFileLocation)
         l_currentTime = time.time()

         if datetime.timedelta(
            seconds=(l_currentTime - l_bigFileMTime)).days > this.timeFlag:
            return True
         else:
            return False
      except OSError:
         return True

   def GenSingleFile(this, a_rootDir, a_gzFiles, a_logFiles):
      if a_gzFiles is not None:

         if this.CheckBigFile(a_rootDir):
            import zipper
            l_unzipper = zipper.Unzipper()

            with open(os.path.join(a_rootDir, filefmt.OneBigLogFileName()), "w") as fh:

               for fn in a_gzFiles:
                  l_unzipper.Decompress(fn, fh)

      elif a_logFiles is not None:

         if this.CheckBigFile(a_rootDir):
            import logger
            l_logger = logger.ConcatLog()

            with open(os.path.join(a_rootDir, filefmt.OneBigLogFileName()), "w") as fh:

               for fn in a_logFiles:
                  l_logger.TakeFile(fn, fh)

      elif this.CheckBigFile(a_rootDir):
         raise NoFileToGenException()

__package__ = "srmparserlite.splFileManager"

from ..splGeneral.deco import VersionDeco
from ..splTraits import filefmt
import os
import glob
import re


@VersionDeco(1)
class GenResultFile(object):
   __slots__ = [
      "rootDir"]

   def __init__(this, a_rootDir):
      this.rootDir = os.path.normpath(a_rootDir)

   def genFileName(this):
      l_num = 1
      l_fileIter = glob.iglob(
         os.path.join(
            this.rootDir, "*.log"))

      for resultFn in l_fileIter:
         l_m = re.match(
            filefmt.ResultFileFormater().NUMFORMAT,
            os.path.basename(resultFn))
         if l_m is not None:
            if int(l_m.group("NUM")) >= l_num:
               l_num = int(l_m.group("NUM")) + 1

      l_repl = r"\1_" + str(l_num) + r"\2"
      l_newFileName = re.sub(
         filefmt.ResultFileFormater().REPLACEFORMAT,
         l_repl,
         filefmt.ResultFileFormater().FILENAME)
      return os.path.join(this.rootDir, l_newFileName)

r"""
TODO 1. use fm to read one big file
TODO 2. if no criteria input from user, parser will based on firstdir's onebig file's
   start time and use it as the filter requirement for the second dir.
TODO 3. need srmparserlite.splFilter component
TODO 4. write into splresult{nu}.log files

"""
__package__ = "srmparserlite.splParser"

import re
from ..splFileManager.fm import ReadBigFile
from ..splFileManager.filenamegen import GenResultFile
from ..splGeneral.exceptions import NoHeaderLineException
from ..splGeneral.exceptions import NoTraitException
from ..splTraits.traits import Traits
from ..splTraits.traits import LineClasses


class Parser(object):
   """
   thread safe
   read one large file and parse it base on filters
      read line into lineObj by line. use filter against each lineObj
   write original header into headerObj into result file
   """
   __slots__ = [
         "rootDir",
         "srmVersion",
         "srmLineClass",
         "trait"]

   def __init__(this, a_rootDir):
      import os
      this.rootDir = os.path.normpath(a_rootDir)

   def Start(this):
      this.Parsing(*this.GetVersion())

   def Parsing(this, a_header, a_bigFileIter):
      l_headlineObj = this.srmLineClass.HeadLineClass()
      l_m = re.match(this.trait.HEADERFMT, a_header)

      if l_m is not None:
         l_headlineObj.PROCESSEDFLAG = True
         l_headlineObj.PID = l_m.group("PID")
         l_headlineObj.VERSION = l_m.group("VERSION")
         l_headlineObj.BUILD = l_m.group("BUILD")
         l_headlineObj.OPTION = l_m.group("OPTION")
         print(l_headlineObj.PID)
         print(l_headlineObj.VERSION)
         print(l_headlineObj.BUILD)
         print(l_headlineObj.OPTION)

      else:
         raise NoHeaderLineException()

      print(GenResultFile(this.rootDir).genFileName())

      with open(GenResultFile(this.rootDir).genFileName(), "w") as l_resultFileObj:
         for ln in a_bigFileIter:
            l_lineObj = this.srmLineClass.LineClass()
            l_m = re.match(this.trait.LINEFMT, ln)
            if l_m is not None:

            l_resultFileObj.write(ln)

   def GetVersion(this):
      import importlib
      from ..splLineClass.general import VersionFmt

      l_ver = VersionFmt()
      l_rb = ReadBigFile(this.rootDir)
      l_iter = l_rb.Read()
      l_header = next(l_iter)
      l_m = re.match(l_ver.VERSIONFMT, l_header)
      if l_m is not None:
         this.srmVersion = "".join(l_m.group("VERSION").split("."))

         if this.srmVersion in Traits:
            try:
               l_traits = importlib.import_module(Traits[this.srmVersion], __package__)
               this.trait = l_traits.SrmTrait()
            except:
               raise NoTraitException()

         else:
            raise NoTraitException()

         if this.srmVersion in LineClasses:
            try:
               this.srmLineClass = importlib.import_module(
                  LineClasses[this.srmVersion],
                  __package__)
            except:
               raise NoTraitException()

         else:
            raise NoTraitException()

      else:
         raise NoHeaderLineException()

      return (l_header, l_iter)
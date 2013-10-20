r"""
DONE 1. use fm to read one big file
DONE 2. write into splresult_{nu}.log files
"""
__package__ = "srmparserlite.splParser"

from ..splGeneral.deco import VersionDeco
from ..splFileManager.fm import ReadBigFile
from ..splFileManager.filenamegen import GenResultFile
from ..splGeneral.exceptions import GenSrcLocation
from ..splGeneral.exceptions import NoHeaderLineException
from ..splGeneral.exceptions import NoTraitException
from ..splGeneral.exceptions import ConfigTimeErrorMsg
from ..splTraits import filefmt
from ..splTraits.traits import Traits
from ..splTraits.traits import LineClasses
from ..splFilter.filterr import TimeFilter
import re
import os.path
import multiprocessing.pool as mpo

SrcLoc = GenSrcLocation(__package__)


@VersionDeco(1)
class Parser(object):
   def __call__(this, a_site):
      DoParsing()(a_site)


@VersionDeco(1)
class DoParsing(object):
   def __call__(this, a_site):
   #l_siteCriterionTuple = [(a_site, l_criterion) for l_criterion in a_site["criteria"]]
      a_site["dir"] = os.path.normpath(a_site["dir"])

      l_siteCriterionTuple = tuple(
         (a_site, l_criterion) for l_criterion in a_site["criteria"])

      l_tpool = mpo.ThreadPool(processes=mpo.cpu_count())
      l_result = l_tpool.map_async(this.ParseCriterion, l_siteCriterionTuple, 2)
      l_result.get()

   def ParseCriterion(this, a_siteCriterion):
      ParsingCriterion()(a_siteCriterion)


@VersionDeco(1)
class ParsingCriterion(object):
   """
   thread safe , an object per criterion
   read one large file and parse it base on filters
      read line into lineObj by line. use filter against each lineObj
   write original header into headerObj into result file
   """
   __slots__ = [
         "siteCriterion",
         "srmVersion",
         "srmLineClass",
         "trait"]

   def __call__(this, a_siteCriterion):
      this.siteCriterion = a_siteCriterion
      this.Parsing(this.siteCriterion[1], *this.GetVersion())

   def TestLine(this, a_criteria, a_ln):

      l_m = re.match(this.trait.LINEFMT, a_ln)
      if l_m is not None:
         l_delayLine.line = ln

         if l_delayLine.found:
            l_resultFileObj.write(l_delayLine.__str__())
            l_delayLine.found = False
            if l_delayLine.bundle.__len__() != 0:
               del l_delayLine.bundle[0:len(l_delayLine.bundle)]
         """
         l_lineObj = this.srmLineClass.LineClass()
         l_lineObj.TIME = l_m.group("TIME")
         l_lineObj.INFO = l_m.group("INFO")
         l_lineObj.TYPE = l_m.group("TYPE")
         l_lineObj.DATA = l_m.group("DATA")
         """

         """
         Apply filter. If match, save the line, else pass
         """

         if not l_startTimeFilter.ApplyLess(l_m.group("TIME")):
            continue
         elif not l_endTimeFilter.ApplyLess(l_m.group("TIME")):
            """
            filter here!
            could use only one flag bit but it's obscure.... it's python, not c++
            :-)
            """
            l_foundFlag = False
            l_localFlag = False

            if a_criteria["info"].__len__() == 0:
               l_localFlag = True

            else:
               l_localFlag = False

            for l_info in a_criteria["info"]:

               if l_localFlag:
                  break

               for l_infoc in l_info:

                  if re.search(l_infoc, l_m.group("INFO"), re.I) is not None:
                     l_localFlag = True
                     break

            l_foundFlag = l_localFlag

            print("ha")
            print(ln)
            if l_foundFlag:

               if l_m.group("TYPE") is None or a_criteria["type"].__len__() == 0:
                  l_localFlag = True

               else:
                  l_localFlag = False

               for l_type in a_criteria["type"]:

                  if l_localFlag:
                     break

                  for l_typec in l_type:

                     if re.search(l_typec, l_m.group("TYPE"), re.I) is not None:
                        l_localFlag = True
                        break

               l_foundFlag = l_localFlag

            if l_foundFlag:

               if a_criteria["data"].__len__() == 0:
                  l_localFlag = True

               else:
                  l_localFlag = False

               for l_data in a_criteria["data"]:

                  if l_localFlag:
                     break

                  for l_datac in l_data:

                     if re.search(l_datac, l_m.group("DATA"), re.I) is not None:
                        l_localFlag = True
                        break

               l_foundFlag = l_localFlag

            print("in filter area")
            if l_foundFlag:
               print("ha2")
               print(ln)

               l_delayLine.found = True
               continue
         else:
            l_outOfScope = True
            continue

   def Parsing(this, a_criteria, a_header, a_bigFileIter):
      """
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
         raise NoHeaderLineException(
            SrcLoc.__str__(),
            os.path.join(this.siteCriterion[0]["dir"], filefmt.OneBigLogFileName()))
      """
      """
      Reason that use lineobj to save it first rather filter each line directly
      and write any line that passes filter is that
      later on, we want to save lineobj into database
      """

      l_unsupportFileName = GenResultFile(this.siteCriterion[0]["dir"]).genFileName(
               a_criteria["logfilename"] + "_UnsupportFormat")
      l_unsupportFileObj = None

      with open(GenResultFile(this.siteCriterion[0]["dir"]).genFileName(
         a_criteria["logfilename"]), "w") as l_resultFileObj:

         l_resultFileObj.write(a_header)

         l_outOfScope = False
         l_delayLine = this.srmLineClass.LiteLineClass()

         for ln in a_bigFileIter:

            if l_outOfScope:
               break


            elif a_criteria["bundle"].__len__() != 0:

               l_m = re.match(this.trait.BUNDLEFMT, ln)

               if l_m is not None:
                  """
                  apply filter, if match, save, else , skip
                  """
                  print("ha4")
                  print(l_delayLine)
                  print(ln)
                  l_foundFlag = False
                  l_localFlag = False

                  if l_delayLine.found:

                     for l_bundle in a_criteria["bundle"]:
                        if l_localFlag:
                           break
                        for l_bundlec in l_bundle:
                           if re.search(l_bundlec, ln, re.I) is not None:
                              l_localFlag = True
                              break

                     l_foundFlag = l_localFlag
                     if l_foundFlag:
                        l_delayLine.bundle.append(ln)
                        continue
                     else:
                        l_delayLine.found = False
                        continue
                  elif l_delayLine.line == "":

                     for l_bundle in a_criteria["bundle"]:
                        if l_localFlag:
                           break
                        for l_bundlec in l_bundle:
                           if re.search(l_bundlec, ln, re.I) is not None:
                              l_localFlag = True
                              break

                     l_foundFlag = l_localFlag
                     if l_foundFlag:
                        l_delayLine.bundle.append(ln)
                        l_delayLine.found = True
                        continue

               else:
                  # flush previous found l_delayLine
                  if l_delayLine.found:
                     l_resultFileObj.write(l_delayLine.__str__())
                     l_delayLine.found = False

                  if l_unsupportFileObj is not None:
                     l_unsupportFileObj.write(ln)
                  else:
                     l_unsupportFileObj = open(l_unsupportFileName, "a+")
                     l_unsupportFileObj.write(ln)
                  #raise UnSupportFormatException(ln)

         if l_delayLine is not None and l_delayLine.found is True:
            l_resultFileObj.write(l_delayLine.__str__())

      if l_unsupportFileObj is not None:
         l_unsupportFileObj.close()

   def GetVersion(this):
      import importlib
      from ..splTraits.general import VersionFmt

      l_ver = VersionFmt()
      l_rb = ReadBigFile(this.siteCriterion[0]["dir"])
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
               raise NoTraitException(SrcLoc.__str__(), this.srmVersion)

         else:
            raise NoTraitException(SrcLoc.__str__(), this.srmVersion)

         if this.srmVersion in LineClasses:
            try:
               this.srmLineClass = importlib.import_module(
                  LineClasses[this.srmVersion],
                  __package__)
            except:
               raise NoTraitException(SrcLoc.__str__(), this.srmVersion)

         else:
            raise NoTraitException(SrcLoc.__str__(), this.srmVersion)

      else:
         raise NoHeaderLineException(
            SrcLoc.__str__(),
            os.path.join(this.siteCriterion[0]["dir"], filefmt.OneBigLogFileName()))

      return (l_header, l_iter)

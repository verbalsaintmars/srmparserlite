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
      l_startTimeFilter = TimeFilter(
            this.srmVersion,
            # strip will be removed , let reader handle this
            a_criteria["time"]["start"].strip(),
            a_criteria["time"]["flag"].strip())

      if not l_startTimeFilter.ApplyLess(a_criteria["time"]["end"].strip()):
         print(ConfigTimeErrorMsg(
            this.siteCriterion[0]["name"],
            a_criteria["name"],
            a_criteria["time"]["start"],
            a_criteria["time"]["end"]))
         return

      l_endTimeFilter = TimeFilter(
            this.srmVersion,
            a_criteria["time"]["end"].strip(),
            a_criteria["time"]["flag"].strip())

      l_unsupportFileName = GenResultFile(this.siteCriterion[0]["dir"]).genFileName(
               a_criteria["logfilename"] + "_UnsupportFormat")

      with open(GenResultFile(this.siteCriterion[0]["dir"]).genFileName(
         a_criteria["logfilename"]), "w") as l_resultFileObj:

         l_resultFileObj.write(a_header)
         l_delayLine = None
         l_outOfScope = False

         for ln in a_bigFileIter:
            print("testing")
            print(ln)
            print(l_outOfScope)
            if l_outOfScope:
               break
            l_m = re.match(this.trait.LINEFMT, ln)
            if l_m is not None:
               if l_delayLine is not None and l_delayLine.found is True:
                  l_resultFileObj.write(l_delayLine.__str__())
                  l_delayLine.found = False
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
                  """
                  print("in filter area")
                  print(ln)
                  l_delayLine = this.srmLineClass.LiteLineClass()
                  l_delayLine.line = ln
                  if l_delayLine.bundle.__len__ != 0:
                     del l_delayLine.bundle[0:len(l_delayLine.bundle)]
                  l_delayLine.found = True
                  continue
               else:
                  l_outOfScope = True
                  continue

            else:
               l_m = re.match(this.trait.BUNDLEFMT, ln)

               if l_m is not None:
                  """
                  apply filter, if match, save, else , skip
                  """
                  if False:  # test criteria true or false
                     if l_delayLine is None:
                        l_delayLine = this.srmLineClass.LiteLineClass()

                     l_delayLine.bundle.append(ln)
                     l_delayLine.found = True

                  elif l_delayLine.found is True:
                     l_delayLine.bundle.append(ln)

                  elif l_delayLine.bundle.__len__ != 0:
                     l_resultFileObj.write(ln)

               else:
                  # flush previous found l_delayLine
                  if l_delayLine.found:
                     l_resultFileObj.write(l_delayLine.__str__())
                     l_delayLine.found = False

                  with open(l_unsupportFileName, "a+") as l_unsupportFileObj:
                     l_unsupportFileObj.write(ln)
                  #raise UnSupportFormatException(ln)

         if l_delayLine is not None and l_delayLine.found is True:
            l_resultFileObj.write(l_delayLine.__str__())

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

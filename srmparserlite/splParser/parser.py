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
      """
      a_site =>
      Site1 = {
         "name": "Site_1",
         "dir": r"/myfiles/Source/vsProject/srmparserlite/pplog/",
         "criteria": (site1pack11,),
         "type": "config",  # ignore other parameter. gen same
         splsync_{nu}.log on each site
         "dayoffset": 1}
      """
      a_site["dir"] = os.path.normpath(a_site["dir"])

      l_siteCriterionTuple = tuple(
         (a_site, l_criterion) for l_criterion in a_site["criteria"])

      l_tpool = mpo.ThreadPool(processes=mpo.cpu_count())
      """
      l_siteCriterionTuple => ((a_site, site1pack11),(a_site, site1pack12))
      """
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

   def TestLineKind(this, a_m, a_ln, a_kind):
      l_criterion = this.siteCriterion[1]
      l_singleFlag = False

      #(type1, type2) is OR
      #type1's ("PCM", "XXXX") is AND
      for l_kind in l_criterion[a_kind]:
         if l_singleFlag:
            break
         for l_kindc in l_kind:
            if re.search(l_kindc, a_m.group(a_kind.upper()), re.I) is None:
               l_singleFlag = False
               break
            else:
               l_singleFlag = True

      return l_singleFlag

   def TestBundle(this, a_m, a_ln):
      l_criterion = this.siteCriterion[1]
      l_found = False

      if l_criterion["bundle"].__len__() == 0:
         l_found = True
      else:
         l_found = this.TestLineKind(a_m, a_ln, "bundle")

      return l_found

   def TestLine(this, a_m, a_ln):
      l_criterion = this.siteCriterion[1]

      l_found = False

      # Test info criteria
      if l_criterion["info"].__len__() == 0:
         l_found = True
      else:
         l_found = this.TestLineKind(a_m, a_ln, "info")

      if l_found:
         if l_criterion["type"].__len__() == 0:
            l_found = True
         elif a_m.group("TYPE") is None:
            l_found = False
         else:
            l_found = this.TestLineKind(a_m, a_ln, "type")

      if l_found:
         if l_criterion["data"].__len__() == 0:
            l_found = True
         else:
            l_found = this.TestLineKind(a_m, a_ln, "data")

      return l_found

   def Parsing(this, a_criteria, a_header, a_bigFileIter):

      l_startTimeFilter = TimeFilter(
         this.srmVersion,
         # strip will be removed , let reader handle this
         a_criteria["time"]["start"].strip(),
         a_criteria["time"]["flag"].strip())

      l_endTimeFilter = TimeFilter(
           this.srmVersion,
           a_criteria["time"]["end"].strip(),
           a_criteria["time"]["flag"].strip())

      l_unsupportFileName = GenResultFile(this.siteCriterion[0]["dir"]).genFileName(
               a_criteria["logfilename"] + "_UnsupportFormat")
      l_unsupportFileObj = None

      with open(GenResultFile(this.siteCriterion[0]["dir"]).genFileName(
         a_criteria["logfilename"]), "w") as l_resultFileObj:

         l_resultFileObj.write(a_header)

         l_delayLine = this.srmLineClass.LiteLineClass()

         for ln in a_bigFileIter:

            l_m = re.match(this.trait.LINEFMT, ln)

            if l_m is not None:

               if l_delayLine.found:
                  if l_delayLine.bundle.__len__() == 0 and \
                     a_criteria["bundle"].__len__() == 0:
                     l_resultFileObj.write(l_delayLine.__str__())
                  elif l_delayLine.bundleFlag:
                     l_resultFileObj.write(l_delayLine.__str__())

                  del l_delayLine.bundle[:]
                  l_delayLine.found = False
                  l_delayLine.bundleFlag = False

               if not l_startTimeFilter.ApplyLessEq(l_m.group("TIME")):
                  l_delayLine.line = "default"
                  continue
               elif not l_endTimeFilter.ApplyLessEq(l_m.group("TIME")):
                  if this.TestLine(l_m, ln):
                     l_delayLine.line = ln
                     l_delayLine.found = True
                  continue
               else:
                  break

            l_m = re.match(this.trait.BUNDLEFMT, ln)
            if l_m is not None:
               if l_delayLine.found:
                  if this.TestBundle(l_m, ln):
                     l_delayLine.bundleFlag = True

                  l_delayLine.bundle.append(ln)

               elif l_delayLine.line == "":
                  if this.TestBundle(l_m, ln):
                     l_delayLine.bundle.append(ln)
                     l_delayLine.bundleFlag = True
                     l_delayLine.found = True

            else:
               if l_unsupportFileObj is not None:
                  l_unsupportFileObj.write(ln)
               else:
                  l_unsupportFileObj = open(l_unsupportFileName, "a+")
                  l_unsupportFileObj.write(ln)

         if l_delayLine.found:
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

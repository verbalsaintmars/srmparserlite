r"""
DONE: Take logfilename and onelargefile file handle
"""
__package__ = "srmparserlite.splFileManager"

from ..splGeneral.deco import VersionDeco
from ..splGeneral.exceptions import NoHeaderLineException
from ..splGeneral.exceptions import NoTraitException
from ..splGeneral.exceptions import GenSrcLocation
from ..splTraits.traits import Traits
import re

SrcLoc = GenSrcLocation(__package__)


@VersionDeco(1)
class ConcatLog(object):
   __slots__ = [
         "singleFileObj",
         "numOfFiles",
         "srmTrait"]

   def __init__(this):
      this.singleFileObj = None
      this.numOfFiles = 0
      this.srmTrait = None

   def WriteSingleFile(this, a_fileObj):
      from ..splTraits.general import GeneralFmt
      from os import SEEK_END
      import importlib
      if this.numOfFiles == 1:
         l_headLine = a_fileObj.readline()
         l_verp = GeneralFmt()
         l_m = re.match(l_verp.VERSIONFMT, l_headLine)

         if l_m is not None:
            #print("Head line for parsing version : " + l_m.string)
            #print("Version : " + l_m.group("VERSION"))
            l_logversion = "".join(l_m.group("VERSION").split("."))
            #print("Version_Concat : " + l_logversion)
            if l_logversion in Traits:
               l_traits = importlib.import_module(Traits[l_logversion], __package__)
               this.srmTrait = l_traits.SrmTrait()
               #print("this.srmTrait offset : " + str(this.srmTrait.TRAILOFFSET))
               this.singleFileObj.write(l_headLine)
               this.singleFileObj.writelines(a_fileObj.readlines())
               this.singleFileObj.seek(-this.srmTrait.TRAILOFFSET, SEEK_END)

            else:
               raise NoTraitException(SrcLoc.__str__(), l_logversion)

         else:
            raise NoHeaderLineException(SrcLoc.__str__(), a_fileObj.name)

      else:
         #print("Appened gz files : " + a_fileObj.name)
         if this.srmTrait is None:
            this.numOfFiles = 1
            l_headLine = a_fileObj.readline()
            l_verp = GeneralFmt()
            l_m = re.match(l_verp.VERSIONFMT, l_headLine)

            if l_m is not None:
               #print("Head line for parsing version : " + l_m.string)
               #print("Version : " + l_m.group("VERSION"))
               l_logversion = "".join(l_m.group("VERSION").split("."))
               #print("Version_Concat : " + l_logversion)
               if l_logversion in Traits:
                  l_traits = importlib.import_module(Traits[l_logversion], __package__)
                  this.srmTrait = l_traits.SrmTrait()
                  #print("this.srmTrait offset : " + str(this.srmTrait.TRAILOFFSET))
                  this.singleFileObj.write(l_headLine)
                  this.singleFileObj.writelines(a_fileObj.readlines())
                  this.singleFileObj.seek(-this.srmTrait.TRAILOFFSET, SEEK_END)

               else:
                  raise NoTraitException(SrcLoc.__str__(), l_logversion)

            else:
               raise NoHeaderLineException(SrcLoc.__str__(), a_fileObj.name)

         else:
            a_fileObj.readline()
            this.singleFileObj.writelines(a_fileObj.readlines())
            this.singleFileObj.seek(-this.srmTrait.TRAILOFFSET, SEEK_END)

   def TakeFile(this, a_fileName, a_sfileObj):
      #print("TakeFile: a_fileName : " + a_fileName)
      with open(a_fileName) as l_fileObj:
         if a_sfileObj is this.singleFileObj:
            #print("Same single file hd")
            this.numOfFiles += 1

         else:
            this.singleFileObj = a_sfileObj
            #print("Different single file hd")
            this.numOfFiles = 1

         try:
            this.WriteSingleFile(l_fileObj)
         except (NoTraitException, NoHeaderLineException) as ex:
            print(ex.message)
            return False
         else:
            return True

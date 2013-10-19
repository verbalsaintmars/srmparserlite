r"""
DONE 1. read files in dir/sorted
DONE 2. intrusive test file name inside if match format "vmware-dr-4245.log"
DONE 3. If there is _a_ match in file format, unzip the whole gz file
DONE 4. zip file with input filename / test it / delete original file
"""
__package__ = "srmparserlite.splFileManager"

from ..splGeneral.deco import VersionDeco
from ..splGeneral.exceptions import NoHeaderLineException
from ..splGeneral.exceptions import NoTraitException
from ..splGeneral.exceptions import NotGzFileFormat
from ..splGeneral.exceptions import GenSrcLocation
from ..splTraits.traits import Traits
import re

SrcLoc = GenSrcLocation(__package__)


@VersionDeco(1)
class GzipHandler(object):

   def __init__(this, a_formater):
      this.formater = a_formater  # formater for files inside the gz file
      this.singleFileObj = None
      this.numOfFiles = 0
      this.srmTrait = None

   def WriteSingleFile(this, a_gzipFileObj):
      from ..splTraits.general import VersionFmt
      from os import SEEK_END
      import importlib
      if this.numOfFiles == 1:
         l_headLine = a_gzipFileObj.readline()
         l_verp = VersionFmt()
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
               this.singleFileObj.writelines(a_gzipFileObj.readlines())
               this.singleFileObj.seek(-this.srmTrait.TRAILOFFSET, SEEK_END)

            else:
               raise NoTraitException(SrcLoc.__str__(), l_logversion)

         else:
            raise NoHeaderLineException(SrcLoc.__str__(), a_gzipFileObj.name)

      else:
         if this.srmTrait is None:
            this.numOfFiles = 1
            l_headLine = a_gzipFileObj.readline()
            l_verp = VersionFmt()
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
                  this.singleFileObj.writelines(a_gzipFileObj.readlines())
                  this.singleFileObj.seek(-this.srmTrait.TRAILOFFSET, SEEK_END)

               else:
                  raise NoTraitException(SrcLoc.__str__(), l_logversion)

            else:
               raise NoHeaderLineException(SrcLoc.__str__(), a_gzipFileObj.name)

         else:
            #print("Appened gz files : " + a_gzipFileObj.name)
            a_gzipFileObj.readline()
            this.singleFileObj.writelines(a_gzipFileObj.readlines())
            this.singleFileObj.seek(-this.srmTrait.TRAILOFFSET, SEEK_END)

   def TakeFile(this, a_fileName, a_sfileObj):
      import gzip
      l_unzipFlag = False
      #print("GzipHandler:TakeFile: a_fileName : " + a_fileName)
      with gzip.open(a_fileName) as l_fileObj:
         l_fileNames = []  # files inside a gz file
         l_tmpfn = ''

         try:
            l_tmpfn = GzipHandler.GetContentFileNames(l_fileObj.fileobj)
         except NotGzFileFormat as ioe:
            print(ioe.message)
            return False

         l_fileNames.append(l_tmpfn)
         #print(l_fileNames)
         #print("formater : " + this.formater)

         l_match = None
         for fn in l_fileNames:
            #print("fn : " + fn)
            l_match = re.match(this.formater, fn)
            if l_match is not None:
               #print("filename : " + fn + "is valid.")
               l_unzipFlag = True
               break

         if l_unzipFlag:

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

         else:
            return False

   def GetContentFileNames(a_fileObj):
      """
      Return File names inside the gz file
      """
      import struct

      from gzip import FEXTRA, FNAME
      a_fileObj.seek(0)
      magic = a_fileObj.read(2)
      if magic != '\037\213':
        raise NotGzFileFormat(SrcLoc.__str__(), a_fileObj.name)

      method, flag, mtime = struct.unpack("<BBIxx", a_fileObj.read(8))

      if not flag & FNAME:
        # Not stored in the header, use the filename sans .gz
        fname = a_fileObj.name
        if fname.endswith('.gz'):
            fname = fname[:-3]
        return fname

      if flag & FEXTRA:
        # Read & discard the extra field, if present
        a_fileObj.read(struct.unpack("<H", a_fileObj.read(2)))

      # Read a null-terminated string containing the filename
      fname = []

      while True:
        s = a_fileObj.read(1)
        if not s or s == '\000':
            break
        fname.append(s)
      a_fileObj.seek(0)
      return ''.join(fname)

   GetContentFileNames = staticmethod(GetContentFileNames)


from ..splTraits.filefmt import SrmLogFileNameFormater


@VersionDeco(1)
class Unzipper(object):
   def __init__(this):
      this.handler = GzipHandler(SrmLogFileNameFormater())

   def Decompress(this, a_file, a_sfileObj):
      """
      Decompress file passed in and write to passed in file object
      """
      return this.handler.TakeFile(a_file, a_sfileObj)

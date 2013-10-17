import srmparserlite.splFileManager.zipper as zipper
import srmparserlite.splFileManager.fm as filemanager
import srmparserlite.splFileManager.filenamegen as genfile
import srmparserlite.splParser.parser as parser


def TestUnzipFunc():
   unzipper = zipper.Unzipper
   v_files = [
         "vmware-dr-4245.log.gz",
         "vmware-dr-4246.log.gz",
         "vmware-dr-4247.log.gz"]
   fh = open("BigLog.log", "w")
   uz = unzipper()
   for fn in v_files:
      uz.Decompress(fn, fh)


def TestFilemanager():
   fm = filemanager.GenBigFile(0)  # number of days
   dirs = (r"/myfiles/Source/vsProject/srmparserlite/pplog/",
           r"/myfiles/Source/vsProject/srmparserlite/sslog",
           r"/myfiles/Source/vsProject/srmparserlite/vvvog")

   fm.Start(*dirs)


def TestReadBigFile():
   rb = filemanager.ReadBigFile(r"/myfiles/Source/vsProject/srmparserlite/pplog")
   for fl in rb.Read():
      print(fl)


def TestGenFile():
   genf = genfile.GenResultFile(r"/myfiles/Source/vsProject/srmparserlite/pplog")
   print(genf.genFileName())


def TestSplParser():
   dirRoot = [
         r"/myfiles/Source/vsProject/srmparserlite/pplog",
         r"/myfiles/Source/vsProject/srmparserlite/sslog"]
   pa1 = parser.Parser(r"/myfiles/Source/vsProject/srmparserlite/sslog")
   pa2 = parser.Parser(r"/myfiles/Source/vsProject/srmparserlite/pplog")
   pa1.Start()
   pa2.Start()


if __name__ == '__main__':  # Only when run
   #TestUnzipFunc()
   TestFilemanager()
   #TestReadBigFile()
   #TestSplParser()
   #TestGenFile()

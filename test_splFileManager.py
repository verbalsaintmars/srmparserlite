import srmparserlite.splFileManager.zipper as zipper
import srmparserlite.splFileManager.fm as filemanager
import srmparserlite.splFileManager.filenamegen as genfile
import srmparserlite.splParser.parser as parser
import srmparserlite.splFilter.filterr as filterr
import srmparserlite.splGeneral.exceptions as ex


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


def TestGenBigFile():
   fm = filemanager.GenBigFile()  # number of days

   dirs = ((r"/myfiles/Source/vsProject/srmparserlite/vvlog/", 0),
           (r"/myfiles/Source/vsProject/srmparserlite/sslog", 1),
           (r"/myfiles/Source/vsProject/srmparserlite/pplog/", 0))

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


def TestSplFilter():
   ft = filterr.TimeFilter("501", r"2014-07-05T14:26:15.182-08:00", "year")
   print(ft.ApplyLess(r"2014-08-06T15:27:16.183-08:00"))


def TestSpl():
   import srmparserlite.spl as spl
   import srmparserlite.splConfig.fakeconfig as fakeconfig
   singleSite = fakeconfig.singleSite
   #doubleSite = fakeconfig.doubleSite
   sp = spl.Start()
   sp.Start(singleSite)

if __name__ == '__main__':  # Only when run
   #TestUnzipFunc()
   #TestGenBigFile()
   #TestReadBigFile()
   #TestSplParser()
   #TestGenFile()
   #TestSplFilter()
   TestSpl()

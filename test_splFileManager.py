import srmparserlite.splFileManager.zipper as zipper
import srmparserlite.splFileManager.fm as filemanager


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
   fm = filemanager.FileManager()
   fm.ScanDir(r"/myfiles/Source/vsProject/srmparserlite/pplog/", r"/myfiles/Source/vsProject/srmparserlite/sslog/")
   fm.GenSingleFile()

if __name__ == '__main__':  # Only when run
   #TestUnzipFunc()
   TestFilemanager()

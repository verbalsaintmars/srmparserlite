def VersionDeco(a_version):
   def TrueDeco(a_class):
      a_class.__version__ = a_version
      return a_class
   return TrueDeco

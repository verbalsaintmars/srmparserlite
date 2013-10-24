__package__ = "srmparserlite.splConfig"
from ..splGeneral.deco import VersionDeco


@VersionDeco(1)
class PrepareConfig(object):
   __slots__ = ["sites", "syncState", "syncTime"]

   def __init__(this, a_sites):
      this.sites = a_sites
      this.syncTime = []
      this.syncState = False

   def CheckZeroCriteria(this):
      this.sites[:] = \
         [l_site for l_site in this.sites if l_site["criteria"].__len__() != 0]

   def CheckModifyState(this):
      v_tmpConfig = None

      for l_site in this.sites:
         if l_site["type"] == "sync":
            if this.syncState is False:
               for l_criteria in l_site["criteria"]:
                  this.syncTime.append(l_criteria["time"])

               this.syncState = True
               v_tmpConfig = l_site
               break

      if this.syncState is True:

         for l_site in this.sites:
            if l_site is v_tmpConfig:
               continue
            i = 0
            for l_criteria in l_site["criteria"]:
               try:
                  l_criteria["time"] = this.syncTime[i]
                  i += 1
               except IndexError:
                  break

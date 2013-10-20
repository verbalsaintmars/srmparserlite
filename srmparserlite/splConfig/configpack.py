__package__ = "srmparserlite.splConfig"
from ..splGeneral.deco import VersionDeco
import fakeconfig

r"""
TODO: 1. config file name format : *.spl
TODO: 2. give director will scan for .spl files
TODO: 3. with given log dirs, will run spl against each .spl config files
TODO: 4. generate *_spl.log result. if *_spl.log result exist, skip. If force, will
   overwrite the existing *_spl.log files
"""

#def TestOutScope(this, a_criteria, a_ln):
#  l_startTimeFilter = TimeFilter(
#        this.srmVersion,
#        # strip will be removed , let reader handle this
#        a_criteria["time"]["start"].strip(),
#        a_criteria["time"]["flag"].strip())
#
#  if not l_startTimeFilter.ApplyLess(a_criteria["time"]["end"].strip()):
#     print(ConfigTimeErrorMsg(
#        this.siteCriterion[0]["name"],
#        a_criteria["name"],
#        a_criteria["time"]["start"],
#        a_criteria["time"]["end"]))
#     return
#
#  l_endTimeFilter = TimeFilter(
#        this.srmVersion,
#        a_criteria["time"]["end"].strip(),
#        a_criteria["time"]["flag"].strip())

class PrepareConfig(object):
   __slots__ = ["sites", "syncState", "syncTime"]

   def __init__(this, a_sites):
      this.sites = a_sites
      this.syncTime = []
      this.syncState = False

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


@VersionDeco(1)
class ConfigReader(object):
   pass

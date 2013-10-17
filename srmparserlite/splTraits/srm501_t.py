__package__ = "srmparserlite.splTraits"
from ..splGeneral.deco import VersionDeco
import srm500_t


@VersionDeco(501)  # Have class variable ClassVersion
class SrmTrait(srm500_t.SrmTrait):
   __slots__ = ["trailOffSet"]

   def __init__(this):
      super(SrmTrait, this).__init__()
      this.trailOffSet = "Writer rotated...".__len__() + 1  # + 1 as for \n

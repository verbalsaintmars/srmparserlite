__package__ = "srmparserlite.splTraits"
from ..splGeneral.deco import VersionDeco
import srm500_t


@VersionDeco(503)  # Have class variable ClassVersion
class SrmTrait(srm500_t.SrmTrait):
   pass

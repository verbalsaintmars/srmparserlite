__package__ = "srmparserlite.splLineClass"

from ..splGeneral.deco import VersionDeco
import srm500


@VersionDeco(503)
class HeadLineClass(srm500.HeadLineClass):
   pass


@VersionDeco(503)
class LineClass(srm500.LineClass):
   pass

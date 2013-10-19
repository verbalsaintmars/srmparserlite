__package__ = "srmparserlite.splLineClass"

from ..splGeneral.deco import VersionDeco
import srm500


@VersionDeco(501)
class HeadLineClass(srm500.HeadLineClass):
   pass


@VersionDeco(501)
class LineClass(srm500.LineClass):
   pass


@VersionDeco(501)
class LiteLineClass(srm500.LiteLineClass):
   pass

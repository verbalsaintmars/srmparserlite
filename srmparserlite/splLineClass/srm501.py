__package__ = "srmLogParserLite.splLineClass"
from ..splGeneral.deco import VersionDeco
import srm500


@VersionDeco(501)
class HeadLineClass(srm500.HeadLineClass):
   pass


@VersionDeco(501)
class LineClass(srm500.LineClass):
   pass

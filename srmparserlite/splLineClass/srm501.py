if __name__ == "__main__" and __package__ is None:
   __package__ = "srmLogParserLite.splLineClass"

from ..splGeneral.deco import VersionDeco
import srm500


@VersionDeco(501)
class HeadLineClass(srm500.HeadLineClass):
   pass


@VersionDeco(501)
class LineClass(srm500.LineClass):
   pass


def tester():
   pass

if __name__ == '__main__':  # Only when run
   tester()

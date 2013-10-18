__package__ = "srmparserlite.splConfig"
from ..splGeneral.deco import VersionDeco
r"""
TODO: 1. config file name format : *.spl
TODO: 2. give director will scan for .spl files
TODO: 3. with given log dirs, will run spl against each .spl config files
TODO: 4. generate *_spl.log result. if *_spl.log result exist, skip. If force, will
   overwrite the existing *_spl.log files
"""


@VersionDeco(1)
class ConfigReader(object):
   pass

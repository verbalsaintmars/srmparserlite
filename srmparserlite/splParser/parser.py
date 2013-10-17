
r"""
TODO 1. use fm to read one big file
TODO 2. if no criteria input from user, parser will based on firstdir's onebig file's
   start time and use it as the filter requirement for the second dir.
TODO 3. need srmparserlite.splFilter component
TODO 4. write into splresult{nu}.log files

"""
__package__ = "srmparserlite.splGeneral"

from ..splLineClass.srm500


class Parser(object):
   """
   thread safe
   read one large file and parse it base on filters
      read line into lineObj by line. use filter against each lineObj
   write original header into headerObj into result file
   """
   __slots__ = []

   def __init__(this):
      pass

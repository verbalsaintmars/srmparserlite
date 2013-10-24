__package__ = "srmparserlite.splConfig"
from ..splGeneral.deco import VersionDeco
from ..splFilter.filterr import TimeFilter
from ..splGeneral.exceptions import ConfigTimeErrorMsg
from ..splGeneral.exceptions import LoadYamlFileErrorMsg
from .. splTraits.general import GeneralFmt
import os
import re


def ValidateTimeFormat(a_value):
   if re.match(GeneralFmt().TIMEFMT, a_value) is not None:
      return True
   else:
      return False


def ValidateTimeFlag(a_value):
   if a_value != 'milli' and a_value != 'sec' and a_value != 'min' and \
         a_value != 'hour' and a_value != 'day' and a_value != 'month' and \
         a_value != 'year':
            return False
   else:
      return True


def ValidateIsString(a_value):
   try:
      a_value += 0
      return False
   except:
      return True


def ValidateIsNumber(a_value):
   try:
      a_value += 0
      return True
   except:
      return False


def ValidateNotEmptyString(a_value):
   if a_value == '':
      return False
   else:
      return True


def ValidateSiteType(a_value):
   if a_value != 'config' and a_value != 'sync':
      return False
   else:
      return True


def ValidateSiteDir(a_value):
   if os.path.isdir(a_value):
      return True
   else:
      return False

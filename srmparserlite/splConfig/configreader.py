__package__ = "srmparserlite.splConfig"
from ..splGeneral.deco import VersionDeco
from ..splFilter.filterr import TimeFilter
from ..splGeneral.exceptions import ConfigTimeErrorMsg
from ..splGeneral.exceptions import LoadYamlFileErrorMsg
from ..splGeneral.exceptions import ConfigTimeFormatErrorMsg


@VersionDeco(1)
class SplList(object):
   """
   a tuple of strings
   """
   __slots__ = ["lists"]

   def __init__(this):
      this.lists = []

   def addList(this, a_str):
      this.lists.append(a_str)

   def getTuple(this):
      return tuple(this.lists)


@VersionDeco(1)
class SplTime(object):
   __slots__ = [
         "timeMap",
         "start",
         "end",
         "flag"]

   def __init__(this, a_start, a_end, a_flag):
      this.start = a_start
      this.end = a_end
      this.flag = a_flag

   def genTime(this):
      this.timeMap = {
            "start": this.start,
            "end": this.end,
            "flag": this.flag}
      return this.timeMap


@VersionDeco(1)
class SplCriteria(object):
   __slots__ = [
         "criMap",
         "name",  # string
         "theTime",  # SplTime type gened map
         "info",  # SplInfo type gened map
         "theType",  # SplType type gened map
         "theData",  # SplData type gened map
         "bundle",  # SplBundle type gened map
         "logFileName"]  # string

   def __init__(this, a_name, a_time, a_info, a_type, a_data, a_bundle, a_lfn):
      this.name = a_name
      this.theTime = a_time
      this.info = a_info
      this.theType = a_type
      this.theData = a_data
      this.bundle = a_bundle
      this.logFileName = a_lfn

   def genCri(this):
      if this.theTime is False:
         return False
      else:
         this.criMap = {
               "name": this.name,
               "time": this.theTime,
               "info": this.info,
               "type": this.theType,
               "data": this.theData,
               "bundle": this.bundle,
               "logfilename": this.logFileName}
         return this.criMap


@VersionDeco(1)
class SplSite(object):
   __slots__ = [
         "siteMap",
         "name",
         "directory",
         "criteria",  # SplCriteria type gened map
         "theType",
         "dayoffset"]

   def __init__(this, a_name, a_dir, a_cri, a_type, a_dos):
      this.name = a_name
      this.directory = a_dir
      this.criteria = a_cri  # a list
      this.theType = a_type
      this.dayoffset = a_dos

   def genSite(this):
      """
      Return False if config error found for site.
      else return site dict object
      """
      this.siteMap = {
            "name": this.name,
            "dir": this.directory,
            "criteria": this.criteria,
            "type": this.theType,
            "dayoffset": this.dayoffset}
      return this.siteMap


from .validator import ValidateIsString
from .validator import ValidateIsNumber
from .validator import ValidateNotEmptyString
from .validator import ValidateSiteType
from .validator import ValidateSiteDir
from .validator import ValidateTimeFormat
from .validator import ValidateTimeFlag


@VersionDeco(1)
class ReadYaml(object):
   __slots__ = ['yfileName']

   def __init__(this, a_filename):
      this.yfileName = a_filename

   def genTime(this, a_time, a_cri, a_yaml):
      """
      TODO: Deal with bare time format from yaml
      """
      l_stime = None
      l_etime = None
      l_flag = None

      try:
         a_yaml[a_time]
         try:
            l_stime = a_yaml[a_time]['start'].strip()
            if l_stime == '':
               l_stime = r"1900-01-01T00:00:00.000+00:00"
            l_etime = a_yaml[a_time]['end'].strip()
            if l_etime == '':
               l_etime = r"2100-01-01T00:00:00.000+00:00"
            l_flag = a_yaml[a_time]['flag'].strip()
            if l_flag == '':
               l_flag = 'milli'
         except (KeyError, AttributeError) as ke:
            l_stime = r"1900-01-01T00:00:00.000+00:00"
            l_etime = r"2100-01-01T00:00:00.000+00:00"
            l_flag = "year"
            print("{" + ke.message + "}" + " attribute does not exist in time."
                  " Parse whole log.")
      except KeyError as ke:
         l_stime = r"1900-01-01T00:00:00.000+00:00"
         l_etime = r"2100-01-01T00:00:00.000+00:00"
         l_flag = "year"
         print("{" + ke.message + "}" + " does not reference to any criterion."
               " Parse whole log.")

      if ValidateTimeFormat(l_stime) and ValidateTimeFormat(l_etime) and \
         ValidateTimeFlag(l_flag):
         l_startTimeFilter = TimeFilter(
            "500",  # use SRM 5.0.0's time trait to parse it for checking.... auh~~
            l_stime,
            l_flag)

         if not l_startTimeFilter.ApplyLessEq(l_etime):
            print(ConfigTimeErrorMsg(a_cri, l_stime, l_etime))
            return False
         return SplTime(l_stime, l_etime, l_flag).genTime()

      print(ConfigTimeFormatErrorMsg(a_cri, l_stime, l_etime, l_flag))
      return False

   def genTuple(this, a_list, a_yaml):
      l_listBundle = []
      for l_element in a_list:
         try:
            a_yaml[l_element]
         except KeyError as ke:
            print("{" + ke.message + "}" + " does not reference to any criterion."
                  " Skip this criterion.")
            continue

         l_splList = SplList()

         for l_str in a_yaml[l_element]:
            l_splList.addList(str(l_str).strip())

         l_listBundle.append(l_splList.getTuple())

      return tuple(l_listBundle)

   def genCri(this, a_list, a_yaml):
      l_criteria = []
      for l_cri in a_list:
         try:
            a_yaml[l_cri]
         except KeyError as ke:
            print("{" + ke.message + "}" + " does not reference to any criterion."
                  " Skip this criterion.")
            continue
         try:
            a_yaml[l_cri]['name']
            a_yaml[l_cri]['time']
            a_yaml[l_cri]['info']
            a_yaml[l_cri]['type']
            a_yaml[l_cri]['data']
            a_yaml[l_cri]['bundle']
            a_yaml[l_cri]['logfilename']
         except KeyError as ke:
            print("{" + ke.message + "}" + " attribute does not exist in criterion."
                  " Skip this criterion.")
            continue

         l_name = a_yaml[l_cri]['name'].strip()
         l_time = this.genTime(a_yaml[l_cri]['time'], l_name, a_yaml)
         l_info = this.genTuple(a_yaml[l_cri]['info'], a_yaml)
         l_type = this.genTuple(a_yaml[l_cri]['type'], a_yaml)
         l_data = this.genTuple(a_yaml[l_cri]['data'], a_yaml)
         l_bundle = this.genTuple(a_yaml[l_cri]['bundle'], a_yaml)
         l_logfilename = a_yaml[l_cri]['logfilename'].strip()

         if not ValidateNotEmptyString(l_name):
            print("Criterion name should be in string format and not empty."
                  "Skip this criterion.")
            continue
         if ValidateIsNumber(l_name):
            print("Criterion name should be in string format."
                  "Skip this criterion.")
            continue
         if not ValidateNotEmptyString(l_logfilename) or ValidateIsNumber(l_logfilename):
            from ..splTraits.filefmt import DefaultResultFileName
            l_logfilename = DefaultResultFileName()
         if not l_time:
            print("Skip this criterion.")
            continue

         l_criteria.append(SplCriteria(
            l_name,
            l_time,
            l_info,
            l_type,
            l_data,
            l_bundle,
            l_logfilename).genCri())

      return tuple(l_criteria)

   def LoadYaml(this):
      import yaml

      try:
         l_oneYaml = yaml.load(open(this.yfileName, 'r'))
      except IOError:
         print(LoadYamlFileErrorMsg(this.yfileName))
         return False

      l_sites = []

      for l_site in l_oneYaml['sites']:
         if not ValidateIsString(l_site):
            from ..splGeneral.exceptions import ConfigSiteNameErrorMsg
            print(ConfigSiteNameErrorMsg())
            return False

         try:
            l_oneYaml[l_site]
         except KeyError as ke:
            print("{" + ke.message + "}" + " does not reference to any site."
                  " Skip this site.")
            continue
         try:
            l_oneYaml[l_site]['name']
            l_oneYaml[l_site]['dir']
            l_oneYaml[l_site]['type']
            l_oneYaml[l_site]['dayoffset']
         except KeyError as ke:
            print("{" + ke.message + "}" + " attribute does not exist in this site."
                  " Skip this site.")
            continue

         l_name = l_oneYaml[l_site]['name']
         l_dir = l_oneYaml[l_site]['dir']
         l_type = l_oneYaml[l_site]['type']
         l_dos = l_oneYaml[l_site]['dayoffset']

         if not ValidateNotEmptyString(l_name) or ValidateIsNumber(l_name):
            print("Site name should be in string format and not empty. Skip this site.")
            continue

         if ValidateIsNumber(l_dir):
            print("Site : {" + l_name + "} should have dir in string"
                  "format. Skip this site")
            continue

         if not ValidateSiteDir(l_dir):
            print("Site's dir : {" + l_dir + "} does not exist! Skip this site.")
            continue

         if not ValidateSiteType(l_type):
            print("Site : {" + l_name + "} does not have proper type . Supported type are"
                  "config and sync")
            continue

         if not ValidateIsNumber(l_dos):
            print("Site : {" + l_name + "} does not have proper datoffset . Must be >=0"
                  " integer.")
            continue

         l_sites.append(SplSite(
           l_name.strip(),
           l_dir.strip(),
           this.genCri(l_oneYaml[l_site]['criteria'], l_oneYaml),
           l_type.strip(),
           l_dos).genSite())

      if l_sites.__len__() == 0:
         return False
      else:
         return tuple(l_sites)

__package__ = "srmparserlite.splConfig"
from ..splGeneral.deco import VersionDeco
from ..splFilter.filterr import TimeFilter
from ..splGeneral.exceptions import ConfigTimeErrorMsg


@VersionDeco(1)
class PrepareConfig(object):
   __slots__ = ["sites", "syncState", "syncTime"]

   def __init__(this, a_sites):
      this.sites = a_sites
      this.syncTime = []
      this.syncState = False

   def CheckZeroCriteria(this):
      this.sites[:] = \
         [l_site for l_site in this.sites if l_site["criteria"].__len__() != 0]

   def CheckModifyState(this):
      v_tmpConfig = None

      for l_site in this.sites:
         if l_site["type"] == "sync":
            if this.syncState is False:
               for l_criteria in l_site["criteria"]:
                  this.syncTime.append(l_criteria["time"])

               this.syncState = True
               v_tmpConfig = l_site
               break

      if this.syncState is True:

         for l_site in this.sites:
            if l_site is v_tmpConfig:
               continue
            i = 0
            for l_criteria in l_site["criteria"]:
               try:
                  l_criteria["time"] = this.syncTime[i]
                  i += 1
               except IndexError:
                  break


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
         "flag",
         "chkErr"]

   def __init__(this, a_start, a_end, a_flag):
      this.start = a_start
      this.end = a_end
      this.flag = a_flag
      this.chkErr = False

      l_startTimeFilter = TimeFilter(
         "500",  # use SRM 5.0.0's time trait to parse it for checking.... auh~~
         a_start,
         a_flag)

      if not l_startTimeFilter.ApplyLessEq(a_end):
         this.chkErr = True

   def genTime(this):
      if this.chkErr:
         return False
      else:
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
      this.siteMap = {
            "name": this.name,
            "dir": this.directory,
            "criteria": this.criteria,
            "type": this.theType,
            "dayoffset": this.dayoffset}
      return this.siteMap


@VersionDeco(1)
class ReadYaml(object):
   __slots__ = ['yfileName']

   def __init__(this, a_filename):
      this.yfileName = a_filename

   def genTime(this, a_time, a_yaml):
      return SplTime(
         a_yaml[a_time]['start'].strip(), a_yaml[a_time]['end'].strip(),
         a_yaml[a_time]['flag'].strip()).genTime()

   def genTuple(this, a_list, a_yaml):
      l_listBundle = []
      for l_element in a_list:
         l_splList = SplList()
         for l_str in a_yaml[l_element]:
            l_splList.addList(l_str.strip())
         l_listBundle.append(l_splList.getTuple())

      return tuple(l_listBundle)

   def genCri(this, a_list, a_yaml):
      l_criteria = []
      for l_cri in a_list:
         l_splCri = SplCriteria(
            a_yaml[l_cri]['name'].strip(),
            this.genTime(a_yaml[l_cri]['time'], a_yaml),
            this.genTuple(a_yaml[l_cri]['info'], a_yaml),
            this.genTuple(a_yaml[l_cri]['type'], a_yaml),
            this.genTuple(a_yaml[l_cri]['data'], a_yaml),
            this.genTuple(a_yaml[l_cri]['bundle'], a_yaml),
            a_yaml[l_cri]['logfilename'].strip()).genCri()

         if l_splCri is False:
            print(ConfigTimeErrorMsg(
               a_yaml[l_cri]['name'].strip(),
               a_yaml[a_yaml[l_cri]['time']]['start'].strip(),
               a_yaml[a_yaml[l_cri]['time']]['end'].strip()))
         else:
            l_criteria.append(l_splCri)

      return tuple(l_criteria)

   def LoadYaml(this):
      import yaml
      try:
         l_oneYaml = yaml.load(open(this.yfileName, 'r'))
      except IOError:
         print("Loading " + this.yfileName + " error! Config file might not exist or"
               " spl does not have permission to access.")
         return False

      l_sites = []
      for l_site in l_oneYaml['sites']:
         l_sites.append(SplSite(
            l_oneYaml[l_site]['name'].strip(),
            l_oneYaml[l_site]['dir'].strip(),
            this.genCri(l_oneYaml[l_site]['criteria'], l_oneYaml),
            l_oneYaml[l_site]['type'].strip(),
            l_oneYaml[l_site]['dayoffset']).genSite())

      return tuple(l_sites)

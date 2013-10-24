__package__ = "srmparserlite.splGeneral"

LoadYamlFileErrorMsgtemplate = \
      "Loading {{{0}}} file error! Config file {{{0}}}not exist or " \
      "SPL does not have permission to access the config file."

ConfigSiteNameErrorMsgTemplate = "Site name should be in string format."

ConfigTimeErrorMsgTemplate = \
   "Criterion : {{{0}}} >> Start time : {{{1}}} is ahead of End time : {{{2}}} \n" \
   "Criterion is not processed"

ConfigTimeFormatErrorMsgTemplate = \
      "Criterion : {{{0}}} >> Start time : {{{1}}}, End time : {{{2}}}, " \
      "Flag : {{{3}}}\n" \
      "Format not supported.\nTime Format example: 2013-07-22T09:38:58.779+02:00 \n" \
      "Flag format : milli sec min hour day month year \n" \
      "Criterion is not processed"

ConfigSiteErrorMsgTemplate = \
   "Site: {{{0}}} >> {1} \n" \
   "Site {{{0}}} is not processed"

ConfigCriteriaErrorMsgTemplate = \
   "Site: {{{0}}} >> {1} \n" \
   "Site {{{0}}} is not processed"

ExceptionMsgTemplate = "Source location : {0} >> Error message : {1}"


def ConfigSiteNameErrorMsg():
   return ConfigSiteNameErrorMsgTemplate


def LoadYamlFileErrorMsg(a_fileName):
   return LoadYamlFileErrorMsgtemplate.format(a_fileName)


def ConfigTimeErrorMsg(a_criteria, a_stime, a_etime):
   return ConfigTimeErrorMsgTemplate.format(a_criteria, a_stime, a_etime)


def ConfigTimeFormatErrorMsg(a_criteria, a_stime, a_etime, a_flg):
   return ConfigTimeFormatErrorMsgTemplate.format(a_criteria, a_stime, a_etime, a_flg)


class GenSrcLocation(object):
   __slots__ = ["loc"]

   def __init__(this, a_loc):
      this.loc = a_loc

   def __str__(this):
      return this.loc


class NotGzFileFormat(IOError):
   def __init__(this, a_srcloc, a_msg=None):
      super(NotGzFileFormat, this).__init__()
      SL = a_srcloc
      EM = "File : " + a_msg + " is not a gz file!"
      this.message = ExceptionMsgTemplate.format(SL, EM)


class NoHeaderLineException(Exception):
   def __init__(this, a_srcloc, a_msg=None):
      super(NoHeaderLineException, this).__init__()
      SL = a_srcloc
      EM = "No header line in " + a_msg + " log file or log format error"
      this.message = ExceptionMsgTemplate.format(SL, EM)


class UnSupportFormatException(Exception):
   def __init__(this, a_srcloc, a_msg=None):
      super(UnSupportFormatException, this).__init__()
      SL = a_srcloc
      EM = "Unsupport Format! Content : " + a_msg
      this.message = ExceptionMsgTemplate.format(SL, EM)


class NoTraitException(Exception):
   def __init__(this, a_srcloc, a_msg=None):
      super(NoTraitException, this).__init__()
      SL = a_srcloc
      EM = "No version trait " + a_msg + " available!"
      this.message = ExceptionMsgTemplate.format(SL, EM)


class NoFileToGenException(Exception):
   def __init__(this, a_srcloc, a_msg=None):
      super(NoFileToGenException, this).__init__()
      SL = a_srcloc
      EM = "No gz or log files avaiable for generating one big file(TM)"
      this.message = ExceptionMsgTemplate.format(SL, EM)

__package__ = "srmparserlite.splGeneral"

ExceptionMsgTemplate = "Source location : {0} >> Error message :{1}"


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

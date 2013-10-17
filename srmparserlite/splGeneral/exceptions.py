__package__ = "srmparserlite.splGeneral"


class NoHeaderLineException(Exception):
   def __init__(this):
      this.message = "No Header Line in Log file or format error!"


class UnSupportFormatException(Exception):
   def __init__(this, a_msg):
      this.message = "Unsupport Format! Content : " + a_msg


class NoTraitException(Exception):
   def __init__(this):
      this.message = "No version trait can be found!"

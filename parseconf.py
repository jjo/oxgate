"""Parses simple var=value configuration file"""

import ConfigParser
import StringIO

VARS_REQ = ['my_jid', 'peer_jid', 'password', 'udpport']
VARS_OPT = {'server':None, 'debug':0, 'visible':0}

MAIN_SECTION = 'main'

class ParseConf(ConfigParser.ConfigParser):
  """
  Derived class from ConfigParser, to be able to read a file without
  any section header at all.
  """

  def read(self, filename):
    """
    Reads configuration file, preappending a [main] section,
    to satisfy ConfigParser library
    """

    try:
      text = open(filename).read()
    except IOError:
      pass
    else:
      filep = StringIO.StringIO("[%s]\n" % MAIN_SECTION + text)
      self.readfp(filep, filename)
    return self

  def getvar(self, varname):
    """
    Get variable's value, supporting VARS_OPT optional (thus defaulted)
    values.
    """
    try:
      val = self.get(MAIN_SECTION, varname)
    except ConfigParser.NoOptionError:
      val = VARS_OPT[varname]
      
    return val

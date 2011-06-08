"implements msg passing interface for file streams"
import msgio
import asyncore


class MsgFILE(msgio.MsgIO, asyncore.file_dispatcher):
  "main class: simple read -> msg implementation"
  def __init__(self, filep):
    msgio.MsgIO.__init__(self)
    asyncore.file_dispatcher.__init__(self, filep.fileno())
    self._filep = filep

  def msg_recv(self):
    pass

  def msg_send(self, msg):
    pass

  def async_init(self):
    "attach my filedescriptor to the asyncore"
    asyncore.file_dispatcher.__init__(self, self._filep.fileno())

  def writable(self):
    pass

  def handle_connect(self):
    pass

  def handle_read(self):
    msg = None
    try:
      msg = self._filep.read()
    except IOError:
      pass

    self.msg_target.msg_send(msg)

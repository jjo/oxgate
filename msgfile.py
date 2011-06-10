"implements msg passing interface for file streams"
import msgio
import asyncore


class MsgFILE(msgio.AsyncMsgIO, asyncore.file_dispatcher):
  _readable = True
  "main class: simple read -> msg implementation"
  def __init__(self, filep):
    msgio.AsyncMsgIO.__init__(self)
    asyncore.file_dispatcher.__init__(self, filep.fileno())
    self._filep = filep

  def msg_recv(self):
    "msg_recv: read the file object"
    return self._filep.read()

  def msg_send(self, msg):
    "no msg send possible for file (read-only implementation)"
    raise IOError('MsgFILE doesnt implement msg_send')

  def async_init(self):
    "attach my filedescriptor to the asyncore"
    asyncore.file_dispatcher.__init__(self, self._filep.fileno())

  def writable(self):
    "no write possible for file (read-only implementation)"
    #TODO(jjo): asyncore should not call this
    #raise IOError('MsgFILE doenst allow write')
    pass

  def readable(self):
    return self._readable

  def handle_connect(self):
    "file objects dont 'connect'"
    raise IOError('MsgFILE doesnt support connect semantics')

  def handle_read(self):
    "callback from asyncore when there's a read possible"
    msg = None
    try:
      msg = self.msg_recv()
    except IOError:
      self._readable = False
    else:
      self.msg_target.msg_send(msg)

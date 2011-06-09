# vim: sw=2:ts=2
"abstract base class for msg passing"
import asyncore


class AsyncMsgIO(asyncore.dispatcher):
  "Specialized MsgIO class that uses asyncore dispatching"
  msg_target = None
  msg_encode = None
  msg_decode = None

  def writable(self):
    """"abstract base class stub: called from asyncore to know if 
        the descriptor is writable"""
    #raise NotImplementedError('missing writable() implementation')
    pass

  def handle_connect(self):
    "abstract base class stub: called from asyncore to trigger connection"
    #raise NotImplementedError('missing handle_connect() implementation')
    pass

  def handle_read(self):
    "abstract base class stub: called from asyncore when readable"
    self.msg_recv_ready()
    self.msg_recv_loop()

  def async_init(self):
    "setup asyncore component: attach my socket to it"
    asyncore.dispatcher.__init__(self, sock=self.getsock())

  def msg_send(self, msg):
    "derived class must implement msg_send semantics"
    raise NotImplementedError('missing msg_send() implementation')

  def msg_recv(self):
    "derived class must implement msg_recv semantics"
    raise NotImplementedError('missing msg_recv() implementation')

  def msg_recv_loop(self):
    "main loop: exchange msgs over already setup channels"
    while True:
      msg = self.msg_recv()
      if (msg==None):
        break
      try:
        if (self.msg_decode):
          msg = self.msg_decode(msg)
        if (msg==None):
          continue
        print "msg=", msg
        if (self.msg_target.msg_encode):
          msg = self.msg_target.msg_encode(msg)
        if (msg==None):
          continue
        self.msg_target.msg_send(msg)
      except IOError:
        continue

  def set_msg_target(self, msg_target, msg_encode=None, msg_decode=None):
    "setup a 'connection' from origin(self) to target"
    self.msg_target = msg_target
    self.msg_encode = msg_encode
    self.msg_decode = msg_decode


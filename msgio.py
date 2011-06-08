# vim: sw=2:ts=2
"abstract base class for msg passing"
import asyncore


class MsgIO:
  "main msg exchanging base class"
  msg_target = None
  msg_encode = None
  msg_decode = None

  def __init__(self):
    pass

  def msg_send(self, msg):
    "send a msg over my channel" 
    raise NotImplementedError()

  def msg_recv(self):
    "receive a msg from my channel" 
    raise NotImplementedError()

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


class AsyncMsgIO(MsgIO, asyncore.dispatcher):
  "Specialized MsgIO class that uses asyncore dispatching"
  def writable(self):
    pass

  def handle_connect(self):
    pass

  def handle_read(self):
    self.msg_recv_ready()
    self.msg_recv_loop()

  def async_init(self):
    "setup asyncore component: attach my socket to it"
    asyncore.dispatcher.__init__(self, sock=self.getsock())

  def msg_send(self, msg):
    pass

  def msg_recv(self):
    pass

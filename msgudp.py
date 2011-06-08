# vim: sw=2:ts=2
"""msgudp.py: implements UDP msg interface for asyncore""" 
import socket
import msgio


class MsgUDP(socket.socket, msgio.AsyncMsgIO):
  """implement UDP msg interface"""
  _port = None
  def __init__(self):
    msgio.AsyncMsgIO.__init__(self)
    socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)
    self.__queue = []
    self.latest_src = ()

  def bindport(self, port):
    """binds to passed port"""
    self._port = int(port)
    if self._port:
      bindaddr = ('', self._port)
    self.bind(bindaddr)

  def __enqueue(self, msg):
    """queue message for async processing"""
    return self.__queue.append(msg)

  def __dequeue(self):
    """dequeue message from async processing"""
    return self.__queue.pop()

  def getsock(self):
    """return a reference to open socket"""
    return self

  def msg_recv_ready(self):
    """called when there's the socket can be read for a msg"""
    msg, self.latest_src = self.recvfrom(8192)
    print "msgudp.recvfrom len=%d <-" % len(msg), self.latest_src
    self.__enqueue(msg)

  def msg_send(self, msg):
    """send passed message to latest_src UDP peer"""
    if (self.latest_src):
      print "msgudp.msg_send ->", self.latest_src
      try:
        self.sendto(msg, self.latest_src)
      except IOError:
        self.latest_src = ()

  def msg_recv(self):
    """dequeue message from async queue"""
    msg = None
    try:
      msg = self.__dequeue()
    finally: 
      pass
    return msg

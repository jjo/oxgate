"implements message passing over XMPP (jabber) channel"
# vim: sw=2:ts=2
import xmpp
import re
import msgio


class MsgJAB(xmpp.Client, msgio.AsyncMsgIO):
  "main class for XMPP message passing"
  def __init__(self, jid, passwd, peer_jid, debug=0): 
    #xmpp.Client.__init__(self, server=None) ## jjo: NOPE
    msgio.AsyncMsgIO.__init__(self)
    jid_re = re.compile(r'(?P<user>^[\w.]+)@(?P<domain>[\w.]+)(/(?P<resource>[\w.-]+))?')
    jid_dict = jid_re.match(jid).groupdict()
    self.user = jid_dict.get("user")
    self.domain = jid_dict.get("domain")
    self.resource = jid_dict.get("resource")
    self.host = self.domain
    self.debug = debug
    self.peer_jid = peer_jid
    self._passwd = passwd
    self.__queue = []
    self.create_client()

  def create_client(self):
    "creates XMPP client instance"
    #self.messageHandler=None
    self.xmpp_client = xmpp.Client(self.domain, debug=self.debug)
    self.xmpp_client.msgjab = self

  def doconnect(self, host=None, port=5222):
    "creates XMPP client instance"
    if host:
      self.host = host
    if not self.xmpp_client.connect(server = (self.host, port)):
      raise IOError('Can not connect with jabber server "%s".' % self.host)
    if not self.xmpp_client.auth(self.user, self._passwd, self.resource):
      raise IOError('Can not auth with jabber server "%s".' % self.host)
    self.xmpp_client.RegisterHandler('message', msgjab_messagehandler)

  def disconnect(self):
    "tears down XMPP channel"
    self.xmpp_client.disconnect()

  def _enqueue(self, msg):
    "enqueue a just-read message from XMPP channel"
    return self.__queue.append(msg)

  def __dequeue(self):
    "dequeue a msg for later sending"
    return self.__queue.pop()

  def sendinitpresence(self):
    "XMPP protocol: make me present"
    self.xmpp_client.sendInitPresence(0)

  def fileno(self):
    "return XMPP channel socket filedescriptor, needed by asyncore"
    return self.xmpp_client.TCPsocket._sock.fileno()

  def getsock(self):
		"return XMPP channel socket object"
    return self.xmpp_client.TCPsocket._sock

  def msg_send(self, msg):
    print "msgjab.msg_send ->", self.peer_jid
    return self.xmpp_client.send(xmpp.Message(self.peer_jid, msg))

  def msg_recv_ready(self, timeout=None):
    """
    Called from asyncore when socket is readable: read and process incoming
    stream, which may not be a complete msg (yet)
    """

    self.xmpp_client.Process(timeout)

  def msg_recv(self):
    msg = None
    try:
      msg = self.__dequeue()
      print "msgjab.msg_recv <-", self.peer_jid
    finally: 
      return msg

def msgjab_messagehandler(conn, mess_node):
  "messageHandler callback for xmpppy, must be static"
  conn._owner.msgjab._enqueue(mess_node.getBody())

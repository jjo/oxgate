"implements message passing over XMPP (jabber) channel"
# vim: sw=2:ts=2
import xmpp
import re
import msgio


class MsgJAB(xmpp.Client, msgio.AsyncMsgIO):
  "main class for XMPP message passing"

  def __init__(self, jid, passwd, peer_jid, server = None, debug = 0): 
    #xmpp.Client.__init__(self, server=None) ## jjo: NOPE
    msgio.AsyncMsgIO.__init__(self)
    jid_re = re.compile(r'(?P<user>^[\w.]+)@(?P<domain>[\w.]+)(/(?P<resource>[\w.-]+))?')
    jid_dict = jid_re.match(jid).groupdict()
    self._user = jid_dict.get("user")
    self._domain = jid_dict.get("domain")
    self._resource = jid_dict.get("resource")
    self._passwd = passwd
    self._host = self._domain
    self._peer_jid = peer_jid
    self.debug = debug
    self.__queue = []
    self.xmpp_client = xmpp.Client(self._domain, debug=self.debug)
    self.xmpp_client.msgjab = self

  def doconnect(self, host=None, port=5222):
    "creates XMPP client instance"
    if host:
      self._host = host
    if not self.xmpp_client.connect(server = (self._host, port)):
      raise IOError('Can not connect with jabber server "%s".' % self._host)
    if not self.xmpp_client.auth(self._user, self._passwd, self._resource):
      raise IOError('Can not auth with jabber server "%s".' % self._host)
    self.xmpp_client.RegisterHandler('message', msgjab_messagehandler)
    self.xmpp_client.sendInitPresence(0)

  def disconnect(self):
    "tears down XMPP channel"
    self.xmpp_client.disconnect()

  def _enqueue(self, msg):
    "enqueue a just-read message from XMPP channel"
    return self.__queue.append(msg)

  def __dequeue(self):
    "dequeue a msg for later sending"
    return self.__queue.pop()

  def fileno(self):
    "return XMPP channel socket filedescriptor, needed by asyncore"
    return self.xmpp_client.TCPsocket._sock.fileno()

  def getsock(self):
		"return XMPP channel socket object"
    return self.xmpp_client.TCPsocket._sock

  def msg_send(self, msg):
    print "msgjab.msg_send ->", self._peer_jid
    return self.xmpp_client.send(xmpp.Message(self._peer_jid, msg))

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
      print "msgjab.msg_recv <-", self._peer_jid
    finally: 
      return msg

def msgjab_messagehandler(conn, mess_node):
  "messageHandler callback for xmpppy, must be static"
  conn._owner.msgjab._enqueue(mess_node.getBody())

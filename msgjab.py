# $Id: msgjab.py,v 1.17 2005/08/17 03:47:30 jjo Exp $
# vim: sw=2:ts=2
import xmpp
import re
import msgio
class msgjab(xmpp.Client,msgio.asyncmsgio):
	def __init__(self, jid, passwd, peer_jid, debug=0): 
		self.JID_RE=re.compile(r'(?P<user>^[\w.]+)@(?P<domain>[\w.]+)(/(?P<resource>[\w.-]+))?')
		jid_dict=self.__jid_match(jid)
		self.user=jid_dict.get("user")
		self.domain=jid_dict.get("domain")
		self.resource=jid_dict.get("resource")
		self.host=self.domain
		self.debug=debug

		self.peer_jid=peer_jid
		self._passwd=passwd
		self.__queue=[]
		self.create_client()

	def create_client(self):
		#self.messageHandler=None
		self.xmpp_client=xmpp.Client(self.domain, debug=self.debug)
		self.xmpp_client.msgjab=self

	def connect(self,host=None,port=5222):
		if host:
			self.host=host

		if not self.xmpp_client.connect(server=(self.host,port)):
			raise IOError('Can not connect with jabber server "%s".' % self.host)
		if not self.xmpp_client.auth(self.user,self._passwd,self.resource):
			raise IOError('Can not auth with jabber server "%s".' % self.host)
		self.xmpp_client.RegisterHandler('message',msgjab_messageHandler)
	def disconnect(self):
		self.xmpp_client.disconnect()
	def _enqueue(self, e):
		return self.__queue.append(e)
	def __dequeue(self):
		return self.__queue.pop()
	def __jid_match(self, jid):
		return self.JID_RE.match(jid).groupdict()

	def sendinitpresence(self):
		self.xmpp_client.sendInitPresence(0);
	def fileno(self):
		return self.xmpp_client.TCPsocket._sock.fileno()
	def getsock(self):
		return self.xmpp_client.TCPsocket._sock
	def msg_send(self, msg):
		print "msgjab.msg_send ->", self.peer_jid
		return self.xmpp_client.send(xmpp.Message(self.peer_jid,msg))
	def msg_recv_ready(self, timeout=None):
		self.xmpp_client.Process(timeout)
	def msg_recv(self):
		m=None
		try:
			m=self.__dequeue()
			print "msgjab.msg_recv <-", self.peer_jid
		finally: 
			return m

def msgjab_messageHandler(conn, mess_node):
		"messageHandler callback for xmpppy, must be static"
		conn._owner.msgjab._enqueue(mess_node.getBody())
		#messageHandler=staticmethod(messageHandler)

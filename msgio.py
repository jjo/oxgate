# $Id: msgio.py,v 1.4 2005/08/17 03:47:30 jjo Exp $
#
# vim: sw=2:ts=2
import asyncore
class msgio:
	msg_target=None
	msg_encode=None
	msg_decode=None
	def msg_send(self,m): raise NotImplementedError()
	def msg_recv(self): raise NotImplementedError()
	def msg_recv_loop(self):
		while True:
			m=self.msg_recv()
			if (m==None): 
				break
			try:
				if (self.msg_decode): m=self.msg_decode(m)
				if (m==None): continue
				print "m=", m
				if (self.msg_target.msg_encode): m=self.msg_target.msg_encode(m)
				if (m==None): continue
				self.msg_target.msg_send(m)
			except: 
				continue
	def set_msg_target(self, msg_target, msg_encode=None, msg_decode=None):
		self.msg_target=msg_target
		self.msg_encode=msg_encode
		self.msg_decode=msg_decode

class asyncmsgio(msgio,asyncore.dispatcher):
	def writable(self): pass
	def handle_connect(self): pass
	def handle_read(self):
		self.msg_recv_ready()
		self.msg_recv_loop()
	def handle_error(self): raise "msgio.handle_error() exception"
	def async_init(self):
		asyncore.dispatcher.__init__(self, sock=self.getsock())

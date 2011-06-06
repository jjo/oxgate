# $Id: msgfile.py,v 1.1 2005/07/03 16:06:03 jjo Exp $
#
import msgio
import asyncore
class msgfile(msgio.msgio,asyncore.file_dispatcher):
	def __init__(self,file):
		self.file=file
	def async_init(self):
		asyncore.file_dispatcher.__init__(self, self.file.fileno())
	def writable(self): pass
	def handle_connect(self): pass
	def handle_read(self):
		self.msg_target.msg_send(self.file.read())

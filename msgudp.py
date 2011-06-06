# $Id: msgudp.py,v 1.7 2005/07/26 03:28:33 jjo Exp $
# vim: sw=2:ts=2
import os
import sys
import socket
import msgio


class msgudp(socket.socket, msgio.asyncmsgio):
	def __init__(self):
		socket.socket.__init__(self,socket.AF_INET, socket.SOCK_DGRAM)
		self.__queue=[]
		self.last_src=()
	def bindport(self,port):
		self.port=int(port)
		if self.port:
			bindaddr=('', self.port)
		self.bind(bindaddr)

	def __enqueue(self, e):
		return self.__queue.append(e)
	def __dequeue(self):
		return self.__queue.pop()

	def getsock(self):
		return self
	def msg_recv_ready(self):
		m,self.last_src=self.recvfrom(8192)
		print "msgudp.recvfrom len=%d <-" % len(m), self.last_src
		self.__enqueue(m)
	def msg_send(self,m):
		if (self.last_src):
			print "msgudp.msg_send ->", self.last_src
			try:
				self.sendto(m, self.last_src)
			except:
				self.last_src=()

	def msg_recv(self):
		m=None
		try:
			m=self.__dequeue()
		finally: 
			return m

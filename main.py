#!/usr/bin/python
# $Id: main.py,v 1.30 2005/07/26 03:28:32 jjo Exp $
# vim: sw=2:ts=2

#
# OXG: OpenVPN XMPP Gateway: encapsulate UDP datagrams via Jabber clients (XMPP streams)
#
# Should investigate and use IBB, xmpppy does (experimentaly) implement it
#
import os
import sys
import socket
import asyncore
import errno

from parseconf import *

import msgudp
import msgjab
import msgfile
import encoding

# __main__
try:
	conf=parseargs(sys.argv)
except:
	sys.exit(1)

buffer_size=8192

def main():
	udp=msgudp.msgudp()
	jab=msgjab.msgjab(conf.my_jid, conf.password, conf.peer_jid, debug=conf.debug)
	stdinmsg=msgfile.msgfile(sys.stdin)

	udp.bindport(conf.udpport)
	udp.set_msg_target(jab, encoding.tobinary, encoding.toascii)
	jab.set_msg_target(udp)
	stdinmsg.set_msg_target(jab)

	jab.connect(conf.server)
	jab.sendinitpresence()
	for x in [udp, jab, stdinmsg]:
		x.async_init()
	asyncore.loop()

main()

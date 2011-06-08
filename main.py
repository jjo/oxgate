#!/usr/bin/python
# vim: sw=2:ts=2
#
# Should investigate and use IBB, xmpppy does (experimentaly) implement it
#
"""
OXG: OpenVPN XMPP Gateway: encapsulate UDP datagrams via Jabber clients
(XMPP streams)
"""

import sys
import asyncore
import parseconf

import msgudp
import msgjab
import msgfile
import encoding

def main():
  """ main loop: will exchange messages between xmpp<->{udp,stdin} """
  #try:
  conf = parseconf.ParseConf()
  conf.read(sys.argv[1])
  print conf
  #except:
  #  sys.exit(1)
  udp = msgudp.MsgUDP()
  jab = msgjab.MsgJAB(
    conf.getvar('my_jid'),
    conf.getvar('password'),
    conf.getvar('peer_jid'),
    debug=conf.getvar('debug')
  )
  stdinmsg = msgfile.MsgFILE(sys.stdin)

  udp.bindport( conf.getvar('udpport'))
  udp.set_msg_target(jab, encoding.tobinary, encoding.toascii)
  jab.set_msg_target(udp)
  stdinmsg.set_msg_target(jab)

  jab.doconnect( conf.getvar('server'))
  jab.sendinitpresence()
  for async_msgdispatcher in [udp, jab, stdinmsg]:
    async_msgdispatcher.async_init()
  asyncore.loop()

if __name__ == "__main__":
  main()

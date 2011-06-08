# vim: sw=2:ts=2
"""Implement de/en-coding for "binary" from/to ascii messages"""

import base64

def toascii(pkt):
  """Convert a pkt to a printable char string (msg)"""
  return "base64:" + base64.encodestring(pkt)

def tobinary(msg):
  """Convert a printable msg to a pkt """
  if (msg[:7]!="base64:"):
    print msg
    return None
  pkt = base64.decodestring(msg[7:])
  return pkt

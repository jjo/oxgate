# vim: sw=2:ts=2
import base64

def toascii(m):
	return "base64:" + base64.encodestring(m)

def tobinary(m):
	if (m[:7]!="base64:"):
		print m
		return None
	m=base64.decodestring(m[7:])
	return m

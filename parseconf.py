# $Id: parseconf.py,v 1.3 2005/08/17 03:47:30 jjo Exp $
class parseconf(object):
	vars_req= ['my_jid', 'peer_jid', 'password', 'udpport']
	vars_opt= {'server':None, 'debug':0, 'visible':0}
	def __init__(self, conf_file):
		# parse conf_file, create dictionary w/found  varname = val
		conf_params={}
		for line in open(conf_file).readlines():
			try: key,val=line.strip().split('=',1)
			except: continue
			if (key[0]=='#'): continue
			conf_params[key.lower()]=val

		# assign required vars as config object attributes
		for varname in self.vars_req:
			try:
				self.__setattr__(varname, conf_params[varname])
			except:
				print "\nERROR: missing '%s' variable in %s config file\n" % (varname, conf_file)
				sys.exit(1)
		# assign optional vars as config object attributes (w/default)
		for varname, val in self.vars_opt.items():
			try:
				self.__setattr__(varname, conf_params[varname])
			except: 
				self.__setattr__(varname, val)

def parseargs(argv):
	try:
		conf_file=argv[1]
	except: 
		print """
usage: %s <conf_file>

	conf_file example:
	#required variables: %s
	my_jid=user@some.jabber.org/v1
	peer_jid=user@some.jabber.org/v2
	password=s0mep4SS
	udpport=1194
	#optional variables: %s
	server=actual.server.address.org
		
		""" % (argv[0], parseconf.vars_req, parseconf.vars_opt.keys())
		raise Error, 'missing conf_file'

	return parseconf(conf_file)
	
	

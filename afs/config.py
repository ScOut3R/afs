import yaml
import sys
import re
from afs.errors import Error

def parse_config(args):
	
	configfile = open(args.config, "r")
	options = yaml.load(configfile)
	configfile.close()
	
	if args.noreload:
		doreload = False
	else:
		doreload = True
	
	if not options.has_key('manage'):
		sys.exit("No 'manage' block in config.yml!")
	elif options['manage'] == None:
		sys.exit("The 'manage' block does not contain any definition!")
	
	if not options.has_key('network'):
		options['network'] = '/etc/afs/network.yml'

	for service in options['manage']:
		if not options.has_key(service):
			msg = ("No %s block in config.yml!") % service
			sys.exit(msg)

	networkfile = open(options['network'], "r")
	network = yaml.load(networkfile)
	networkfile.close()
	
	return ({ 'options': options, "network": network, "doreload": doreload })

class Config(object):
	
	def __init__(self, options, network, doreload):
		self.options = options
		self.network = network
		self.doreload = doreload
		
		for key in self.network.keys():
			if not self.network[key].has_key('host'):
				self.network[key]['host'] = key

	def validate(self):
		self.validate_hostname()

	def validate_hostname(self):
		
		hosts = [ self.network[host]['host'] for host in self.network.keys() ]
		regex = re.compile('[^a-z0-9-]')
		for host in self.network.keys():
			
			hostname = self.network[host]['host']
			
			check = regex.search(hostname)
			if not check == None:
				sys.exit( "%s includes invalid character: %s" % ( hostname, check.group(0) ) )
			elif self.network[host]['host'][0] == '-':
				sys.exit( "%s begins with invalid character: -" % hostname )
	
			if hosts.count(hostname) > 1:
				for duplicate_host in self.network.keys():
					if self.network[duplicate_host]['host'] != hostname:
						continue
					if duplicate_host == host:
						continue
					if self.network[host]['ip'] == self.network[duplicate_host]['ip'] and hostname == self.network[duplicate_host]['host']:
						continue
					else:
						raise Error( "%s has a duplicated host configuration!" % host )

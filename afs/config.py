import yaml
import re
from afs.errors import Error
from socket import inet_aton
from socket import error as socket_error

def parse_config(args):
	
	configfile = open(args.config, "r")
	options = yaml.load(configfile)
	configfile.close()
	
	if args.noreload:
		doreload = False
	else:
		doreload = True
	
	if not options.has_key('manage'):
		raise Error("No 'manage' block in config.yml!")
	elif options['manage'] == None:
		raise Error("The 'manage' block does not contain any definition!")
	
	if not options.has_key('network'):
		options['network'] = '/etc/afs/network.yml'

	for service in options['manage']:
		if not options.has_key(service):
			raise Error( "No %s block in config.yml!" % service )

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
		if self.options.has_key('dhcp') or self.options.has_key('dns') or self.options.has_key('radius'):
			self.validate_ip()
			self.validate_hostname()
		
		if self.options.has_key('shorewall'):
			self.validate_shorewall()

	def validate_hostname(self):
		
		hosts = [ self.network[host]['host'] for host in self.network.keys() ]
		regex = re.compile('[^a-z0-9-]')
		for host in self.network.keys():
			
			hostname = self.network[host]['host']
			
			check = regex.search(hostname)
			if not check == None:
				raise Error( "%s includes invalid character: %s" % ( hostname, check.group(0) ) )
			elif self.network[host]['host'][0] == '-':
				raise Error( "%s begins with invalid character: -" % hostname )
	
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

	def validate_ip(self):
		
		for host in self.network.keys():
			
			for duplicate_host in self.network.keys():
				if host == duplicate_host or self.network[host]['host'] == self.network[duplicate_host]['host']:
					continue

				if self.network[host]['ip'] == self.network[duplicate_host]['ip'] and self.network[host]['host'] != self.network[duplicate_host]['host']:
					raise Error( "%s has duplicated ip configuration!" % host )
		
			try:
				inet_aton(self.network[host]['ip'])
			except socket_error:
				raise Error( "%s has invalid IP address configuration!" % host )

	def validate_shorewall(self):
		for module in self.options['shorewall']['modules']:
			if not self.options['shorewall'].has_key(module):
				raise Error("Shorewall does not have %s module config!" % module )

		if self.options['shorewall'].has_key('maclist'):
			if not self.options['shorewall']['maclist'].has_key('interface'):
				raise Error("Shorewall maclist module does not define an interface!")
			if not self.options['shorewall']['maclist'].has_key('configfile'):
				raise Error("Shorewall maclist module does not define the 'configfile' option!")

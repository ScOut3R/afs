import yaml
import sys

class Config(object):
	
	def __init__(self, args):
		
		self.configfile = open(args.config, "r")
		self.options = yaml.load(self.configfile)
		self.configfile.close()
		
		if args.noreload:
			self.doreload = False
		else:
			self.doreload = True
		
		if not self.options.has_key('manage'):
			sys.exit("No 'manage' block in config.yml!")
		elif self.options['manage'] == None:
			sys.exit("The 'manage' block does not contain any definition!")
		
		if not self.options.has_key('network'):
			self.options['network'] = '/etc/afs/network.yml'

		for service in self.options['manage']:
			if not self.options.has_key(service):
				msg = ("No %s block in config.yml!") % service
				sys.exit(msg)

		self.networkfile = open(self.options['network'], "r")
		self.network = yaml.load(self.networkfile)
		self.networkfile.close()
		
		for key in self.network.keys():
			if not self.network[key].has_key('host'):
				self.network[key]['host'] = key

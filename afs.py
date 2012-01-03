#!/usr/bin/python
import __main__
import argparse
import yaml
import sys
import os

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

class ServiceBase(object):
	
	def __init__(self, config):
		self.network = config.network

	def reload_service(self):
		os.system(self.options['reload'])
		
class DHCP(ServiceBase):
	
	def __init__(self, config):
		super(self.__class__, self).__init__(config)
		self.options = config.options['dhcp']
		
	def generate(self):
		output = open(self.options['configfile'], "w")
		
		for host in sorted(self.network.keys()):
			template = """
host %s {
	hardware ethernet %s;
	fixed-address %s;
}\n
""" % ( host, self.network[host]['mac'], self.network[host]['ip'] )
			output.write(template)

		output.close()

class DNS(ServiceBase):
	
	def __init__(self, config):
		super(self.__class__, self).__init__(config)
		self.options = config.options['dns']
		self.written = []
	
	def generate(self):
		forward_output = open(self.options['forward-zone-file'], "w")
		reverse_output = open(self.options['reverse-zone-file'], "w")
		
		for host in sorted(self.network.keys()):
			if self.network[host]['host'] not in self.written:
				template = "%s\tIN\tA\t%s\n" % ( self.network[host]['host'], self.network[host]['ip'] )
				forward_output.write(template)
			
				template = "%s\tPTR\t%s.%s.\n" % ( self.network[host]['ip'].rsplit('.')[3], self.network[host]['host'], self.options['domain'] )
				reverse_output.write(template)
				
				self.written.append(self.network[host]['host'])
			
		forward_output.close()
		reverse_output.close()

class RADIUS(ServiceBase):
	
	def __init__(self, config):
		super(self.__class__, self).__init__(config)
		self.options = config.options['radius']
		
	def generate(self):
		output = open(self.options['macfile'], "w")
		
		for host in sorted(self.network.keys()):
			if self.network[host].has_key('radius'):
				template = """
#%s
%s
\tReply-Message = "Device with MAC Address %%{User-Name} authorized for network access"
""" % ( host, self.network[host]['mac'] )
			
				output.write(template)
		
		output.close()

def generate(config):
	
	for service in config.options['manage']:
		service_obj = getattr(__main__, service.upper())
		service_obj = service_obj(config)
		service_obj.generate()
		if config.options[service].has_key('reload') and config.doreload == True:
			service_obj.reload_service()

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Automated Firewall System')
	parser.add_argument('command', choices=[ 'generate' ], help='what operation to perform (choices: %(choices)s)', metavar="command")
	parser.add_argument('-c', '--config', default='/etc/afs/config.yml', help='use alternate config file (default: %(default)s)')
	parser.add_argument('-n', '--noreload', action="store_const", const=True, help="don't reload services")
	
	args = parser.parse_args()
	
	config = Config(args)
	
	if args.command == 'generate':
		generate(config)

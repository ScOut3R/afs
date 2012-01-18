#!/usr/bin/python
import argparse
import yaml
import sys
from afs.services import *

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

def generate(config):
	
	for service in config.options['manage']:
		service_obj = sys.modules['afs.services.' + service].__dict__[service.upper()](config)
		service_obj.generate()
		if config.options[service].has_key('reload') and config.doreload == True:
			service_obj.reload_service()

def main():
	
	parser = argparse.ArgumentParser(description='Automated Firewall System')
	parser.add_argument('command', choices=[ 'generate' ], help='what operation to perform (choices: %(choices)s)', metavar="command")
	parser.add_argument('-c', '--config', default='/etc/afs/config.yml', help='use alternate config file (default: %(default)s)')
	parser.add_argument('-n', '--noreload', action="store_const", const=True, help="don't reload services")
	
	args = parser.parse_args()
	
	config = Config(args)
	
	if args.command == 'generate':
		generate(config)

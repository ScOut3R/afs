#!/usr/bin/python
import argparse
import sys
from afs.services import *
from afs.config import Config, parse_config
from afs.errors import Error

def generate(config, verbose):
	
	for service in config.options['manage']:
		service_obj = sys.modules['afs.services.' + service].__dict__[service.upper()](config)
		if verbose == True:
			print "Generating %s" % service_obj.__class__.__name__
		service_obj.generate()
		if config.options[service].has_key('reload') and config.doreload == True:
			if verbose == True:
				print "Reloading %s" % service_obj.__class__.__name__
			service_obj.reload_service()

def main():
	
	parser = argparse.ArgumentParser(description='Automated Firewall System')
	parser.add_argument('command', choices=[ 'generate', 'check' ], help='what operation to perform (choices: %(choices)s)', metavar="command")
	parser.add_argument('-c', '--config', default='/etc/afs/config.yml', help='use alternate config file (default: %(default)s)')
	parser.add_argument('-n', '--noreload', action="store_const", const=True, help="don't reload services")
	parser.add_argument('-v', '--verbose', action="store_const", const=True, help="verbose mode")
	
	args = parser.parse_args()
	
	try:
		if args.verbose == True:
			print "Parsing configuration"
		parse = parse_config(args)
	except Error as e:
		sys.exit(e.msg)
	config = Config(parse['options'], parse['network'], parse['doreload'])
	try:
		if args.verbose == True:
			print "Validating configuration"
		config.validate()
	except Error as e:
		sys.exit(e.msg)
	
	if args.command == 'check':
		print "Syntax OK"
		sys.exit(0)

	if args.command == 'generate':
		try:
			if args.verbose == True:
				print "Starint config generation"
			generate(config, args.verbose)
			if args.verbose == True:
				print "Configuration has been generated"
		except Error as e:
			sys.exit(e.msg)

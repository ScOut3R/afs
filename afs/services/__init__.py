import os

__all__ = [ "dhcp", "dns", "radius" ]

class ServiceBase(object):
	
	def __init__(self, config):
		self.network = config.network
		self.options = config.options[self.__class__.__name__.lower()]

	def reload_service(self):
		os.system(self.options['reload'])

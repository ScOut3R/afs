import subprocess
import os
from subprocess import CalledProcessError
from afs.errors import Error

__all__ = [ "dhcp", "dns", "radius", "shorewall" ]

class ServiceBase(object):
	
	def __init__(self, config):
		self.network = config.network
		self.options = config.options[self.__class__.__name__.lower()]

	def reload_service(self):
		try:
			subprocess.check_call(self.options['reload'].split(), stdout=open(os.devnull, 'w'))
		except CalledProcessError:
			raise Error("Reload of %s returned with error!" % self.__class__.__name__)

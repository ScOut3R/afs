from __init__ import ServiceBase

class SHOREWALL(ServiceBase):
	
		def maclist(self):
			output = open(self.options['maclist']['configfile'], "w")
			
			for host in sorted(self.network.keys()):
				template = "ACCEPT\t%s\t%s\t%s\t#%s\n" % ( self.options['maclist']['interface'], self.network[host]['mac'], self.network[host]['ip'], host)
				output.write(template)
			
			output.close()
			
		def generate(self):
			if self.options.has_key('maclist'):
				self.maclist()

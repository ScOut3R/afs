from __init__ import ServiceBase

class RADIUS(ServiceBase):
		
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

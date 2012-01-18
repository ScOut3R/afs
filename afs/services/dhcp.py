from __init__ import ServiceBase

class DHCP(ServiceBase):
		
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

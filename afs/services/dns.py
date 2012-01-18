from __init__ import ServiceBase

class DNS(ServiceBase):
	
	def __init__(self, config):
		super(self.__class__, self).__init__(config)
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

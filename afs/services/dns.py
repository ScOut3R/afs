from __init__ import ServiceBase
import time

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
		
		serial = int(time.time())
		
		for zonefile in [ self.options['forward-master-zone-file'], self.options['reverse-master-zone-file'] ]:
			
			master_file = open(zonefile, 'r')
			master_content = master_file.readlines()
			master_file.close()
		
			master_content[2] = "\t\t\t%i\t;serial number\n" % serial

			master_file = open(zonefile, 'r+')
			master_file.writelines(master_content)
			master_file.close()

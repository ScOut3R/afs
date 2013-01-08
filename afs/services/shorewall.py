from __init__ import ServiceBase
import yaml

class SHOREWALL(ServiceBase):
	
		def maclist(self):
			output = open(self.options['maclist']['configfile'], "w")
			
			for host in sorted(self.network.keys()):
				template = "ACCEPT\t%s\t%s\t%s\t#%s\n" % ( self.options['maclist']['interface'], self.network[host]['mac'], self.network[host]['ip'], host)
				output.write(template)
			
			output.close()
			
		def groups(self):
			groupsfile = open(self.options['groups']['config'], "r")
			groups = yaml.load(groupsfile)
			groupsfile.close()	
	
			if self.options['groups']['manage-actions'] == True:
				output_actions = open(self.options['groups']['actions-file'], "w")
				
			for group in sorted(groups):
				
				if self.options['groups']['manage-actions'] == True:
					template = "%s\n" % group
					output_actions.write(template)
				
				output = open("%s%s.actions" % ( self.options['groups']['actions-path'], group ), "w")
				
				for ip in sorted(groups[group]['ips']):
					template = "%s\t%s\n" % ( groups[group]['policy'], ip )
					output.write(template)
				
				output.close()
			if self.options['groups']['manage-actions'] == True:
				output_actions.close()

		def generate(self):
			if self.options.has_key('maclist'):
				self.maclist()
			if self.options.has_key('groups'):
				self.groups()

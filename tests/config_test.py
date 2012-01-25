import unittest
import yaml
from afs.config import Config
from afs.errors import Error

class ValidateTest(unittest.TestCase):
	
	def setUp(self):
		self.network = yaml.load("""
notebook-lan:
 ip: 192.168.0.1
 mac: 00:00:00:00:00:88
 host: notebook

notebook-wifi:
 ip: 192.168.0.1
 mac: 00:00:00:00:00:87
 host: notebook
 radius: 1""")
		
		self.network2 = yaml.load("""
notebook-lan:
 ip: 192.168.0.1
 mac: 00:00:00:00:00:88
 host: notebook

notebook-wifi:
 ip: 192.168.0.2
 mac: 00:00:00:00:00:87
 host: notebook
 radius: 1""")
		
		self.network3 = yaml.load("""
notebook-lan:
 ip: 192.168.0.1
 mac: 00:00:00:00:00:88
 host: notebook""")
		
		self.network4 = yaml.load("""
notebook-lan:
 ip: 192.168.0.256
 mac: 00:00:00:00:00:88
 host: notebook""")
		
		self.network5 = yaml.load("""
notebook-lan:
 ip: 192.168.0.a
 mac: 00:00:00:00:00:88
 host: notebook""")

	def test_hostname_duplication(self):
		config = Config("", self.network, "")
		try:
			config.validate_hostname()
		except Error as e:
			self.fail('Unexpected exception: %s' % e.msg)
		config = Config("", self.network2, "")
		try:
			config.validate_hostname()
		except Error:
			pass
		else:
			self.fail('Unexpected exception')
	
	def test_ip_duplication(self):
		config = Config("", self.network, "")
		try:
			config.validate_ip()
		except Error as e:
			self.fail("Unexpected exception: %s" % e.msg)
		
		config = Config("", self.network2, "")
		try:
			config.validate_ip()
		except Error as e:
			self.fail("Unexpected exception: %s" % e.msg)

	def test_ip_format(self):
		config = Config("", self.network3, "")
		try:
			config.validate_ip()
		except Error as e:
			self.fail("Unexpected exception: %s" % e.msg)
		
		config = Config("", self.network4, "")
		try:
			config.validate_ip()
		except Error:
			pass
		else:
			self.fail("Unexpected exception")
		
		config = Config("", self.network5, "")
		try:
			config.validate_ip()
		except Error:
			pass
		else:
			self.fail("Unexpected exception")

if __name__ == "__main__":
	unittest.main()

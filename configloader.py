import configparser


class ConfigLoader(configparser.ConfigParser):

	def __init__(self, cfgfile=""):
		super(configparser.ConfigParser, self).__init__()

		self.username = ""
		self.password = ""
		self.client_id = ""
		self.client_secret = ""
		self.user_agent = ""

		if cfgfile:
			self.read(cfgfile)

	def read(self, filename):
		super(configparser.ConfigParser, self).read(filename)
		self.username = self["CREDENTIALS"]["Username"]
		self.password = self["CREDENTIALS"]["Password"]
		self.client_id = self["AUTH"]["ClientID"]
		self.client_secret = self["AUTH"]["Secret"]
		self.user_agent = self["AUTH"]["UserAgent"]



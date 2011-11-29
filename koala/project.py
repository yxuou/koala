import json

class ProjectFile(object):

	def __init__(self, path="build.json"):
		self.file = open(path)
		self.json = json.load(self.file)

	def __del__(self):
		self.file.close()

	def load_into(self, obj):
		for attr in self.json:
			obj[attr] = self.json[attr]


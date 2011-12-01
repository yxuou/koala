import json
import os

from koala.base import StoreObject
from koala.util import list_files

class Project(StoreObject):

	Defaults = {
		"name" : "a.out", 
		"bin-dir" : "./", 
		"src-dir" : "./"
	}

	def __init__(self):
		super(Project, self).__init__()

		# Initialize default values
		self.update(Project.Defaults)

	def load_from_file(self, path):
		file = open(path)
		self.load_from_object(json.load(file))
		file.close()

	# Loads project fields from an object which supports access through keys
	def load_from_object(self, object):
		self.update(object)

	def load_sources (self):
		self["src-files"] = list_files(self["src-dir"], extension=".vala")


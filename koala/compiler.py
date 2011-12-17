import subprocess
import re
import os

from koala.base import *

class Compiler(ReactiveObject):

	def __init__(self):
		super(Compiler, self).__init__()

		self.register_signal("started")
		self.register_signal("finished")

	def run(self, project):
		self.emit_signal("started")

		if hasattr(self, "do_run"):
			self.do_run(project)
		else:
			raise NotImplementedError()

		self.emit_signal("finished")

	def get_output(self):
		raise NotImplementedError()

	def has_errors(self):
		raise NotImplementedError()

	def __str__(self):
		return self.__class__.__name__

class ValaCompiler(Compiler):

	translator = {
		"name"      : lambda s : "--output=%s" %(s),
		"bin-dir"   : lambda s : "--directory=%s" %(s),
		"packages"  : lambda l : ("--pkg=" + "\t--pkg=".join(l)).split('\t'),
		"arguments" : None
	}

	def __init__(self):
		super(ValaCompiler, self).__init__()

		self.output = None
		self.errors = False

	def get_call(self, project):
		args = ["valac", "--quiet"]

		for prop in project:
			argument = self.property_to_argument (prop, project[prop])
			if argument != None:
				if type(argument) is list:
					args.extend(argument)
				else:
					args.append(argument)

		args.extend(project["src-files"])

		return args

	def property_to_argument (self, name, value):
		if not name in self.translator:
			return None

		translator = self.translator[name]

		if translator == None:
			return value
		else:
			return self.translator[name](value)

	def do_run(self, project):
		call = self.get_call(project)

		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		proc.wait()

		self.errors = (proc.returncode != 0)
		self.output = proc.stdout

	def has_errors(self):
		return self.errors

	def get_output(self):
		return self.output


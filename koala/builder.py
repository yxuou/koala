import os

from koala.util import list_files
from koala.base import ReactiveObject

from koala.compiler import ValaCompiler, MakefileCompiler

class Builder(ReactiveObject):

	def __init__(self):
		super(Builder, self).__init__()

		self.register_signal("build-started")
		self.register_signal("build-finished")

		# Use these ase default values
		self.set_key("name", "a.out")
		self.set_key("bin-dir", "./")
		self.set_key("src-dir", "./")

		self.compiler = None

	def set_compiler (self, compiler):
		self.compiler = compiler

	def get_compiler (self):
		return self.compiler

	def load_sources (self):
		directory = self["src-dir"]

		assert directory != None
		assert os.path.isdir(directory)

		result = list_files(directory, extension=".vala")
		assert len(result) > 0

		self.set_key("src-files", result)

	def build(self):
		self.load_sources()

		self.emit_signal("build-started")
		try:
			compiler = self.get_compiler()
			compiler.run(self)
		except Exception, e:
			print "Error: Exception occured during compilation: %s." %(e)

		self.emit_signal("build-finished")

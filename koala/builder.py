import os

from koala.base import ReactiveObject
from koala.util import list_files

class Builder(ReactiveObject):

	def __init__(self):
		super(Builder, self).__init__()

		self.register_signal("started")
		self.register_signal("finished")

	def set_compiler (self, compiler):
		self.compiler = compiler

	def get_compiler (self):
		if not hasattr(self, "compiler"):
			raise NotImplementedError()

		return self.compiler

	def build(self, project):
		project.load_sources()

		self.emit_signal("started", project)

		compiler = self.get_compiler()
		compiler.run(project)

		self.emit_signal("finished")


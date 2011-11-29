import subprocess
import re
import os

from koala.base import *

class Compiler(ReactiveObject):

	def __init__(self):
		super(Compiler, self).__init__()

		self.messages = None

		self.register_signal("compilation-started")
		self.register_signal("compilation-finished")
		self.register_signal("output-written")

	def run(self, properties):
		self.emit_signal("compilation-started")

		if self.messages != None:
			self.messages.clear_messages()

		if hasattr(self, "do_run"):
			self.do_run(properties)
		else:
			raise NotImplementedError()

		self.emit_signal("compilation-finished")

	def get_messages(self):
		if self.messages == None:
			raise NotImplementedError()

		return self.messages

	def has_errors(self):
		raise NotImplementedError()

class CompilerMessages(ReactiveObject):

	def __init__(self):
		super(CompilerMessages, self).__init__()

		self.register_signal("message-found")

	def add_message(self, type, message):
		if not type in self:
			self[type] = []

		self[type].append(message)
		self.emit_signal("message-found", message, type)

	def get_messages(self, type):
		return self[type]

	def clear_messages(self):
		self.clear()

	def get_types(self):
		return self.__iter__()


class ValaCompiler(Compiler):

	translator = {
		"name"     : lambda s : "--output=%s" %(s),
		"bin-dir"  : lambda s : "--directory=%s" %(s),
		"packages" : lambda l : ("--pkg=" + "\t--pkg=".join(l)).split('\t')
	}

	def __init__(self):
		super(ValaCompiler, self).__init__()

		self.messages = ValaCompilerMessages()
		self.errors = False

	def get_call(self, properties):
		args = ["valac"]

		for prop in properties:
			argument = self.property_to_argument (prop, properties[prop])
			if argument != None:
				if type(argument) is list:
					args.extend(argument)
				else:
					args.append(argument)

		args.extend(properties["src-files"])

		return args

	def property_to_argument (self, name, value):
		if name in self.translator:
			return self.translator[name](value)

		return None

	def do_run(self, properties):
		call = self.get_call(properties)
		proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.wait()

		self.messages.add_messages (proc.stderr)
		self.errors = (proc.returncode != 0)

		if not self.errors:
			path = os.path.join(properties["bin-dir"], properties["name"])
			self.emit_signal("output-written", path)

	def get_messages(self):
		return self.messages

	def has_errors(self):
		return self.errors

class MakefileCompiler(ValaCompiler):
	
	def __init__(self):
		super(MakefileCompiler, self).__init__()
		self.messages = CompilerMessages()

	def do_run(self, properties):
		call = self.get_call(properties)

		prog = call[0]
		args = call[1:]

		try:
			file = open("Makefile", "w")

			file.write("all:\n")
			file.write("\t%s" %(prog))
		
			if len(args) > 0:
				file.write(" \\")
			file.write("\n")

			for arg in args:
				file.write("\t\t%s \\\n" %(arg))

			file.close()

		except IOError, e:
			self.messages.add_message("error", "%s: %s" %(e.filename, e.strerror))
			return
		except Exception, e:
			self.messages.add_message("error", e.__str__())
			return

		self.emit_signal("output-written", "Makefile")

	def has_errors(self):
		return len(self.messages) != 0

class ValaCompilerMessages(CompilerMessages):

	MessageRegex = re.compile("(\s*(.*)\:(\d+).*\:\s*){0,1}(.*)\:\s*(.*)")

	def __init__(self):
		super(ValaCompilerMessages, self).__init__()

	def add_messages (self, stream):
		for line in stream.readlines():
			self.parse_line(line)
		stream.close()

	def parse_line(self, text):
		match = re.match(ValaCompilerMessages.MessageRegex, text)

		if match == None:
			return

		# Skip first group of match.groups(), because it's just the combination 
		# of the second and third group.
		file, line, type, text  = match.groups()[1:]

		if file != None:
			message = "%s.%s: %s" %(file, line, text)
		else:
			message = text

		self.add_message(type, message)



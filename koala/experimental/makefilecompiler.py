
from koala.compiler import ValaCompiler, CompilerMessages

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
			self.messages.add_message("error", str(e))
			return

		self.emit_signal("output-written", "Makefile")

	def has_errors(self):
		return len(self.messages) != 0


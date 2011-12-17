
from koala.compiler import ValaCompiler

class MakefileCompiler(ValaCompiler):
	
	def __init__(self):
		super(MakefileCompiler, self).__init__()

	def do_run(self, properties):
		call = self.get_call(properties)

		prog = call[0]
		args = call[1:]

		self.errors = False
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
		except:
			self.errors = True
	
	def has_errors(self):
		return self.errors


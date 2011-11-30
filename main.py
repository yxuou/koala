#!/usr/bin/env python
#
# Koala
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import koala

from koala.project import ProjectFile
from koala.builder import Builder
from koala.compiler import ValaCompiler
from koala.util import *

def on_build_started(sender, udata=None):
	print "Building %s from source(s):" %(builder["name"])
	for file in builder["src-files"]:
		print " >", file

def on_output_written(sender, output, udata=None):
	print "%d bytes written to %s." %(os.path.getsize(output), output)

if __name__ == "__main__":
	print "%s %d.%d\n" %(koala.program.capitalize(), koala.version[0], koala.version[1])

	builder = Builder()
	builder.connect_signal("build-started", on_build_started)

	if os.path.exists("build.json"):
		try:
			project = ProjectFile()
			project.load_into(builder)
		except Exception, e:
			print "Loading 'build.json' failed:", str(e)
			exit(1)

	compiler = ValaCompiler()
	compiler.connect_signal("output-written", on_output_written)
	
	builder.set_compiler(compiler)
	builder.build()
	
	messages = compiler.get_messages()
	for message_type in messages.get_types():
		print "\nGot the following %s(s):" %(message_type)
		for message in messages.get_messages(message_type):
			print " >", message

	if compiler.has_errors():
		print "\nCompilation failed."
		exit(1)	
	else:
		print "\nCompilation succeeded."

#!/usr/bin/env python
#
# Koala
#   A small build tool for Vala projects.
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

from koala.project import Project
from koala.builder import Builder
from koala.compiler import ValaCompiler
from koala.util import *

def on_build_started(builder, project, udata=None):
	print "Building %s from source(s):" %(project["name"])
	for file in project["src-files"]:
		print " >", file
	print ""

def on_build_finished(builder, udata=None):
	compiler = builder.get_compiler()

	try:
		output = compiler.get_output()
		for line in output:
			print line.strip()
		output.close()
	except:
		pass

	if compiler.has_errors():
		print "\nCompilation failed."
		exit(1)	
	else:
		print "\nCompilation succeeded."

if __name__ == "__main__":
	print "%s\n" %(koala.program_version)

	builder = Builder()
	builder.set_compiler(ValaCompiler())

	builder.connect_signal("started", on_build_started)
	builder.connect_signal("finished", on_build_finished)

	project = Project()
	if os.path.exists("build.json"):
		try:
			project.load_from_file("build.json")
		except Exception, e:
			print "Loading 'build.json' failed:", str(e)
			exit(1)

	try:
		builder.build(project)
	except Exception, e:
		print "Building project failed:", str(e)


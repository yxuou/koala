import os
import re
import xdg.BaseDirectory

import koala

def list_files(directory, extension=None):
	result = []
	for basename in os.listdir(directory):
		path = os.path.join(directory, basename)

		if os.path.isdir(path):
			result.extend(list_files(path, extension))
		else:
			if extension != None:
				name, ext = os.path.splitext(basename)
				if extension == ext:
					result.append(path)
			else:
				result.append(path)
	return result

def list_directories(directory, pattern=None):
	if pattern != None:
		regex = re.compile(pattern)

	result = []
	for basename in os.listdir(directory):
		path = os.path.join(directory, basename)

		if os.path.isdir(path):
			if pattern == None:
				result.append(path)
			else:
				if re.match(regex, basename) != None:
					result.append(path)

	return result

def get_config_directory():
	return xdg.BaseDirectory.save_config_path(koala.program)

def get_vapi_directories():
	regex = "^vala(\-[\d\.]+){0,1}$"

	result = []
	for vala_dir in list_directories("/usr/share", regex):
		vapi_dir = os.path.join(vala_dir, "vapi")

		if os.path.isdir(vapi_dir):
			result.append(vapi_dir)

	return result


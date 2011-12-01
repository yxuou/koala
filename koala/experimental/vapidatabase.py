#!/usr/bin/env python
import os
import re
import xapian

import Crypto.Hash.MD4

from koala.util import get_config_directory, get_vapi_directories, list_files

def unify(value):
	hash = Crypto.Hash.MD4.new()
	hash.update(value)
	return hash.hexdigest()

class XapianDatabase(xapian.WritableDatabase):

	def __init__(self, path):
		super(XapianDatabase, self).__init__(path, xapian.DB_CREATE_OR_OPEN)

		self.indexer = xapian.TermGenerator()
		self.stemmer = xapian.Stem("english")
		self.indexer.set_stemmer(self.stemmer)

		self.query_parser = xapian.QueryParser()
		self.query_parser.set_stemmer(self.stemmer)
		self.query_parser.set_database(self)

		self.enquire = xapian.Enquire(self)

	def execute(self, query, offset=0, limit=10):
		if type(query) is str:
			query = self.query_parser.parse_query(query)

		self.enquire.set_query(query)
		return self.enquire.get_mset(offset, limit)

	def index(self, document):
		self.indexer.set_document(document)
		self.indexer.index_text(document.get_data())
		self.add_document(document)

class VapiDatabase(XapianDatabase):

	Path = os.path.join(get_config_directory(), "vapi.cache")

	def __init__(self):
		super(VapiDatabase, self).__init__(VapiDatabase.Path)

		for name in VapiDocument.Prefixes:
			self.query_parser.add_prefix(name,  VapiDocument.Prefixes[name])

		self.index_vapi_directories ()

	def index_vapi_directories (self):
		for directory in get_vapi_directories():
			for file in list_files(directory, ".vapi"):
				if not self.contains_value("path", file):
					self.index_vapi(file)

	def index_vapi(self, path):
		self.index(VapiDocument(path))

	def contains_value(self, value, data):
		match = self.execute('%s:"%s"' %(value, unify(data)), limit=1)
		return match.size() != 0

	def lookup_namespace (self, namespace):
		if type(namespace) is list:
			query = " ".join(namespace)
		else:
			query = namespace.replace(".", " ")

		matches = self.execute (query, limit=20)

		results = []
		for match in matches:
			results.append(match.document.get_value(VapiDocument.Values["name"]))

		return results

class VapiDocument(xapian.Document):

	Values = {
		"name" : 0,
		"path" : 1
	}

	Prefixes = {
		"name" : "XNAME",
		"path" : "XPATH"
	}

	Pattern = re.compile("\s*namespace\s+(\w+(\.\w+)*)")

	def __init__(self, path):
		super(VapiDocument, self).__init__()

		self.load(path)

	def get_value_prefix(self, name):
		return VapiDocument.Prefixes[name]

	def get_value_index(self, name):
		return VapiDocument.Values[name]

	def get_value_by_name (self, name):
		return self.get_value(self.Values[name])

	def set_value_by_name (self, name, data):
		self.add_term(self.get_value_prefix(name) + unify(data))
		self.add_value(self.get_value_index(name), data)

	def set_path(self, path):
		self.set_value_by_name ("path", path)

		base = os.path.basename(path)
		name = os.path.splitext(base)[0]
		self.set_value_by_name ("name", name)

	def detect_namespace_in_line (self, text):
		match = re.match(VapiDocument.Pattern, text)

		if match == None:
			return None

		return match.groups()[0]		

	def load (self, path):
		assert os.path.exists(path)

		namespaces = []
		
		stream = open(path)
		for line in stream.readlines():
			match = self.detect_namespace_in_line (line)
			if match != None and not match in namespaces:
				namespaces.append(match)
		stream.close()

		self.set_data (" ".join(namespaces))
		self.set_path (path)

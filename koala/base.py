
class StoreObject(object):

	def __init__(self):
		self.__data = {}

	def set_key(self, key, value):
		self.__data[key] = value

	def get_key(self, key):
		return self.__data[key]

	def has_key(self, key):
		return key in self.__data

	def count(self):
		return len(self.__data)

	def clear(self):
		self.__data = {}

	def __getitem__(self, key):
		return self.get_key(key)

	def __setitem__(self, key, value):
		return self.set_key(key, value)

	def __contains__(self, key):
		return self.has_key(key)

	def __len__(self):
		return self.count()

	def __iter__(self):
		return iter(self.__data)

class ReactiveObject(StoreObject):
	
	def __init__(self):
		super(ReactiveObject, self).__init__()
		self.__events = {}

	def register_signal(self, event):
		self.__events[event] = []

	def connect_signal(self, event, handler, udata=None):
		self.__events[event].append((handler, udata))

	def emit_signal(self, event, *args):

		for handler in self.__events[event]:
			func, udata = handler

			args_list = list(args)
			if udata != None:
				args_list.append(udata)

			func(self, *tuple(args_list))


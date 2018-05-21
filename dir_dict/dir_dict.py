import os
import collections
import subprocess

class DirDict(collections.MutableMapping):
	def __init__(self, path):
		self._path = path

	def __len__(self):
		return len(os.listdir(self._path))

	def __getitem__(self, file):
		full_path = self._path + '/' + file
		f = open(full_path, 'r')
		buf = f.read()
		f.close()
		return buf


	def __setitem__(self, file, string):
		full_path = self._path + '/' + file
		print(full_path)
		f = open(full_path, 'w')
		f.write(string)
		f.close()

	def __delitem__(self, file):
		if str(file) not in os.listdir(self._path):
			raise KeyError(str(file))
		subprocess.call(['rm', os.path.join(self._path, str(file))])

	def __iter__(self):
		return iter(os.listdir(self._path))

	def __bool__(self):
		return self.__len__() > 0
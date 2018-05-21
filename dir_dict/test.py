from dir_dict import DirDict
from unittest import TestCase

class DirDictTests(TestCase):
	def test_add(self):
		p = DirDict("/tmp/dirdict")
		self.assertEqual(0, len(p))
		self.assertFalse(p)
		p['file'] = 'somestring\n'
		self.assertEqual(1, len(p))
		self.assertEqual('somestring\n', p['file'])
		del p['file']
		self.assertEqual(0, len(p))
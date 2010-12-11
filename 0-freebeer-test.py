import unittest
import p6

class P6Tester(unittest.TestCase):
	def test_freebeer(self):
		freebeers = '1 2 free 4 beer free 7 8 free beer 11 free 13 14 freebeer'
		self.assertEqual(freebeers, p6.freebeer(15))	


if __name__ == "__main__":
	unittest.main()

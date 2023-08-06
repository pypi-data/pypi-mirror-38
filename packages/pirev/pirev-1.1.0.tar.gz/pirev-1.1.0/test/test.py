import unittest
from pirev.pirev import getInfo

def testDataPath(filename):
  return f'test/data/{filename}'

CPUINFO_PI1 = testDataPath('cpuinfo_pi1')
CPUINFO_PI3 = testDataPath('cpuinfo_pi3')
CPUINFO_MBP = testDataPath('cpuinfo_mbp')
MISSING_FILE = testDataPath('missing')

class TestGetInfo(unittest.TestCase):
  
  def test_cpuinfo_pi1(self):
    info = getInfo(CPUINFO_PI1)

    self.assertEqual(info['revision'], {
      'type': 'B',
      'memory': '512 MB',
      'processor': 'BCM2835',
      'revision': 2,
      'manufacturer': 'Sony UK',
      'code': '000e',
    })
  
  def test_cpuinfo_pi3(self):
    info = getInfo(CPUINFO_PI3)

    self.assertEqual(info['revision'], {
      'type': '3B',
      'memory': '1 GB',
      'processor': 'BCM2837',
      'revision': 2,
      'manufacturer': 'Embest',
      'code': 'a22082',
    })
  
  def test_cpuinfo_mbp(self):
    with self.assertRaises(ReferenceError):
      getInfo(CPUINFO_MBP)
  
  def test_missing_file(self):
    with self.assertRaises(FileNotFoundError):
      getInfo(MISSING_FILE)

if __name__ == '__main__':
    unittest.main()

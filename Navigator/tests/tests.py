import unittest
from clases import *
from sql import *
from way_builder_class import *


class GetID(unittest.TestCase):
   def test_check_keys(self):
        assert_mas=[
            ['11',1],
            ['25',16],
            ['24',15]
        ]
        for name, key in assert_mas:
            self.assertEqual(get_id(name), key)






suite = unittest.defaultTestLoader.loadTestsFromTestCase(GetID)
unittest.TextTestRunner().run(suite)

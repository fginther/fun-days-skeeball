import unittest

import cortex

class TestOperationModes(unittest.TestCase):
    def test_attract(self):
        assert cortex.OperationMode.ATTRACT == 'ATTRACT'
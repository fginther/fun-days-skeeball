import mock
import unittest

import machine
import fake_gpio


class TestMachine(unittest.TestCase):

    def test_init(self):
        gpio = fake_gpio.FakeGPIO()
        assert gpio.mode is None
        assert gpio.warnings is None
        m = machine.Machine(gpio=gpio)
        assert gpio.mode == gpio.BCM
        assert not gpio.warnings
        assert len(m.triggers) == 0

    def test_create_trigger(self):
        gpio = fake_gpio.FakeGPIO()
        m = machine.Machine(gpio=gpio)
        assert len(m.triggers) == 0
        event = mock.Mock()
        m.create_trigger('test', 1, event)
        assert len(m.triggers) == 1

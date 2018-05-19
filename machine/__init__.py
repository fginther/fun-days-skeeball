'''Receive GPIO machine inputs.'''
import logging
import pygame

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    # This module can't be imported, assume running in test context
    GPIO = None

DEFAULT_BOUNCETIME = 1000


class Machine(object):
    '''The arcade machine backend.'''
    BASE_PIN = 20

    def __init__(self, gpio=GPIO):
        '''Initialize the machine.'''
        self.gpio = gpio
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log(logging.INFO, 'Machine setup begin.')
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setwarnings(False)
        self.log(logging.INFO, 'Machine setup complete.')
        self.triggers = []

    def log(self, level, msg):
        '''Machine specific event logger.'''
        self.logger.log(level, msg)

    def create_trigger(self, name, target, event_number, sub_event):
        pin = self.BASE_PIN + target
        event = pygame.event.Event(event_number, sub=sub_event)
        trigger = Trigger(self.gpio, self.logger, name, pin, event)
        self.triggers.append(trigger)
        return trigger

    def release_balls(self):
        '''Activate the servo to release the balls'''
        pass

    def hold_balls(self):
        '''Activate the servo to hold the balls'''
        pass


class Trigger(object):
    '''An input trigger.'''

    def __init__(self, gpio, logger, name, pin, event,
                 bouncetime=DEFAULT_BOUNCETIME):
        '''Initialize the GPIO trigger.'''
        self.gpio = gpio
        self.logger = logger
        self.name = name
        self.pin = pin
        self.event = event
        self.gpio.setup(pin, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.add_event_detect(
            pin, self.gpio.FALLING, callback=self.callback,
            bouncetime=bouncetime)
        self.log(logging.INFO, 'Configuring {} on pin {}.'.format(name, pin))

    def __repr__(self):
        return '[name: {}, pin: {}, event: {}]'.format(
            self.name, self.pin, self.event)

    def log(self, level, msg):
        '''Trigger specific event logger.'''
        self.logger.log(level, msg)

    def callback(self):
        '''GPIO event callback.'''
        self.log(logging.INFO, 'GPIO callback: {}'.format(self.name))
        self.log(logging.INFO, 'Event: {}'.format(self.event))
        pygame.event.post(self.event)

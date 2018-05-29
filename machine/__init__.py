'''Receive GPIO machine inputs.'''
import logging
import time

import pygame

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    # This module can't be imported, assume running in test context
    import tests.fake_gpio
    GPIO = tests.fake_gpio.FakeGPIO()

DEFAULT_BOUNCETIME = 2000


class Machine(object):
    '''The arcade machine backend.'''
    BASE_PIN = 20
    SERVO_PIN = 12

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
        #self.duty_time = 0
        #self.gpio.setup(self.SERVO_PIN, self.gpio.OUT)
        #self.pwm = self.gpio.PWM(self.SERVO_PIN, 50)
        self.log(logging.INFO, 'GPIO: {}'.format(self.gpio))

    def log(self, level, msg):
        '''Machine specific event logger.'''
        self.logger.log(level, msg)

    def create_trigger(self, name, target, event_number, sub_event):
        pin = self.BASE_PIN + target
        event = pygame.event.Event(event_number, sub=sub_event)
        trigger = Trigger(self.gpio, self.logger, name, pin, event)
        self.triggers.append(trigger)
        return trigger

    def get_current_time(self):
        return int(round(time.time() * 1000))

    # The servo control is untested
    def check_duty_cycle(self):
        return
        now = self.get_current_time()
        if self.duty_time + 1000 > now:
            self.turn_off_duty_cycle()
            self.duty_time = 0

    def turn_off_duty_cycle(self):
        return
        self.gpio.output(self.SERVO_PIN, False)
        self.pwm.ChangeDutyCycle(0)

    def set_angle(self, angle):
        '''Sets the angle of the servo motor.'''
        duty = angle / 18 + 2
        self.gpio.output(self.SERVO_PIN, True)
        self.pwm.ChangeDutyCycle(duty)

    def release_balls(self):
        '''Activate the servo to release the balls'''
        return
        self.set_angle(90)
        self.duty_time = self.get_current_time()

    def hold_balls(self):
        '''Activate the servo to hold the balls'''
        return
        self.set_angle(0)
        self.duty_time = self.get_current_time()


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
        self.bouncetime = bouncetime
        self.latched = False
        self.latch_time = 0
        self.gpio.setup(pin, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.log(logging.INFO, 'Configuring {} on pin {}.'.format(name, pin))

    def __repr__(self):
        return '[name: {}, pin: {}, event: {}]'.format(
            self.name, self.pin, self.event)

    def log(self, level, msg):
        '''Trigger specific event logger.'''
        self.logger.log(level, msg)

    def get_current_time(self):
        return int(round(time.time() * 1000))

    def poll(self):
        '''Poll the status of this target.'''
        state = GPIO.input(self.pin)
        now = self.get_current_time()

        # Perform debouncing by ensuring this does not trigger again until
        # after the bouncetime
        if self.latch_time + self.bouncetime > now:
            return

        # The target must also be clear for a minimum time before it can
        # be triggered again
        if self.latched and state == 1:
            self.latched = False
            return

        if state == 0:
            self.latched = True
            self.latch_time = now
            pygame.event.post(self.event)

    def callback(self, data):
        '''GPIO event callback.'''
        self.log(logging.INFO, 'GPIO callback: {}'.format(self.name))
        self.log(logging.INFO, 'Event: {}'.format(self.event))
        self.log(logging.INFO, 'Data: {}'.format(data))
        pygame.event.post(self.event)

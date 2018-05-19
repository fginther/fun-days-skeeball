'''
Cortex is the event handler and dispatcher.
'''
import logging
import machine
import game
from tests import fake_gpio

import pygame
import time

class OperationMode(object):
    '''
    Enumerates the possible operating modes.
    '''
    ATTRACT = 'ATTRACT'
    PLAY = 'PLAY'
    POST_PLAY = 'POST_PLAY'
    SHUTDOWN = 'SHUTDOWN'

class Cortex(object):
    # XXX: This constants need to go somewhere else
    POST_PLAY_TIMEOUT = None
    LAST_BALL = None
    TARGET_EVENT = pygame.USEREVENT
    START_EVENT = pygame.USEREVENT + 1
    
    def __init__(self):
        '''Initialize the Cortex.'''
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.mode = OperationMode.ATTRACT
        self.game = game.Game()
        self.machine = machine.Machine(fake_gpio.FakeGPIO())

        # Configure the targets and their event handlers
        self.targets = []
        for target in self.game.targets:
            value = self.game.targets[target]
            self.log(logging.INFO, 'target: {} - {}'.format(target, value))
            event = self.TARGET_EVENT
            sub_event = (target, value)
            self.targets.append(self.machine.create_trigger('target {}'.format(target), target, event, sub_event))
            # XXX: Create a mapping of pygame.events to target objects
            # This will allow the event handler to lookup the target based on event
        self.log(logging.INFO, 'Cortex target list:')
        self.log(logging.INFO, self.targets)

        start_event = self.START_EVENT
        self.start_button = self.machine.create_trigger('start', -1, start_event, 0)
        self.log(logging.INFO, 'start_button: {}'.format(self.start_button))
        pygame.init()

    def log(self, level, msg):
        '''Cortex specific event logger.'''
        self.logger.log(level, '{}: {}'.format(self.mode, msg))

    def get_current_time(self):
        return int(round(time.time() * 1000))

    def play(self):
        '''Starts a new play of the currently selected game.'''
        # Display the new game screen
        # Release the balls
        self.log(logging.INFO, 'play triggered')
        self.mode = OperationMode.PLAY
        self.machine.release_balls()
        self.machine.hold_balls()

    def post_play(self):
        '''Start the post play period, presenting the last score.'''
        # Display current score
        # Display current ranking
        pass

    def attract(self):
        '''Start attracting players to play a new game.'''
        # Display game attraction graphics
        # Display high scores
        pass

    def hit_target(self, event):
        '''Handler for processing target events.'''
        # Lookup the event in a game table
        # Increment the score by the value
        self.game.drop_ball(event.sub[0])
        points = event.sub[1]
        self.log(logging.INFO, 'Points: {}'.format(points))
        self.log(logging.INFO, 'Score: {}'.format(self.game.score))
        if self.game.check_game_over():
            self.mode = OperationMode.POST_PLAY
        return

    def event_loop(self):
        '''The pygame event loop.'''
        # Start the event loop
        self.log(logging.INFO, 'Starting event loop')
        while True: 
            current_time = self.get_current_time()

            for event in pygame.event.get():
                # Process global events first
                self.log(logging.INFO, 'New event: {}'.format(event))
                if event.type == pygame.QUIT:
                    self.log(logging.WARNING, 'QUITing the event loop')
                    return
                if event.type == pygame.KEYDOWN:
                    self.log(logging.INFO, 'Event key: {}'.format(event.key))
                    if event.key == ord(' '):
                        self.start_button.callback()
                        continue
                    if event.key > ord('9'):
                        return
                    if event.key < ord('0'):
                        return
                    event_no = event.key - ord('0')
                    self.targets[event_no].callback()
                    continue
                if event.type == pygame.KEYUP:
                    continue
                if event.type == self.START_EVENT:
                    self.log(logging.INFO, 'START_BUTTON TRIGGERED')

                # Process events per specific mode
                if self.mode == OperationMode.ATTRACT:
                    if event.type == self.START_EVENT:
                        self.play()
                        continue
                if self.mode == OperationMode.POST_PLAY:
                    if event.type == self.START_GAME:
                        self.play()
                        continue
                    if event.type == self.POST_PLAY_TIMEOUT:
                        self.attract()
                        continue
                if self.mode == OperationMode.PLAY:
                    if event.type == self.LAST_BALL:
                        self.post_play()
                        continue
                    if event.type == self.TARGET_EVENT:
                        self.hit_target(event)
                        continue

                # Unhandled event
                self.log(logging.ERROR, 'Unhandled event: {}'.format(
                    event.type))
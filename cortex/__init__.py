'''
Cortex is the event handler and dispatcher.
'''
import logging
import display
import machine
import game

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
    TARGET_EVENT = pygame.USEREVENT
    START_EVENT = pygame.USEREVENT + 1
    END_EVENT = pygame.USEREVENT + 2
    POLL_EVENT = pygame.USEREVENT + 3

    POLL_SPEED = 100

    def __init__(self, config):
        '''Initialize the Cortex.'''
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.mode = OperationMode.ATTRACT
        self.game = game.Game()
        self.machine = machine.Machine()
        self.display = display.Display(config, False)
        self.last_target = 0
        self.last_points = 0

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
        self.end_event = pygame.event.Event(self.END_EVENT)
        self.log(logging.INFO, 'end_event: {}'.format(self.end_event))

        pygame.time.set_timer(self.POLL_EVENT, self.POLL_SPEED)
        pygame.init()

    def log(self, level, msg):
        '''Cortex specific event logger.'''
        self.logger.log(level, '{}: {}'.format(self.mode, msg))

    def get_current_time(self):
        return int(round(time.time() * 1000))

    def poll_targets(self):
        '''Poll for target events'''
        #self.log(logging.INFO, 'poll triggered')
        for target in self.targets:
            target.poll()

    def play(self):
        '''Starts a new play of the currently selected game.'''
        # Display the new game screen
        # Release the balls
        self.log(logging.INFO, 'play triggered')
        self.game.start_game()
        self.display.show_score(self.game.score, 0, 0, [])
        self.machine.release_balls()
        self.machine.hold_balls()
        self.mode = OperationMode.PLAY

    def post_play(self):
        '''Start the post play period, presenting the last score.'''
        self.log(logging.INFO, 'post_play triggered')
        bonus = []
        self.mode = OperationMode.POST_PLAY
        self.display.show_final_score(self.game.score, self.last_target,
                                      self.last_points, bonus)
        # Display current ranking
        pass

    def attract(self):
        '''Start attracting players to play a new game.'''
        # Display game attraction graphics
        # Display high scores
        pass

    def hit_target(self, event):
        '''Handler for processing target events.'''
        self.game.drop_ball(event.sub[0])
        target, points = event.sub
        self.display.show_score(self.game.score, target, points, [])
        self.log(logging.INFO, 'Points: {}'.format(points))
        self.log(logging.INFO, 'Score: {}'.format(self.game.score))
        if self.game.check_game_over():
            self.log(logging.INFO, 'Posting end_event')
            pygame.event.post(self.end_event)
        self.last_target = target
        self.last_points = points

    def event_loop(self):
        '''The pygame event loop.'''
        # Start the event loop
        self.log(logging.INFO, 'Starting event loop')
        while True: 
            current_time = self.get_current_time()

            for event in pygame.event.get():
                # Process global events first
                #self.log(logging.INFO, 'New event: {}'.format(event))
                if event.type == pygame.QUIT:
                    self.log(logging.WARNING, 'QUITing the event loop')
                    return
                if event.type == pygame.KEYDOWN:
                    self.log(logging.INFO, 'Event key: {}'.format(event.key))
                    if event.key == ord(' '):
                        self.start_button.callback(None)
                        continue
                    if event.key > ord('9'):
                        return
                    if event.key < ord('0'):
                        return
                    event_no = event.key - ord('0')
                    self.targets[event_no].callback(None)
                    continue
                if event.type == pygame.KEYUP:
                    continue
                if event.type == self.START_EVENT:
                    self.log(logging.INFO, 'START_BUTTON TRIGGERED')
                if event.type == self.POLL_EVENT:
                    self.poll_targets()

                # Process events per specific mode
                if self.mode == OperationMode.ATTRACT:
                    if event.type == self.START_EVENT:
                        self.play()
                        continue
                if self.mode == OperationMode.POST_PLAY:
                    if event.type == self.START_EVENT:
                        self.play()
                        continue
                    if event.type == self.POST_PLAY_TIMEOUT:
                        self.attract()
                        continue
                if self.mode == OperationMode.PLAY:
                    if event.type == self.END_EVENT:
                        self.post_play()
                        continue
                    if event.type == self.TARGET_EVENT:
                        self.hit_target(event)
                        continue

                # Unhandled event
                #self.log(logging.ERROR, 'Unhandled event: {}'.format(
                #    event.type))

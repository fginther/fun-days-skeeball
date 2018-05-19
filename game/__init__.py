'''
Provides the game play mechanics.
'''
import logging

class Game(object):
    '''Scoring and mechanics for the standard skeeball game.'''
    # Create a target scoring layout
    # XXX: This should be configurable someday to support different game modes
    MIDWAY = {0: 0,
              1: 50,
              2: 100,
              3: 150,
              4: 200,
              5: 250,
              6: 300,
              7: 300,
              }

    def __init__(self):
        '''Initialize the game board.'''
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log(logging.INFO, 'Game setup begin.')
        self.targets = self.MIDWAY
        self.score = 0
        self.remaining_balls = 9
        self.game_over = False
        self.log(logging.INFO, 'Game setup complete.')

    def log(self, level, msg):
        '''Machine specific event logger.'''
        self.logger.log(level, msg)

    def get_target_value(self, target):
        '''Assigns a point total to each target and returns the value.'''
        try:
            value = self.targets[target]
        except KeyError:
            value = 0
        return value

    def drop_ball(self, target):
        '''Process common ball drop actions.'''
        self.log(logging.INFO, 'Process drop_ball target: {}'.format(target))
        value = self.get_target_value(target)
        self.score += value
        self.remaining_balls -= 1
        self.check_game_over()
        self.log(logging.INFO, 'Score is now {} ({})'.format(value, self.score))
        self.log(logging.INFO, 'Remaining balls: {}'.format(self.remaining_balls))

    def check_game_over(self):
        '''Determine if the game is over.'''
        if self.remaining_balls == 0:
            self.game_over = True
            self.log(logging.INFO, 'Game is over.')
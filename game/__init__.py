'''
Provides the game play mechanics.
'''
import logging

class Game(object):
    '''Scoring and mechanics for the standard skeeball game.'''
    def __init__(self):
        '''Initialize the game board.'''
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.log(logging.INFO, 'Game setup begin.')
        self.score = 0
        self.remaining_balls = 9
        self.game_over = False
        self.log(logging.INFO, 'Game setup complete.')

    def log(self, level, msg):
        '''Machine specific event logger.'''
        self.logger.log(level, msg)

    def target(self, target):
        '''Assigns a point total to each target and returns the value.'''
        mapping = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50,
            6: 100,
            7: 100}
        try:
            value = mapping[target]
        except KeyError:
            value = 0
        return value

    def drop_ball(self, target):
        '''Process common ball drop actions.'''
        self.log(logging.INFO, 'Process drop_ball target: {}'.format(target))
        value = self.target(target)
        self.score += value
        self.remaining_balls -= 1
        self.check_game_over()
        self.log(logging.INFO, 'Score is now {} ({})'.format(value, self.score))

    def check_game_over(self):
        '''Determine if the game is over.'''
        if self.remaining_balls == 0:
            self.game_over = True
            self.log(logging.INFO, 'Game is over.')
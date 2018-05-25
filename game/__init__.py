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
        self.start_game()
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
        if target == 0:
            # This is the special target which catches all balls
            self.remaining_balls -= 1
            self.pending_drops -= 1
            if self.pending_drops < 0:
                self.pending_drops = 0
        else:
            self.pending_drops += 1
        self.log(logging.INFO, 'Score is now {} ({})'.format(value, self.score))
        self.log(logging.INFO, 'Remaining balls: {}'.format(self.remaining_balls))
        self.log(logging.INFO, 'Pending drops: {}'.format(self.pending_drops))

    def check_game_over(self):
        '''Determine if the game is over.
        
        This will 'guess' that the game is over before the last ball passes
        the catch-all target. This is done by keeping track of the balls that
        it knows of passed the catch-all and those that have hit a scoring
        target. If these add up to the total number of balls, the game is over.

        This currently requires the balls to 'drain' into the next play area
        before the next game starts.
        '''
        if self.remaining_balls - self.pending_drops == 0:
            self.game_over = True
            self.log(logging.INFO, 'Game is over.')
            return True
        return False

    def start_game(self):
        self.score = 0
        self.remaining_balls = 9
        self.pending_drops = 0
        self.game_over = False
        self.log(logging.INFO, 'Game is ready to start.')

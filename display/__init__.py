'''
Provides the display output interface.
'''
import logging

import pygame


class Display(object):
    '''The display interface.'''
    def __init__(self, config, fullscreen=True, pygame=pygame):
        '''Initialize the display.'''
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.pygame = pygame
        self.pygame.init()

        if fullscreen:
            width, height = self.get_fullscreen_resolution()
            self.screen = self.pygame.display.set_mode(
                [width, height], self.pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((600, 600))
            pygame.display.set_caption('skeeball')
            background = pygame.Surface(self.screen.get_size())
            background = background.convert()
            background.fill((0, 0, 0))

        self.score_font = self.init_score_font()
        self.text_font = self.init_text_font()

        # Initialize the screen and background
        self.init_background()

    def blit(self, surface, position, flip=True):
        '''Render the surface and optionally flip the buffer.'''
        self.screen.blit(surface, position)
        if flip:
            self.pygame.display.flip()

    def get_fullscreen_resolution(self):
        '''Returns the maximum fullscreen resolution.'''
        modes = self.pygame.display.list_modes(0, self.pygame.FULLSCREEN)
        max_mode = modes[0]
        self.log(logging.INFO, 'Selected fullscreen mode: {}'.format(
            max_mode))
        return max_mode

    def init_background(self):
        '''Initialize the screen surface with black.'''
        background = self.pygame.Surface(self.screen.get_size())
        background.fill((0, 0, 0))
        self.blit(background, (0, 0))
        return background

    def init_score_font(self):
        '''Initialize the font used to render the current score.'''
        font_path = self.config['score_font']
        try:
            font = self.pygame.font.Font(font_path, 128)
        except IOError:
            font = self.pygame.font.SysFont('ubuntumono', 128)
        return font

    def init_text_font(self):
        font = self.pygame.font.SysFont('ubuntumono', 96)
        return font

    def log(self, level, msg):
        '''Machine specific event logger.'''
        self.logger.log(level, msg)

    def show_score(self, score, final=False):
        '''Show the current score.'''
        # Clear the background first
        background = self.pygame.Surface(self.screen.get_size())
        background.fill((0, 0, 0))
        # Blit the background surface to the screen, but don't flip it until
        # the text is drawn below
        self.blit(background, (0, 0), False)

        text = self.score_font.render(str(score), 1, (250, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        # Blit the text surface onto the screen
        self.blit(text, textpos)

        if final:
            text = self.text_font.render('Final Score', 1, (250, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 150
            self.blit(text, textpos)

    def show_final_score(self, score):
        '''Show the final score at the end of the game.'''
        self.show_score(score, True)

    def show_high_scores(self, scores):
        '''Show the list of high scores.'''
        pass

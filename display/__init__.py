'''
Provides the display output interface.
'''
import logging
from math import pi

import pygame


class Display(object):
    '''The display interface.'''

    BOARD_COLOR = (10, 240, 10)
    SCORE_COLOR = (240, 10, 10)
    SCORE_COLOR = (229, 229, 48)
    TARGET_COLOR = (180, 180, 10)

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
            self.screen = pygame.display.set_mode((1440, 900))
            pygame.display.set_caption('skeeball')
            background = pygame.Surface(self.screen.get_size())
            background = background.convert()
            background.fill((0, 0, 0))

        self.score_font = self.init_score_font()
        self.text_font = self.init_text_font()
        self.background_pattern = pygame.image.load(self.config['background'])

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
        self.blit(background, (0, 0), False)
        self.blit(self.background_pattern, (0, 0))
        return background

    def init_score_font(self):
        '''Initialize the font used to render the current score.'''
        font_path = self.config['score_font']
        try:
            font = self.pygame.font.Font(font_path, 256)
        except IOError:
            font = self.pygame.font.SysFont('helvetica', 256)
        return font

    def init_text_font(self):
        font = self.pygame.font.SysFont('helvetica', 128)
        return font

    def log(self, level, msg):
        '''Machine specific event logger.'''
        self.logger.log(level, msg)

    def show_board(self, target):
        '''Draw the game board and optionally highlight a target.'''
        size = self.screen.get_size()
        size = (size[0] / 2, size[1])
        pos = (size[0], 0)
        center_left = size[0] / 2 - 50
        center_right = center_left + 100
        targets = {0: [0, 0, 0, 0],
                   1: [center_left, 725, 100, 100],
                   2: [center_left, 600, 100, 100],
                   3: [center_left, 475, 100, 100],
                   4: [center_left, 300, 100, 100],
                   5: [center_left, 125, 100, 100],
                   6: [5, 5, 100, 100],
                   7: [size[0] - 5 - 100, 5, 100, 100]}
        arcs = [[[size[0] / 2 - 200, 300, 400, 400], 0, 2.1 * pi],
                [[0, size[0] - 615, size[0], size[0]], pi, 2 * pi]]

        board = self.pygame.Surface(size)
        pygame.draw.rect(board, self.BOARD_COLOR, [0, 0, size[0], size[1]], 3)
        for t in targets:
            if t == 0:
                continue
            color = self.BOARD_COLOR
            if t == target:
                color = self.TARGET_COLOR
            pygame.draw.ellipse(board, color, targets[t], 3)
        for a in arcs:
            pygame.draw.arc(board, self.BOARD_COLOR, a[0], a[1], a[2], 3)
        self.blit(board, pos)

    def show_score(self, score, target, points, bonus, final=False):
        '''Show the current score.'''
        # Clear the background first
        background = self.pygame.Surface(self.screen.get_size())
        background.fill((0, 0, 0))
        # Blit the background surface to the screen, but don't flip it until
        # the text is drawn below
        self.blit(background, (0, 0), False)

        self.blit(self.background_pattern, (0, 0), False)

        def render_font(font, x, y, color, content):
            offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
            for xoffset, yoffset in offsets:
                text = font.render(content, 1, (0, 0, 0))
                textpos = text.get_rect()
                textpos.centerx = x + xoffset
                textpos.centery = y + yoffset
                # Blit the text surface onto the screen
                self.blit(text, textpos)
            text = font.render(content, 1, color)
            textpos = text.get_rect()
            textpos.centerx = x
            textpos.centery = y
            # Blit the text surface onto the screen
            self.blit(text, textpos)

        text_x = background.get_rect().centerx
        text_y = background.get_rect().centery
        render_font(self.score_font, text_x, text_y, self.SCORE_COLOR,
                    str(score))

        if final:
            render_font(self.text_font, text_x, text_y - 250, self.SCORE_COLOR,
                        'Final Score')
            return
            text = self.text_font.render('Final Score', 1, self.SCORE_COLOR)
            textpos = text.get_rect()
            textpos.centerx = (background.get_rect().centerx -
                background.get_width() / 2)
            textpos.centery = background.get_rect().centery - 150
            self.log(logging.INFO, 'final score: {}, {}'.format(textpos.centerx,
                                                                textpos.centery))
            self.blit(text, textpos)

    def show_final_score(self, score, target, points, bonus):
        '''Show the final score at the end of the game.'''
        self.show_score(score, target, points, bonus, True)

    def show_high_scores(self, scores):
        '''Show the list of high scores.'''
        pass

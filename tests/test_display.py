import mock
import unittest

import display


class TestDisplay(unittest.TestCase):
    mock_config = {'score_font': '/assets/score_font.ttf'}

    def test_get_fullscreen_resolution(self):
        '''Ensure the first resoluiton in the list is returned.'''
        resolutions = [[1920, 1080], [320, 240]]
        pygame = mock.Mock()
        pygame.display = mock.Mock()
        pygame.display.list_modes = mock.Mock(return_value=resolutions)
        d = display.Display(self.mock_config, pygame)
        assert d.get_fullscreen_resolution() == resolutions[0]

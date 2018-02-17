import mock
import unittest

import game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.message_buffer = ''
        # Patch in the fake_log routine to create the game object
        with mock.patch('game.Game.log') as mock_log:
            mock_log.side_effect = self.fake_log
            self.game = game.Game()
        # Patch the fake_log handler in directly now that we have the object
        self.game.log = self.fake_log

    def fake_log(self, level, message):
        '''A fake log handler.'''
        self.message_buffer += message

    def test_init_game(self):
        '''Test game starting conditions.'''
        assert self.game.score == 0
        assert self.game.remaining_balls == 9
        assert self.game.game_over is False
        assert 'Game setup begin.' in self.message_buffer
        assert 'Game setup complete.' in self.message_buffer

    def test_drop_ball_miss(self):
        '''Test drop_ball actions when no target is hit.'''
        self.game.drop_ball(0)
        assert self.game.remaining_balls == 8
        assert 'Process drop_ball target: 0' in self.message_buffer
        assert 'Score is now 0 (0)' in self.message_buffer

    def test_drop_ball_hit(self):
        '''Test drop_ball actions.'''
        self.game.drop_ball(1)
        assert self.game.remaining_balls == 8
        assert 'Process drop_ball target: 1' in self.message_buffer
        assert 'Score is now 10 (10)' in self.message_buffer

    def test_check_game_over(self):
        '''Ensure game is over when there are no remaining balls.'''
        assert self.game.game_over is False
        self.game.remaining_balls = 0
        self.game.check_game_over()
        assert self.game.game_over is True

    def test_target(self):
        '''Ensure the expected point value is returned.'''
        assert self.game.target(0) == 0
        assert self.game.target(1) > 0

    def test_target_invalid_target(self):
        '''Hitting an invalid target number has a 0 point value.'''
        assert self.game.target(10) == 0
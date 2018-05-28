class FakeGPIO(object):
    BCM = 'BCM'
    IN = 'IN'
    PUD_UP = 'PUD_UP'
    FALLING = 'FALLING'

    def __init__(self):
        self.mode = None
        self.warnings = None
        self.pin_mapping = {}

    def setmode(self, mode):
        self.mode = mode

    def setwarnings(self, warnings):
        self.warnings = warnings

    def setup(self, pin_number, direction, pull_up_down=None):
        pin = {
            'direction': direction,
            'pull_up_down': pull_up_down,
        }

        self.pin_mapping[pin_number] = pin

    def add_event_detect(self, pin_number, edge, callback=None, bouncetime=0):
        assert pin_number in self.pin_mapping
        pin = self.pin_mapping[pin_number]
        pin['edge'] = edge
        pin['callback'] = callback
        pin['bouncetime'] = bouncetime

    def input(self, pin):
        return True

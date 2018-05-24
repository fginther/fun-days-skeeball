#!/usr/bin/env python
import logging
import sys
import time
import yaml

import cortex


def main():
    # Configure logging for the main module
    logging.basicConfig(format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)

    try:
        with open('config.yaml') as config_file:
            config = yaml.safe_load(config_file.read())
    except IOError:
        config = {}
    # Initialize the start-up machine state
    #mach = machine.Machine()
    ctex = cortex.Cortex(config)
    ctex.event_loop()
    return
    for score in range(0, 1001, 250):
        #disp.show_score(score)
        time.sleep(1)


    #cortext = cortex.Cortex(machine, display)
    return 0


if __name__ == '__main__':
    sys.exit(main())

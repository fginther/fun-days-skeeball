# Fun Days Skeeball

A skeeball arcade machine controller.

## Host configuration

Install the following on the host machine (running the lastest rasbian):

```
sudo apt install virtualenv libsdl1.2-dev
```

Then create the virtualenv for running the game and install dependencies:

```
virtualenv -p python .venv
.venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

Tests can be executed with python unittest:

```
python -m unittest discover -s ./tests
```

Copyright © 2017-2018, [Francis Ginther](https://github.com/fginther).
Released under the [MIT License](LICENSE).

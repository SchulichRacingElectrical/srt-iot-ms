# srv-iot-ms

Microservice for SR Telemetry communications with onboard hardware.

## Setting Up

Package management and virtual environment is managed by `poetry`. If you don't already have it installed, install `poetry` by running the command for your OS listed on [this page](https://python-poetry.org/docs/#installation).

After installing, run `poetry install` from within the root project directory to install any dependencies.

Once dependencies are installed, run `poetry shell` to activate the environment.

## Running

With the environment activated in your shell as described above, simply run `flask run` to run the service.

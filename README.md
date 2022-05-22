# srv-iot-ms

Microservice for SR Telemetry communications with onboard hardware.

## Setting Up

Package management and virtual environment is managed by `poetry`. If you don't already have it installed, install `poetry` by running the command for your OS listed on [this page](https://python-poetry.org/docs/#installation).

After installing, run `poetry install` from within the root project directory to install any dependencies.

Once dependencies are installed, run `poetry shell` to activate the environment.

Alternatively, use whichever environment manager you wish and install requirements via `requirements.txt`.

## Running

With the environment activated in your shell as described above, simply run `flask run` to run the service.

## Updating Requirements

To install a new package, run `poetry add <package>`. If it is a dev dependency (test framework, formatters, etc) add the `-D` flag.
To remove a package, run `poetry remove <package>`.

To keep `requirements.txt` up to date, run `pip list --format=freeze > requirements.txt`.

If installing or removing a package with a different package management tool, please add/remove the package and version to `pyproject.toml`.

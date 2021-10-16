# srv-iot-ms

Micro-service for SR Telemetry communications with onboard hardware.

# Running

Make sure to enter the python environment 'env' by:

source env/bin/activate

To leave the environment:

deactivate

If you install a new pip library, after installing, be sure to do this:

pip3 freeze > requirements.txt

# Running the hardware simulation

Depending on your machine, there will be different commands to run the run.sh bash file that compiles and executes the simulation.

On MacOS:

bash ./run.sh

If you add a new C and header file, update the bash file to include the new file in the compilation.

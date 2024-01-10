# Fetch Take-Home Exercise - SRE
health_check.py is used to perform health checks periodically for every 15 seconds on specified endpoints and report their availabiliy status. The script reads configuration details from a YAML file, executes health checks on the provided endpoints and outputs the result to the console.

1. Clone Repository: Using the git clone <https://github.com/Hemanth110500-projects/fetch>
2. Install the required python dependencies using pip install: *pip install pyyaml*
3. Create a YAML config file according to the requirements. Here we got the config.yaml file according to our requirements.
4. Run the script from the command line, providing the path to the YAML config file as an argument: *python health_check.py config.yaml*
5. To exit the script execution, press 'Ctrl + c'. The script exits printing an exit message.

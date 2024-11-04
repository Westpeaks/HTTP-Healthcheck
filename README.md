# Parse YAML File and Check the Health of HTTP Endpoints

## A fully functional script that parses a yaml file for multiple HTTP endpoints and then performs a series of HTTP requests to verify if the site is up and responds to requests.

This script was built as a coding challenge demonstrating how to parse a yaml file, extract URLs from the file, and run a series of HTTP requests to check, analyze, and verify the health (availability of access) of a particular site.

This script was written in python and uses the following libraries as dependancies:

- **yaml** to parse the yaml file.
- **requests** to make HTTP requests and return stauses
- **time** to perform time based calculations.
- **schedule** to run the script on every 15 seconds.
- **urllib.parse** to parse and extract the base domain as a component.

This sript does the following:

- Parses a Yaml file.
- Iterates through the endpoints in the file.
- Identifies and extracts the URL.
- Makes a GET request to the URL and returns the latency and status code.
- Detemines if the site is up or down based on the following parameters: UP = 200-299 status and latency of less than 500 miliseconds (ms). DOWN = Any other status code or a 200-299 with a latency higher than 500ms.
- Extracts the base domain from the potential of multiple subdomains and tests the base domain availability on the bases of the multiple subdomains listed.
  Ex. The yaml file may contain mutiple endpoints for the same domain (http://httpstat.us/404 and http://httpstat.us/200). The script will extract the domain and average the availability of both subdoamins. The result is that you will receive the availabilty of both subdomains combined.
- Adds each base domain to a dictionary and attaches the statistics to produce the final outcome of providing an availability percentage. This allows the script to be run for multiple domains at one time.
- Prints the availability percentage of each base domain on a schedule every 15s until terminated by the user using the ctrl+c command in the terminal.
  Ex. Here is an example of the output, "httpstat.us has 60% availability percentage."

### Installation Instructions

1. Install python if you have not done so. Install the necessary libraries. I used pip to install the libraries.
2. Clone this project.
3. Ensure your YAML file is in the same format as example provided or use the example YAML file.
4. Insert the correct file path in the parse_yaml() function.
5. Save and run the .py file. Hit ctrl+c in the console to stop program.

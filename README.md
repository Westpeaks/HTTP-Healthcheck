# Check the Health of HTTP Endpoints

## A fully functional script that parses a yaml file for multiple HTTP endpoints and then performs a series of HTTP requests to verify if the site is up and responds to requests.

This script was built as a coding challenge demonstrating how to parse a yaml file, extract URLs from the file, and run a series of HTTP requests to check, analyze, and verify the health (availability of access) of a particular site.

It was written in Python and uses the following libraries as dependancies:

- **yaml** to parse the yaml file.
- **requests** to make HTTP requests and return stauses
- **time** to perform time based calculations.
- **schedule** to run the script on every 15 seconds.
- **urllib.parse** to parse and extract the base domain as a component.

## Breakdown of Functionality

This sript does the following:

- Parses a Yaml file.

```python
def parse_yaml():
    try:
        # You will need to input the file path to the yaml file between the '' in the open statement.
        # Example yaml file is provided in the GH repo. Other yaml files used will need to follow the same format.
        with open('', 'r') as file:
            data = yaml.safe_load(file)
        return data

    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return []
```

- Iterates through the endpoints in the file.

```python
def scheduled_task():
    endpoints = parse_yaml()

    for endpoint in endpoints:
        if isinstance(endpoint, dict) and 'url' in endpoint:
            url = endpoint['url']

        else:
            continue

        latency, status_code = get_latency_and_status(url)
        status = check_status(latency, status_code)
        domain = urlparse(url).netloc
        if domain not in domain_stats:
            domain_stats[domain] = DomainStats()
        domain_stats[domain].update(status == "UP")

    print_availability_percentages()

```

- Identifies and extracts the URL.
- Makes a GET request to the URL and returns the latency and status code.
- Detemines if the site is up or down based on the following parameters: UP = 200-299 status and latency of less than 500 miliseconds (ms). DOWN = Any other status code or a 200-299 with a latency higher than 500ms.

```python
class DomainStats:
    def __init__(self):
        self.total_requests = 0
        self.up_requests = 0

    def update(self, is_up):
        self.total_requests += 1
        if is_up:
            self.up_requests += 1

    def availability_percentage(self):
        if self.total_requests == 0:
            return 0
        return round(100 * self.up_requests / self.total_requests)

def check_status(latency, status_code):
    if 200 <= status_code < 300 and latency < 500:
        return "UP"
    else:
        return "DOWN"
```

- Extracts the base domain from the potential of multiple subdomains and tests the base domain availability on the bases of the multiple subdomains listed.
  Ex. The yaml file may contain mutiple endpoints for the same domain (http://httpstat.us/404 and http://httpstat.us/200). The script will extract the domain and average the availability of both subdoamins. The result is that you will receive the availabilty of both subdomains combined.
- Adds each base domain to a dictionary and attaches the statistics to produce the final outcome of providing an availability percentage. This allows the script to be run for multiple domains at one time.

```python
def print_availability_percentages():
    for domain, stats in domain_stats.items():
        print(f"{domain} has {stats.availability_percentage()}% availability percentage")
```

- Prints the availability percentage of each base domain on a schedule every 15s until terminated by the user using the ctrl+c command in the terminal.
  Ex. Here is an example of the output, "httpstat.us has 60% availability percentage."

```python
def main():
    interval = 15

    scheduled_task()
    schedule.every(interval).seconds.do(scheduled_task)
    while True:
        schedule.run_pending()
        time.sleep(1)
```

## Installation Instructions

1. Install Python if you have not done so. Install the necessary libraries. I used pip to install the libraries.
2. Clone this project.
3. Ensure your YAML file is in the same format as example provided or use the example YAML file.
4. Insert the correct file path in the parse_yaml() function.
5. Save and run the .py file. Type ctrl+c in the console to stop program.

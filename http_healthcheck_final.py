import yaml
import requests
import time 
import schedule
from urllib.parse import urlparse

def main():
    interval = 15
    
    scheduled_task()
    schedule.every(interval).seconds.do(scheduled_task)
    while True:
        schedule.run_pending()
        time.sleep(1)
        

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
    
    
def print_availability_percentages():
    for domain, stats in domain_stats.items():
        print(f"{domain} has {stats.availability_percentage()}% availability percentage")    
    

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
    

domain_stats = {}


def check_status(latency, status_code):
    if 200 <= status_code < 300 and latency < 500:
        return "UP"
    else:
        return "DOWN"


def get_latency_and_status(url):
    response = requests.get(url)
    start_time = time.time()
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    status_code = response.status_code
    return latency, status_code


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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by the user.")
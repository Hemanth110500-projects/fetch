import yaml
import requests
import time
import sys
import argparse
from urllib.parse import urlparse


# Reading a YAML file and returning its content as a dictionary
def read_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{file_path}': {e}")
        sys.exit(1)

# Health checks on different endpoints
def health_check(endpoint):
    try:
        # Send HTTPS requests to the specified endpoints
        response = requests.request(
            method=endpoint.get('method', 'GET'),
            url=endpoint['url'],
            headers=endpoint.get('headers', {}),
            data=endpoint.get('body', None),
        )

        latency = response.elapsed.total_seconds() * 1000  # in milliseconds

        # Determine if the outcome is UP or DOWN based on status code and latency
        is_up = 200 <= response.status_code < 300 and latency < 500
        return is_up, response.status_code, latency
    except requests.RequestException as e:
        return False, None, str(e)

def main():
    # Command line argument parser
    parser = argparse.ArgumentParser(description='Health check script')
    parser.add_argument('config_file_path', type=str, help='Path to the YAML configuration file')
    args = parser.parse_args()
    try:
        # Read YAML config file
        endpoints = read_yaml_file(args.config_file_path)
    except Exception as e:
        print(f"Error reading or parsing YAML file '{args.config_file_path}': {e}")
        sys.exit(1)
    # Dictionary to store domain availability information
    domain_availability = {}
    cycle = 0

    try:
        # Record start time
        start_time = time.time()

        while True:
            # Increment cycle count
            cycle += 1
            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            # Print cycle start message
            print(f"Test cycle #{cycle} begins at time = {round(elapsed_time)} seconds")

            # Iterate through each endpoint in the configuration
            for endpoint in endpoints:
                # Perform health check on the endpoint
                is_up, status_code, latency = health_check(endpoint)
                # Extract domain from the endpoint URL
                domain = urlparse(endpoint['url']).netloc
                # If we have domain as fetchrewards.com append www.
                if domain == "fetchrewards.com":
                    domain = "www." + domain
                # Extract endpoint name and print status information
                endpoint_name = endpoint['name'].replace("fetch ", "")
                print(f"Endpoint with name {domain} {endpoint_name} has HTTP response code {status_code} "
                      f"and response latency {latency} ms => {'UP' if is_up else 'DOWN'}")

                # Update Domain availability information
                domain_availability.setdefault(domain, {'total': 0, 'up': 0})
                domain_availability[domain]['total'] += 1
                if is_up:
                    domain_availability[domain]['up'] += 1

            # Print cycle end message
            print(f"Test cycle #{cycle} ends.")
            print("\n")
            
            # Print availability information for each domain
            for domain, availability in domain_availability.items():
                total, up = availability['total'], availability['up']
                availability_percentage = round((up / total) * 100) if total > 0 else 0
                print(f"{domain} has {availability_percentage}% availability percentage")

            print("\n")
            
            # Pause the execution for 15 seconds before starting the next cycle
            time.sleep(15)
    
    # If (ctl + c) keyboard Interrupt, the program exits
    except KeyboardInterrupt:
        print("\nExit")

if __name__ == "__main__":
    main()

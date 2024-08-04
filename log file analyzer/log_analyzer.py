import re
from collections import defaultdict, Counter

# Configuration
LOG_FILE_PATH = 'webserver.log'

# Regex pattern for common log format (you may need to adjust it for your log format)
log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d{3}) (?P<size>\S+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
)

def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

def analyze_log_file(log_file_path):
    ip_counter = Counter()
    requested_pages_counter = Counter()
    status_counter = Counter()

    with open(log_file_path, 'r') as file:
        for line in file:
            log_entry = parse_log_line(line)
            if log_entry:
                ip_counter[log_entry['ip']] += 1
                request = log_entry['request']
                if request:
                    requested_page = request.split(' ')[1]
                    requested_pages_counter[requested_page] += 1
                status_counter[log_entry['status']] += 1

    return ip_counter, requested_pages_counter, status_counter

def print_summary(ip_counter, requested_pages_counter, status_counter):
    print("Summary Report")
    print("==============")

    print("\nTop 10 IP Addresses with Most Requests:")
    for ip, count in ip_counter.most_common(10):
        print(f"{ip}: {count} requests")

    print("\nTop 10 Most Requested Pages:")
    for page, count in requested_pages_counter.most_common(10):
        print(f"{page}: {count} requests")

    print("\nHTTP Status Codes:")
    for status, count in status_counter.items():
        print(f"{status}: {count} occurrences")

    print("\nNumber of 404 Errors:")
    print(status_counter.get('404', 0))

if __name__ == "__main__":
    ip_counter, requested_pages_counter, status_counter = analyze_log_file(LOG_FILE_PATH)
    print_summary(ip_counter, requested_pages_counter, status_counter)

import re
import csv
from collections import defaultdict

# Regular expression to match datetime, URL path, and status code in log entries
log_pattern = re.compile(r'\[(.*?)\].*"GET (\S+) HTTP.*" (\d{3}) ')

def process_log_file(file_path):
    paths = defaultdict(lambda: {'count': 0, 'last_access': None, 'status_code': None})

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = log_pattern.search(line)
            if match:
                datetime, path, status_code = match.groups()
                paths[path]['count'] += 1
                paths[path]['last_access'] = datetime
                paths[path]['status_code'] = status_code

    return paths

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Access Count', 'Last Access', 'Status Code'])

        for path, info in data.items():
            writer.writerow([path, info['count'], info['last_access'], info['status_code']])

def main():
    log_file = '/Users/shz/Downloads/heimlicher.com_access.log'
    output_csv = 'heimlicher.com_access.csv'
    paths = process_log_file(log_file)
    write_to_csv(paths, output_csv)
    print(f"Analysis completed. Data written to {output_csv}")

if __name__ == "__main__":
    main()

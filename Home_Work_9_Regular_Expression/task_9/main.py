from collections import Counter

from Home_Work_9_Regular_Expression.task_7 import ip


def ip_from_log():
    """Counts the occurrences of IP addresses in a log file.
    Opens the specified log file, reads each line, extracts IP addresses
    using a regular expression, and counts the occurrences of each unique IP.
    """

    with open(file_name, "r", encoding="utf-8") as file:
        ip_counter = Counter()
        for line in file:
            if ip_count := ip(line):
                ip_counter[ip_count[0]] += 1
    return ip_counter


file_name = "file.log"
for find_ip, count in ip_from_log().most_common(10):
    print(f"{find_ip}: {count} request")

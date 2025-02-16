from collections import Counter

from Home_Work_9_Regular_Expression.task_7 import ip


def ip_from_log(file_name_for_search: str) -> Counter[str]:
    """Counts the occurrences of IP addresses in a log file.

    This function reads a log file, extracts IP addresses from each line, and counts the frequency of each unique IP address.

    Args:
        file_name_for_search: The path to the log file.

    Returns:
        A Counter object where keys are IP addresses and values are their counts.
    """

    with open(file_name_for_search, "r", encoding="utf-8") as file:
        ip_counter = Counter()
        for line in file:
            if ip_list := ip(line):
                for ip_addr in ip_list:
                    ip_counter[ip_addr] += 1
    return ip_counter


file_name = "file.log"
for find_ip, count in ip_from_log(file_name).most_common(10):
    print(f"{find_ip}: {count} request")

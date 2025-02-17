import pprint
import re


def ip(text: str) -> list[int] | None:
    """Finds and validates IPv4 addresses in a given text.

    This function searches for strings that resemble IPv4 addresses and then validates each found string to ensure it conforms to the IPv4 address format.

    Args:
        text: The input string to search for IPv4 addresses.

    Returns:
        A list of valid IPv4 addresses found in the input text, or None if no valid addresses are found.
    """
    ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    list_ip = ip_pattern.findall(text)
    mas_ip = []
    for ip_from_list in list_ip:
        ip_part = ip_from_list.split(".")
        flag = not any(int(part) < 0 or int(part) > 255 for part in ip_part)
        if flag:
            mas_ip.append(ip_from_list)
    return mas_ip


if __name__ == "__main__":
    pprint.pprint(ip("22.222.222.222 555.555.555.555"))

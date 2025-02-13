import pprint
import re


def ip(text: str):
    """Extracts valid IPv4 addresses from a given string.
    This function searches for patterns matching IPv4 addresses and validates each octet to be within the range of 0 to 255.
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

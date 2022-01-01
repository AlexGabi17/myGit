import re


def check_if_date(string: str):
    regex = "[0-9]*-[0-9]*-[0-9]*"
    return False if not re.search(regex, string) else True


def get_task_from_command(data: list[str]):
    result = ""
    idx = 1

    for str in data[1:]:
        if check_if_date(str):
            break
        result += str + " "
        idx += 1

    return (idx, result)

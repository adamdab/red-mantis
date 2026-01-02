import re

def regex_mathcher(value: str, pattern:str = '*') -> bool:
    return bool(re.fullmatch(pattern, value))

def exact(value: str, expected: str) -> bool:
    return value == expected
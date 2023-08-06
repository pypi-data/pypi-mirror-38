import string

__all__ = ['convert_base', 'convert_to_base_10']


def convert_to_base_10(x: int, base: int) -> str:
    """https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-in-any-base-to-a-string"""
    digits = string.digits + string.ascii_uppercase
    if x < 0:
        sign = -1
    elif x == 0:
        return digits[0]
    else:
        sign = 1
    x *= sign
    converted = []
    while x:
        converted.append(digits[int(x % base)])
        x = int(x // base)
    if sign < 0:
        converted.append('-')
    converted.reverse()
    return ''.join(converted)


def convert_base(x: str, source: int, dest: int) -> str:
    """
    Returns:
        'n' converted from base 'source' to base 'dest'
    """
    if source == 10:
        return convert_to_base_10(int(x), dest)
    return convert_to_base_10(int(x, source), dest)

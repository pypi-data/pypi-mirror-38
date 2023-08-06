def gcd(a: int, b: int) -> int:
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b

    return a


def lcm(a: int, b: int) -> int:
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def lcmm(*args: int) -> int:
    if len(args) == 1:
        return args[0]
    else:
        return lcmm(lcm(args[0], args[1]), *args[2:])

def modulo(a, b, n):
    binary = getBinaryRepresentation(b)
    print(binary)

def getBinaryRepresentation(n):
    res = ''  # binary result

    while n > 0:
        res = str(n & 1) + res
        n >>= 1

    return res

modulo(1, 21323, 1)
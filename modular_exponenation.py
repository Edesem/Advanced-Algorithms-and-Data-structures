def modulo(a, b, n):
    binary = getBinaryRepresentation(b)
    
    # Base case
    current = a % n
    lsb = binary[-1]
    binary = binary[:-1]
    if lsb in binary == 1:
        result = current
    else:
        result = 1

    for i in range(1, len(binary) + 1):
        lsb = int(binary[-i])
        current = (current * current) % n
        if lsb == 1:
            result = (result * current) % n
            
    return result
    

def getBinaryRepresentation(n):
    # Reference is geeks for geeks
    # https://www.geeksforgeeks.org/python-program-to-covert-decimal-to-binary-number/
    res = ''  # binary result

    while n > 0:
        res = str(n & 1) + res
        n >>= 1

    return res

print(modulo(7, 330, 13))
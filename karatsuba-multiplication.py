from modular_exponenation import getBinaryRepresentation

def multiply(u, v):
    if u < 10 or v < 10:
        return u * v
    else:
        n = max(len(str(u)), len(str(v)))
        half = n // 2

        left_u = int(str(u)[:half])
        right_u = int(str(u)[half:])
        left_v = int(str(v)[:half])
        right_v = int(str(v)[half:])

        left = multiply(left_u, left_v)
        right = multiply(right_u, right_v)
        left_right = multiply((left_u + right_u), (left_v + right_v))

        return left * (10 ** (2 * half)) + ((left_right - left - right) * (10 ** half)) + right

print(multiply(13, 14))
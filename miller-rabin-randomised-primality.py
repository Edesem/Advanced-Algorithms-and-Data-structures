import random

def millerRabinRandomisedPrimality(n,k):
    # Special case
    if n == 2 or n == 3:
        return True
    
    # If n is even
    if n < 2 or n % 2 == 0:
        return False
    
    # Factor n - 1 as (2^s)*t, where t is odd
    s = 0
    t = n - 1
    while t % 2 == 0:
        s = s + 1
        t = t // 2
    
    # Run k random tests
    for _ in range(k):
        # Select random witness
        a = random.randrange(1,n-1)
        x = pow(a, t, n)  # x0 = a^t mod n


        # Check if n satisfies fermat's little theorem for this witness
        if x == 1 or x == n - 1:
            continue
        
        # Run sequence test
        for _ in range(s):
            x = pow(x, 2, n)

            if x == n - 1:
                break
            if x == 1:
                # x_j == 1 and x_{j-1} != 1 and != n-1
                return False
            
        else:
            return False  # Composite
    
    # If n has passed all tests, then it's probably a prime
    return True

print(millerRabinRandomisedPrimality(999983, 100000))
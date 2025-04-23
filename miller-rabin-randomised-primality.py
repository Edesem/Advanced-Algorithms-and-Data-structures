def millerRabinRandomisedPrimality(n,k):
    # Special case
    if n == 2 or n == 3:
        return True
    
    # If n is even
    if n % 2 == 0:
        return False
    
    


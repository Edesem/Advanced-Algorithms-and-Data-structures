from modular_exponenation import getBinaryRepresentation

def multiply(u, v):
   u_b = getBinaryRepresentation(u) 
   v_b = getBinaryRepresentation(v)
   return u_b, v_b

print(multiply(13, 14))
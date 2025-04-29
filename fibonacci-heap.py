class Node():
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.mark = False

        self.parent = None 
        self.child = None
        self.left = None
        self.right = None

class FibonacciHeap():

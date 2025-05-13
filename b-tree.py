class Node():
    def __init__(self):
        self.keys = []
        self.children = None
        self.parent = None

    def get_length(self):
        return len(self.keys)
    
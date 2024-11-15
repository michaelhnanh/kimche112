class Experience:
    def __init__(self, x, y, size, color, value):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.value = value
    
    def absorb(self):
        return self.value    
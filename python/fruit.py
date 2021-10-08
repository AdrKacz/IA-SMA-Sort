class Fruit:
    def __init__(self, x, y, key):
        self.x = x
        self.y = y
        self.key = key
        self.color = 1 if key == 'A' else 2
        self.is_carried = False

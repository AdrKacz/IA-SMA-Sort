class Fruit:
    colors = {'A': 2, 'B': 3, 'C': 4}
    def __init__(self, x, y, key):
        self.x = x
        self.y = y
        self.key = key
        self.color = Fruit.colors.get(key, 0)
        self.is_carried = False

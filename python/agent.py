import random

class Agent:
    k_plus, k_minus = 0.1, 0.3
    memory_length = 100
    error_rate = 0.00

    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.memory = list()
        self.parent = parent
        self.fruit = None
        self.color = 3

    def get_frequency(self, key):
        assert len(self.memory) <= Agent.memory_length
        assert not key is None
        if len(self.memory) == 0:
            return 0
        count, other = 0, 0
        for value in self.memory:
            if value == key:
                count += 1
            elif value != 0:
                other += 1
        return (count + other * Agent.error_rate) / len(self.memory)

    def will_carry(self, key):
        frequency = self.get_frequency(key)
        return random.random() < (Agent.k_plus / (Agent.k_plus + frequency)) ** 2

    def will_release(self):
        frequency = self.get_frequency(self.fruit.key)
        return random.random() < (frequency / (Agent.k_minus + frequency)) ** 2

    def act(self):
        empty_neighbors = list(self.parent.get_empty_neighbors(self.x, self.y))
        fruit_neighbors = list(self.parent.get_fruit_neighbors(self.x, self.y))
        key_fruit = 0
        if len(fruit_neighbors) > 0:
            key_fruit = random.choice(fruit_neighbors).key

        # Update memory
        while len(self.memory) >= Agent.memory_length:
            self.memory.pop(0)
        self.memory.append(key_fruit)

        if len(empty_neighbors) == 0:
            return

        # Move
        old_x, old_y = self.x, self.y
        self.x, self.y = random.choice(empty_neighbors)
        # If carry, release, else look around
        if self.fruit:
            if self.will_release(): # Release fruit
                self.fruit.x, self.fruit.y = old_x, old_y
                self.color = 3 # Release
                self.fruit.is_carried = False
                self.fruit = None
        else:
            fruit = None
            for f in fruit_neighbors:
                if self.will_carry(f.key):
                    fruit = f
                    break

            if fruit: # Carry this fruit (new_key)
                self.x, self.y = fruit.x, fruit.y # Overwrite movement
                self.color = fruit.color
                fruit.is_carried = True
                self.fruit = fruit

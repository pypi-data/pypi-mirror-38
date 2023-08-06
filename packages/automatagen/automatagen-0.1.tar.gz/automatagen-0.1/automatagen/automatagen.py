import random

class TerrainGenerator():
    def __init__(self,
                 initial_density = 0.48,
                 steps = 5,
                 loneliness_limit = 4):

        self.initial_density = initial_density
        self.steps = steps
        self.loneliness_limit = loneliness_limit


    def _randomize(self):
        # seed random function
        random.seed(a = self.seed)

        # change cell to true if random float is under initial_density
        for y in range(0, self.height):
            for x in range(0, self.width):
                if random.random() < self.initial_density:
                    self._cells[y][x] = False

    def _step_simulation(self):
        # initialize a new 2d cell array
        new_cells = [[True for x in range(self.width)] for y in range(self.height)]

        # iterate over cells
        for y in range(0, self.height):
            for x in range(0, self.width):
                neighbours = self._count_living_neighbours(x, y)

                if neighbours > self.loneliness_limit:
                    new_cells[y][x] = True
                else:
                    new_cells[y][x] = False

        self._cells = new_cells

    def _count_living_neighbours(self, x, y):
        count = 0

        # iterate over the 3x3 neighbourhood
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbour_x = x + i
                neighbour_y = y + j

                # if neighbour is outside of map, count it
                if neighbour_x < 0 or neighbour_y < 0 or neighbour_y >= len(self._cells) or neighbour_x >= len(self._cells[0]):
                    count += 1
                # if neighbour is alive, count it
                elif self._cells[neighbour_y][neighbour_x]:
                    count += 1
        return count

    def generate(self, width, height, seed = None):
        self.width = width
        self.height = height

        # create 2d bool array, all true (walls)
        self._cells = [[True for x in range(self.width)] for y in range(self.height)]

        # generate random seed or use provided
        if not seed:
            seed = random.randrange(2147483648)
        self.seed = seed

        self._randomize()

        for step in range(self.steps):
            self._step_simulation()

        return self._cells

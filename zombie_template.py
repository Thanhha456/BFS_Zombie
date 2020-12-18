"""
Student portion of Zombie Apocalypse mini-project
"""

import grid_class_zombie
import queue_zombie
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(grid_class_zombie.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list=None,
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        grid_class_zombie.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        grid_class_zombie.Grid.clear(self)

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
        return self._zombie_list

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie


    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        return self._human_list

    def num_humans(self):
        """
        Return number of humans
        """

        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human


    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        if entity_type == "human":
            entity_queue = self._human_list
        elif entity_type == "zombie":
            entity_queue = self._zombie_list

        #define visited bondary and istance field, initially with max which is the product of grid_height and grid_width
        visited_grid = grid_class_zombie.Grid(self._grid_height, self._grid_width)
        value = self._grid_width * self._grid_height
        entity_distance_field = [[value for dummy_x in range(self._grid_width)]
                                 for dummy_y in range(self._grid_height)]
        for entity in entity_queue:
            visited_grid.set_full(entity[0], entity[1])
            entity_distance_field[entity[0]][entity[1]] = 0

        #define the queue
        queue = queue_zombie.Queue()
        for dummy in entity_queue:
            queue.enqueue(dummy)

        #BFS
        while queue:
            entity = queue.dequeue()
            if entity_type == "human":
                neighbors = self.four_neighbors(entity[0], entity[1])
            elif entity_type == "zombie":
                neighbors = self.eight_neighbors(entity[0], entity[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]) and visited_grid.is_empty(neighbor[0], neighbor[1]):
                    visited_grid.set_full(neighbor[0], neighbor[1])
                    entity_distance_field[neighbor[0]][neighbor[1]] = entity_distance_field[entity[0]][entity[1]] + 1
                    queue.enqueue(neighbor)
        return entity_distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0], human[1])
            zombie_list = []
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    zombie_list.append((zombie_distance_field[neighbor[0]][neighbor[1]], (neighbor[0], neighbor[1])))
            human_move = max(zombie_list)[1]
            new_human_list.append(human_move)
        self._human_list = new_human_list


    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            human_list = []
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    human_list.append((human_distance_field[neighbor[0]][neighbor[1]], (neighbor[0], neighbor[1])))
            zombie_move = min(human_list)[1]
            new_zombie_list.append(zombie_move)
        self._zombie_list = new_zombie_list



# Start up gui for simulation - You will need to write some code above
# before this will work without errors
poc_zombie_gui.run_gui(Apocalypse(30, 40))


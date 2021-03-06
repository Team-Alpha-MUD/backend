# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
import random

# random.seed(12)
class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)

    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from center
        x = size_x//2
        y = size_y//2
        room_count = 0

        previous_room = None
        prev_dir = None
        # While there are rooms to be created...
        while room_count < num_rooms:
            directions = []
            if x < size_x - 1 and prev_dir != 'w':
                directions.append('e')
            if x > 0 and prev_dir != 'e':
                directions.append('w')
            if y > 0 and prev_dir != 'n':
                directions.append('s')
            if y < size_y - 1 and prev_dir != 's':
                directions.append('n')

            room_direction = random.choice(directions)
            prev_dir = room_direction
            if room_direction == 'n':
                y += 1
            elif room_direction == 'e':
                x += 1
            elif room_direction == 's':
                y -= 1
            else:
                x -= 1

            # If room already exist, call it back
            if self.grid[y][x]:
                room = self.grid[y][x]
            # Create room only if room doesn't exist yet
            else:
                room = Room(room_count, "A Generic Room",
                            "This is a generic room.", x, y)
                self.grid[y][x] = room
                room_count += 1
            # Note that in Django, you'll need to save the room after you create it

            # Connect the room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)
            # Update iteration variables
            previous_room = room

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 100
width = 31
height = 11
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")

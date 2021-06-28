'''
File: 2048.py
Author: Gavin Vogt
This program will create a graphics window for the user to play
2048 using the arrow keys and the undo button.
'''

from graphics import graphics
import random

class Board:
    def __init__(self, size, colors=None):
        self._size = size
        self._grid = [[None for i in range(size)] for i in range(size)]
        self._prev_grid = None
        self._undo_available = False
        self._score = 0

        # to help with drawing
        self._tile_size = (392 - 8*size)/size
        self._color_scheme = colors

    def __str__(self):
        spacing = len(str(self.get_max()))
        retstring = ("+--" + "-"*spacing) * self._size + "+"
        for row in self._grid:
            row_string = "\n"
            for tile in row:
                tile_str = tile or ""
                row_string += "| " + str(tile_str).center(spacing) + " "
            row_string += "|\n"
            retstring += row_string  + ("+--" + "-"*spacing) * self._size + "+"

        return retstring

    def draw(self, canvas):
        '''
        Draws the board on the provided graphics window
        '''
        canvas.clear()
        canvas.rectangle(0, 0, 500, 600, "light gray")
        canvas.text(200, 10, "2048", "green", 40)
        canvas.text(50, 90, f"Score: {self._score}", "blue", 30)
        # draw undo button
        canvas.rectangle(415, 95, 35, 35, "blue")
        canvas.line(430, 122, 442, 122, "light blue", 5)
        canvas.line(442, 125, 442, 103, "light blue", 5)
        canvas.line(445, 103, 421, 103, "light blue", 5)
        canvas.line(423, 103, 423, 118, "light blue", 5)
        # arrow head in undo button
        canvas.line(423, 118, 418, 112, "light blue")
        canvas.line(422, 118, 429, 112, "light blue")
        canvas.line(416, 112, 431, 112, "light blue", 1)

        canvas.rectangle(50, 150, 400, 600 - 200, "dark gray")
        tile_size = self._tile_size
        for y in range(self._size):
            for x in range(self._size):
                # Draw the tile at (x, y)
                tile_num = self._grid[y][x]
                color = self._color_scheme[tile_num]
                if tile_num is None:
                    tile_num = ""
                canvas.rectangle(58 + (tile_size + 8)*x, 158 + (tile_size + 8)*y,
                tile_size, tile_size, color)
                canvas.text(58 + (tile_size + 8)*x, 158 + (tile_size + 8)*y, tile_num)
        canvas.update()

    def add_tile(self):
        '''
        Adds a tile randomly to the board
        '''
        num = random.randint(1, 2) * 2   # 2 or 4 tile
        x, y = random.choice(self.get_empty_tiles())
        self._grid[y][x] = num

    def can_undo(self):
        return self._undo_available

    def perform_move(self, direction):
        assert direction in ["l", "r", "u", "d"]

        # make a copy of the grid
        copy = []
        for row in self._grid:
            copy.append(row.copy())

        if direction == "l":
            self.swipe_left()
        elif direction == "r":
            self.swipe_right()
        elif direction == "u":
            self.swipe_up()
        elif direction == "d":
            self.swipe_down()

        # Check that the move actually changed the board
        if self._grid != copy:
            # board changed (good)
            self._prev_grid = copy
            self._undo_available = True
            self.add_tile()
        else:
            # board did not change (must revert)
            self._grid = copy

    def swipe_left(self):
        for y in range(self._size):
            row = [0]
            for x in range(self._size):
                cur_tile = self._grid[y][x]
                self._grid[y][x] = None
                if cur_tile is not None:
                    if cur_tile == row[-1]:
                        row[-1] = cur_tile * 2
                        self._score += row[-1]
                        row.append(0)
                    else:
                        row.append(cur_tile)

            x = 0
            for num in row:
                if num != 0:
                    self._grid[y][x] = num
                    x += 1

    def swipe_right(self):
        for y in range(self._size):
            row = [0]
            for x in range(self._size - 1, -1, -1):
                cur_tile = self._grid[y][x]
                self._grid[y][x] = None
                if cur_tile is not None:
                    if cur_tile == row[-1]:
                        row[-1] = cur_tile * 2
                        self._score += row[-1]
                        row.append(0)
                    else:
                        row.append(cur_tile)

            x = -1
            for num in row:
                if num != 0:
                    self._grid[y][x] = num
                    x -= 1

    def swipe_up(self):
        for x in range(self._size):
            column = [0]
            for y in range(self._size):
                cur_tile = self._grid[y][x]
                self._grid[y][x] = None
                if cur_tile is not None:
                    if cur_tile == column[-1]:
                        column[-1] = cur_tile * 2
                        self._score += column[-1]
                        column.append(0)
                    else:
                        column.append(cur_tile)

            y = 0
            for num in column:
                if num != 0:
                    self._grid[y][x] = num
                    y += 1

    def swipe_down(self):
        for x in range(self._size):
            column = [0]
            for y in range(self._size - 1, -1, -1):
                cur_tile = self._grid[y][x]
                self._grid[y][x] = None
                if cur_tile is not None:
                    if cur_tile == column[-1]:
                        column[-1] = cur_tile * 2
                        self._score += column[-1]
                        column.append(0)
                    else:
                        column.append(cur_tile)

            y = -1
            for num in column:
                if num != 0:
                    self._grid[y][x] = num
                    y -= 1

    def get_max(self):
        '''
        Gets the highest value tile on the board
        '''
        max_tile = 0
        for row in self._grid:
            for tile in row:
                if tile is not None and tile > max_tile:
                    max_tile = tile

        return max_tile

    def get_empty_tiles(self):
        '''
        Get the list of empty locations on the board
        '''
        empty_locs = []
        for y in range(self._size):
            for x in range(self._size):
                if self._grid[y][x] is None:
                    empty_locs.append( (x, y) )

        # list of empty (x, y) locations
        return empty_locs

    def undo(self):
        '''
        Restores the board to the previous board
        '''
        if self._undo_available:
            self._grid = []
            for row in self._prev_grid:
                self._grid.append(row.copy())
            self._undo_available = False

    def is_game_over(self):
        '''
        Checks if the game is over
        '''
        if self.get_empty_tiles() != []:
            return False
        for y in range(self._size):
            for x in range(self._size):
                if self._grid[y][x] in self._get_adjacent_tiles(x, y):
                    return False

        # didn't find any possible moves left
        return True

    def _get_adjacent_tiles(self, x, y):
        '''
        Gets the values of every tile adjacent to the one
        at (x, y)
        x: int
        y: int
        '''
        assert 0 <= x < self._size
        assert 0 <= y < self._size

        adj_tiles = []
        if 0 < x:
            adj_tiles.append(self._grid[y][x-1])
        if x < self._size - 1:
            adj_tiles.append(self._grid[y][x+1])
        if 0 < y:
            adj_tiles.append(self._grid[y-1][x])
        if y < self._size - 1:
            adj_tiles.append(self._grid[y][y+1])
        return adj_tiles

def keyboard_input(window, keycode, board):
    if keycode == 81:
        # quit
        window.primary.destroy()
    elif keycode in [37, 38, 39, 40]:
        direction = {37: "l", 38: "u", 39: "r", 40: "d"}[keycode]
        board.perform_move(direction)
        board.draw(window)

def mouse_input(window, x, y, board):
    '''
    If the mouse clicks in the right region on the board window,
    the board will undo a move and redraw.
    '''
    if (415 <= x < 450) and (95 <= y < 130):
        board.undo()
        board.draw(window)

def command_line_game():
    '''
    This function allows the user to play 2048 in the
    command line.
    '''
    size = int(input("Board size? "))
    board = Board(size)
    board.add_tile()
    print(board)
    command = ""
    while command != "quit":
        if board.is_game_over():
            print("Game over")
            break
        command = input("> ")
        if command in ["l", "r", "u", "d"]:
            board.perform_move(command)
        elif command == "undo":
            board.undo()
        print(board)

def main():
    size = int(input("Board size? "))
    window = graphics(500, 600, "2048")

    color_dictionary = {None: "gray",
                        2: "AntiqueWhite1",
                        4: "bisque2",
                        8: "orange",
                        16: "dark orange",
                        32: "orange red",
                        64: "red",
                        128: "LightGoldenrod1",
                        256: "goldenrod1",
                        512: "purple"}

    board = Board(size, color_dictionary)
    board.add_tile()
    board.draw(window)
    window.set_keyboard_action(keyboard_input, board)
    window.set_left_click_action(mouse_input, board)
    window.mainloop()

if __name__ == "__main__":
    main()
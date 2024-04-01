'''
Requirements
1. Create a recursive, multithreaded program that finds the exit of each maze.
   
Questions:
1. It is not required to save the solution path of each maze, but what would
   be your strategy if you needed to do so?
   >mp.Array
   >
2. Is using threads to solve the maze a depth-first search (DFS) or breadth-first search (BFS)?
   Which search is "better" in your opinion? You might need to define better. 
   (see https://stackoverflow.com/questions/20192445/which-procedure-we-can-use-for-maze-exploration-bfs-or-dfs)
   >bfs and I prefer bfs
   >
'''

import math
import threading
from screen import Screen
from maze import Maze
import sys
import cv2

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (72, 61, 139),
    (143, 143, 188),
    (226, 138, 43),
    (128, 114, 250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False


def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_find_end(maze: Maze, solution_path, position, color):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    # TODO - add code here
    # Calls gloabl variables
    global stop
    global thread_count
    # initialize row and column
    row = position[0]
    col = position[1]

    # Checks to see if maze is done
    if maze.at_end(row, col):
        stop = True

    # add path to maze
    solution_path.append(position)

    # creates Array of Possible Arrays
    moves = maze.get_possible_moves(row, col)

    # array to append my threads
    piece = []

    # For loop to look for possible moves and make the correct moves
    for i in range(len(moves)):
        # Stops threads
        if stop == True:
            break

        # initialize thread
        p = threading.Thread(target=solve_find_end, args=(
            maze, solution_path, moves[i], color))

        # start thread
        piece.append(p)

        # Checks for possible Moves
        if maze.can_move_here(moves[i][0], moves[i][1]):
            maze.move(moves[i][0], moves[i][1], color)

            # Changes Color
            color = get_color()

            # Update Thread count
            thread_count += 1

            # Starts Thread
            p.start()

        # get's rid of false coordinates
        else:
            solution_path.pop()


def find_end(filename, delay):

    global thread_count
    global stop

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    # Initializes thread
    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    # Array for solution path
    solution_path = []

    # gets starting position
    start = maze.get_start_pos()

    # moves to start
    maze.move(start[0], start[1], COLOR)

    # initializes threads
    stop = False

    # calls functions
    solve_find_end(maze, solution_path, maze.get_start_pos(), get_color())

    print(f'Number of drawing commands = {screen.get_command_count()}')
    print(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True


def find_ends():
    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    print('*' * 40)
    print('Part 2')
    for filename, delay in files:
        print()
        print(f'File: {filename}')
        find_end(filename, delay)
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_ends()


if __name__ == "__main__":
    main()

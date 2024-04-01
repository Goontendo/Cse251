'''
Requirements
1. Create a recursive program that finds the solution path for each of the provided mazes.
'''

import math
from screen import Screen
from maze import Maze
import cv2
import sys

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


# TODO add any functions
def recursion(maze: Maze, solution_path, position):
    # initialize row and column
    row = position[0]
    col = position[1]

    # add path to maze
    solution_path.append(position)

    # Checks to see if maze is done
    if maze.at_end(row, col):
        return True

    # creates Array of Possible Arrays
    moves = maze.get_possible_moves(row, col)

    # For loop to look for possible moves and make the correct moves
    for i in range(len(moves)):
        if maze.can_move_here(moves[i][0], moves[i][1]):
            maze.move(moves[i][0], moves[i][1], COLOR)
        if recursion(maze, solution_path, moves[i]) == True:
            return True
        else:
            maze.restore(moves[i][0], moves[i][1])
            solution_path.pop()


def solve(maze):
    """ Solve the maze. The path object should be a list (x, y) of the positions 
        that solves the maze, from the start position to the end position. """

    # TODO add code here
    solution_path = []

    start = maze.get_start_pos()

    maze.move(start[0], start[1], COLOR)

    recursion(maze, solution_path, maze.get_start_pos())

    # Remember that an object is passed by reference, so you can pass in the
    # solution_path object, modify it, and you won't need to return it from
    # your recursion function

    return solution_path


def get_solution_path(filename):
    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    solution_path = solve(maze)

    print(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return solution_path


def find_paths():
    files = ('verysmall.bmp', 'verysmall-loops.bmp',
             'small.bmp', 'small-loops.bmp',
             'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    print('*' * 40)
    print('Part 1')
    for filename in files:
        print()
        print(f'File: {filename}')
        solution_path = get_solution_path(filename)
        print(f'Found path has length          = {len(solution_path)}')
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_paths()


if __name__ == "__main__":
    main()

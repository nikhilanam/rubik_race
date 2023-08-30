import pygame
import pygame.math
from board import Board, Reference
import sys
import model
import ai
import numpy as np
import random

# size constants
SIZE = 5
TILE = 50
SPACING = 20
WIDTH = ((SIZE+6)*TILE + (SIZE+5)*SPACING)
HEIGHT = ((SIZE+2)*TILE) + ((SIZE+1)*SPACING)

# setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rubik's Race")

# initialize board
board = Board(size=SIZE)
board.shuffle()

reference = Reference(size=SIZE)
reference.shuffle()
puzzle = model.Puzzle()

# create tiles
player_tiles = [pygame.Surface((TILE, TILE)) for i in range(SIZE**2)]
tile_coordinates = [board.board[i].get_position() for i in range(len(board.board))]
reference_tiles = [pygame.Surface((TILE, TILE)) for i in range(SIZE ** 2)]

# clock
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# initialize ai solutions
ai.init(5)
aiMoves = []  # ai.idaStar(puzzle)
aiMoveIndex = 0
first_time = True

# Reshuffle when "r" is pressed, perform ai moves when "h" is pressed (will build ai solution when "h" is pressed the first time).

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(tile_coordinates)):
                rect = player_tiles[i].get_rect(topleft=tile_coordinates[i])
                if rect.collidepoint(mouse_pos):
                    board.update(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board.shuffle()
                reference.shuffle()
                aiMoveIndex = 0
                aiMoves = []
                first_time = True
            elif event.key == pygame.K_h:
                if len(aiMoves) == 0:
                    # enter here when aiMoves is empty
                    count_in_goal, rlist, olist, ylist, glist, blist, wlist = reference.colorcount()
                    if not first_time:
                        ''' 
                        enter here when not solved in one quadrant. 
                        First check whether it can be solved in one quadrant now. If yes, record which quadrant.
                        If not, find and record which quadrant(s) has least amount of missing colors.
                        Then based on the previous quadrant and the next quadrant, shuffle the blank space without 
                        shifting the inner three-by-three.
                        '''
                        candidate_q_index = []
                        once = False
                        mis_color_count = [0]*4
                        for i in range(4):
                            count_in_quadrant = board.colorcount(i+1)
                            if np.all(np.asarray(count_in_quadrant) >= np.asarray(count_in_goal)):
                                candidate_q_index.append(i+1)
                                once = True
                                break
                            for j in range(len(count_in_quadrant)):
                                if count_in_goal[j] > count_in_quadrant[j]:
                                    mis_color_count[i] += count_in_goal[j] - count_in_quadrant[j]
                        if not once:
                            candidate_q_index = mis_color_count.index(min(mis_color_count))
                            print('Missing pieces in quadrant ', candidate_q_index, ' - ', mis_color_count[candidate_q_index])
                        if quadrant == 1:
                            if 4 in candidate_q_index:
                                q_index = 4
                            elif 3 in candidate_q_index:
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index+SIZE)  # move up
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index-1)   # move right
                                q_index = 3
                            elif 2 in candidate_q_index:
                                for j in range(3):
                                    empty_index = board.get_empty_index()
                                    board.swap(empty_index, empty_index - SIZE)  # move down
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index - 1)  # move right
                                q_index = 2
                        if quadrant == 2:
                            q_index = random.choice(candidate_q_index)
                        if quadrant == 3:
                            if 4 in candidate_q_index:
                                q_index = 4
                            elif 1 in candidate_q_index:
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index+1)  # move left
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index-SIZE)   # move down
                                q_index = 1
                            elif 2 in candidate_q_index:
                                for j in range(3):
                                    empty_index = board.get_empty_index()
                                    board.swap(empty_index, empty_index - 1)  # move right
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index - SIZE)  # move down
                                q_index = 2
                        if quadrant == 4:
                            if 1 in candidate_q_index:
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index - SIZE)  # move down
                                q_index = 1
                            elif 3 in candidate_q_index:
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index - 1)  # move right
                                q_index = 3
                            elif 2 in candidate_q_index:
                                for j in range(4):
                                    empty_index = board.get_empty_index()
                                    board.swap(empty_index, empty_index - 1)  # move right
                                empty_index = board.get_empty_index()
                                board.swap(empty_index, empty_index - SIZE)  # move down
                                q_index = 2
                        quadrant = q_index

                    if first_time:
                        '''
                        enter here when "h" is first pressed 
                        Check which quadrant the blank position is in. 
                        Check whether it is solvable in one quadrant.
                        If not, pick the quadrant that has least amount the missing colors.
                        '''
                        first_time = False
                        #blank_in_quadrant = board.empty_in_quadrant()
                        mis_color_count = [0] #* #len(blank_in_quadrant)
                        once = False
                        #for i in [1]:#range(len(blank_in_quadrant)):
                        count_in_quadrant = board.colorcount(1)
                        print("count in quadrant")
                        print(count_in_quadrant)
                        mis_color_count[0] = 0
                        print(count_in_quadrant , count_in_goal)
                        if np.all(np.asarray(count_in_quadrant) >= np.asarray(count_in_goal)):
                            print('found all colors')
                            q_index = i
                            once = True
                            
                        # for j in range(len(count_in_quadrant)):
                        #     if count_in_goal[j] > count_in_quadrant[j]:
                        #         mis_color_count[i] += count_in_goal[j] - count_in_quadrant[j]
                        # if not once:
                        #     q_index = mis_color_count.index(min(mis_color_count))
                        #     print('Missing pieces in quadrant ', q_index, ' - ', mis_color_count[q_index])
                        quadrant = 1#blank_in_quadrant[q_index]

                    print('quadrant =', quadrant, 'Solvable in one quadrant =', once)
                    fifteen_puzzle, blank_pos = board.fifteen_eq(count_in_goal,rlist,olist,ylist,glist,blist,wlist,quadrant)
                    fifteen_seq = [element for sublist in fifteen_puzzle for element in sublist]
                    # if board.solvable(fifteen_seq, 5):
                    puzzle.board = fifteen_puzzle
                    puzzle.blankPos = blank_pos
                    aiMoves = ai.idaStar(puzzle)
                    aiMoveIndex = 0
                    # else:
                    #     print('not solvable!')

                    if quadrant == 2 and once:
                        aiMoves.extend([(0, -1)]*3)
                        #for quadrant 2, move to the right 3 times after fifteen puzzle solved

                if len(aiMoves) != 0:
                    # execute the move from ai solutions, one at a time, meanwhile remove it from the solution.
                    # so when all the moves from the ai solutions are executed, it will enter the if branch to
                    # search for next quadrant
                    aiMove = aiMoves.pop(0)
                    empty_index = board.get_empty_index()
                    new_empty_index = empty_index + SIZE*aiMove[0] + aiMove[1]
                    board.swap(empty_index, new_empty_index)
                    if board == reference:
                        aiMoveIndex = 0
                        aiMoves = []


    # display tiles
    for i in range(len(player_tiles)):
        # update tile color
        player_tiles[i].fill(board.get_color(i))
        reference_tiles[i].fill(reference.get_color(i))

        # place tiles
        startx = SPACING + TILE
        starty = SPACING + TILE
        x = (SPACING + TILE) * (i % SIZE)
        y = (SPACING + TILE) * (i // SIZE) + starty

        # draw reference tiles
        if i // SIZE != 0 and i // SIZE != SIZE - 1:
            if i % SIZE != 0 and i % SIZE != SIZE - 1:
                screen.blit(reference_tiles[i], (x, y))

        # draw player tiles
        offset = (SIZE)*TILE + (SIZE-1)*SPACING
        tile_coordinates[i] = (x + offset, y)
        screen.blit(player_tiles[i], (tile_coordinates[i]))

    # end game
    if board == reference:
        print('congrats!')
        running = False

    pygame.display.update()
    clock.tick(60)

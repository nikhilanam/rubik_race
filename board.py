import math
import random
import numpy as np

def setup_indices(size):
    indices = {i: [] for i in range(size ** 2)}

    for i in range(size ** 2):
        # set adjacent neighbors
        if i != 0:
            indices[i].append(i - 1)
            indices[i - 1].append(i)

        # set vertically adjacent neighbors
        if i / (size - 1) > 1:
            indices[i].append(i - size)
            indices[i - size].append(i)

    return indices


class Tile:
    def __init__(self, color):
        self.color = color
        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def get_color(self):
        return self.color

    def is_empty(self):
        return self.color == 'black'


class Board:
    def __init__(self, size=5):
        self.size = size
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'white']
        self.board = [Tile(i) for i in colors * (size - 1)] + [Tile('black')]
        self.indices = setup_indices(size)
        self.shuffle()

    def __str__(self):
        s = ''
        for i in range(len(self.board)):
            if self.board[i].get_color() == 'black':
                s += '  '
            else:
                s += self.board[i].get_color()[0] + ' '
            if i % self.size == self.size - 1:
                s += '\n'

        return s

    def assign_tiles(self, slist, slist_board, indices, fifteen_seq, outlist_board):
        
        color_list_quadrant = []
        outskirt_list = []
        print('slist - ',slist, ' board list - ', slist_board)
        # print('Index Map - ')
        # for x in slist_board:
        #     print(x, ':', x)
        board_value = 0
        
        for i in range(len(slist)): # [6]
            if len(slist_board) != 0: #[1,5,12,21]
                t_x = (slist_board[0]) // 5 #1//5 == 0, 5//5 == 1
                t_y = (slist_board[0]) % 5 # 1%5 == 1, 5 % 5 == 0
                min_kx, min_ky, min_k = 0, 0, 0
                min_dist = 25
                for k in slist:
                    k_x = ((k) // 5) # 6//5 = 1
                    k_y = (k) % 5 # 6%5 =1
                    dist = np.sqrt(np.square(k_x - t_x) + np.square(k_y - t_y))
                    if dist<min_dist : 
                        min_dist = dist
                        min_kx, min_ky = k_x, k_y
                        min_k = k
                
                min_x = 0
                min_dist = 25
                for x in slist_board:
                    t_x = (x) // 5
                    t_y = (x) % 5
                    dist = np.sqrt(np.square(min_kx - t_x) + np.square(min_ky - t_y))
                    if dist<min_dist : 
                        min_dist = dist
                        min_x = x
                print(f'min k {min_k}')
                fifteen_seq[min_x] = min_k
                # if min_k == 0:
                #     fifteen_seq[min_x] = 7
                # elif min_k == 1:
                #     fifteen_seq[min_x] = 8
                # elif min_k == 2:
                #     fifteen_seq[min_x] = 9
                # elif min_k == 3:
                #     fifteen_seq[min_x] = 12
                # elif min_k == 4:
                #     fifteen_seq[min_x] = 13
                # elif min_k == 5:
                #     fifteen_seq[min_x] = 14
                # elif min_k == 6:
                #     fifteen_seq[min_x] = 17
                # elif min_k == 7:
                #     fifteen_seq[min_x] = 18
                # elif min_k == 8:
                #     fifteen_seq[min_x] = 19
                color_list_quadrant.append(fifteen_seq[min_x])
                slist_board.remove(min_x)
                slist.remove(min_k)


        if len(slist) != 0:
            for x in slist:    
                outskirt_list.append(x)

        if len(slist_board) != 0:    
            for x in slist_board:    
                # color_list_quadrant.append(fifteen_seq[indices[x]])
                outlist_board.append(x)
        print('fifteen_seq, color_list_quadrant, outlist_board, outskirt_list')
        print(fifteen_seq, color_list_quadrant, outlist_board, outskirt_list)
        return fifteen_seq, color_list_quadrant, outlist_board, outskirt_list

    def assign_outskirt(self, outskirt, outlist_board, indices, fifteen_seq):
        outskirt_assigned = 0

        print('outskirt list - ',outskirt, ' outskirt board list - ', outlist_board)

        for i in outlist_board:
            if len(outlist_board) != 0:
                t_x = (outlist_board[0]) // 4
                t_y = (outlist_board[0]) % 4
                min_kx, min_ky, min_k = 0, 0, 0
                min_dist = 16
                for k in outskirt:
                    k_x = (k-1)//4
                    k_y = (k-1)%4
                    dist = np.sqrt(np.square(k_x - t_x) + np.square(k_y - t_y))
                    if dist<min_dist : 
                        min_dist = dist
                        min_kx, min_ky = k_x, k_y
                        min_k = k
                
                min_x = 0
                min_dist = 16
                for x in outlist_board:
                    t_x = (x) // 4
                    t_y = (x) % 4
                    dist = np.sqrt(np.square(min_kx - t_x) + np.square(min_ky - t_y))
                    if dist<min_dist : 
                        min_dist = dist
                        min_x = x
                # min_k=1
                # min_x = i
                fifteen_seq[min_x] = min_k
                outlist_board.remove(min_x)
                outskirt.remove(min_k)
                outskirt_assigned += 1
        print(f'outskirt assign {fifteen_seq}, {outskirt_assigned}')
        return fifteen_seq, outskirt_assigned

    def colorcount_target(self, indices):
        # return the count of different colors in the goal and also their corresponding indices
        count = [0, 0, 0, 0, 0, 0]    # in the sequence of r o y g b w
        rlist_board = []
        olist_board = []
        ylist_board = []
        glist_board = []
        blist_board = []
        wlist_board = []
        print('colorcount_target',indices)
        for i in indices:
            i = i
            s = self.board[i].get_color()
            print('colorcount_target')
            print(s)
            if s == 'red':
                count[0] += 1
                print(f'red {i}')
                rlist_board.append(i)
            elif s == 'orange':
                count[1] += 1
                print(f'orange {i}')
                olist_board.append(i)
            elif s == 'yellow':
                count[2] += 1
                print(f'yellow {i}')
                ylist_board.append(i)
            elif s == 'green':
                count[3] += 1
                print(f'green {i}')
                glist_board.append(i)
            elif s == 'blue':
                count[4] += 1
                print(f'blue {i}')
                blist_board.append(i)
            elif s == 'white':
                print(f'white {i}')
                count[5] += 1
                wlist_board.append(i)
        return count, rlist_board, olist_board, ylist_board, glist_board, blist_board, wlist_board


    def colorcount(self, quadrant=1):
        # return the count of each color based on different quadrant parameters
        count = [0, 0, 0, 0, 0, 0]    # in the sequence of r o y g b w
        indices1 = [1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19,20,21,22,23,24]
        # indices2 = list(map(lambda x: x-1,  indices1))
        # indices3 = list(map(lambda x: x+5,  indices2))
        # indices4 = list(map(lambda x: x+1,  indices3))
        # if quadrant == 1:
        #     countindices = indices1
        # elif quadrant == 2:
        #     countindices = indices2
        # elif quadrant == 3:
        #     countindices = indices3
        # elif quadrant == 4:
        #     countindices = indices4
        for i in indices1:
            s = self.board[i].get_color()[0]
            if s == 'r':
                count[0] += 1
            elif s == 'o':
                count[1] += 1
            elif s == 'y':
                count[2] += 1
            elif s == 'g':
                count[3] += 1
            elif self.board[i].get_color() == 'blue':
                count[4] += 1
            elif s == 'w':
                count[5] += 1
        return count

    def get_color(self, index):
        return self.board[index].get_color()

    def get_empty_index(self):
        for i in range(len(self.board)):
            if self.board[i].is_empty():
                return i
        return None

    def empty_in_quadrant(self):
        # return the list of quadrant(s) that contains the blank
        empty_index = self.get_empty_index()
        quadrant = []
        indices1 = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21,22]
        # indices2 = list(map(lambda x: x - 1, indices1))
        # indices3 = list(map(lambda x: x + 5, indices2))
        # indices4 = list(map(lambda x: x + 1, indices3))
        # if (empty_index in indices1):
        #     quadrant.append(1)
        # if (empty_index in indices2):
        #     quadrant.append(2)
        # if (empty_index in indices3):
        #     quadrant.append(3)
        # if (empty_index in indices4):
        #     quadrant.append(4)
        return [1]


    def update(self, index):
        empty_index = self.get_empty_index()
        if self.is_move(index):
            if empty_index in self.indices[index]:
                self.swap(empty_index, index)
            else:
                self.move_row(index)

    def shuffle(self, moves=1000):
        for i in range(moves):
            empty_index = self.get_empty_index()
            index = random.choice(self.indices[empty_index])
            self.update(index)

    def get_interior_tiles(self):
        b = []#[7,8,9,12,13,14,17,18,19]
        for i in range(len(self.board)):
            if i // self.size != 0 and i // self.size != self.size - 1:
                if i % self.size != 0 and i % self.size != self.size - 1:
                    b.append(self.board[i])
        return b

    def move_row(self, tile_index):
        row = []
        empty_index = self.get_empty_index()
        start = min(tile_index, empty_index)
        end = max(tile_index, empty_index)
        backwards = True
        if start == empty_index:
            backwards = False
        if (end - start) < self.size:
            row = [i for i in range(start, end+1)]
        else:
            row = [i for i in range(start, end+1, self.size)]
        if backwards:
            for i in reversed(range(len(row) - 1)):
                self.swap(row[i], row[i - 1])
        else:
            for i in range(len(row)-1):
                self.swap(row[i], row[i+1])


    def swap(self, index1, index2):
        self.board[index1], self.board[index2] = self.board[index2], self.board[index1]

    def is_move(self, index):
        empty_space = self.get_empty_index()
        if index in self.indices:
            # if in same row
            if index // self.size == empty_space // self.size:
                return True
            # if in same column
            elif index % self.size == empty_space % self.size:
                return True
        return False

    def __eq__(self, other):
        tiles1 = self.get_interior_tiles()
        tiles2 = other.get_interior_tiles()
        for i in range(len(tiles1)):
            if tiles1[i].get_color() != tiles2[i].get_color():
                return False
        return True

    def fifteen_eq(self,count_in_goal,rlist,olist,ylist,glist,blist,wlist,quadrant):
        '''
        return a fifteen puzzle and the corresponding blank position
        '''
        rlist, olist, ylist, glist, blist, wlist = self.colorlist_map(rlist,olist,ylist,glist,blist,wlist,quadrant)
        color_list = [rlist, olist, ylist, glist, blist, wlist]
        count_in_quadrant = self.colorcount(quadrant)

        # mapping the indices of a rubik's race board (5x5) to the indices of a fifteen puzzle board (4x4) based on
        # different quadrants
        indices =[0,1,2,3,4,5,6, 7, 8, 9,10,11, 12, 13, 14,15,16, 17, 18, 19,20,21,22,23,24]
        #indices1 = inner_indices + [1, 2, 3, 4, 9, 14, 19]
        # if quadrant == 1:
        #     indices = indices1
        #     index_map = {1:0, 2:1, 3:2, 4:3, 6:4, 7:5, 8:6, 9:7, 11:8, 12:9, 13:10, 14:11, 16:12, 17:13, 18:14, 19:15}
        #     outskirt = [1, 2, 3, 4, 8, 12]
        #     blank_offset = [0, -1]
        # elif quadrant == 2:
        #     indices = list(map(lambda x: x - 1, indices1))
        #     index_map = {0: 0, 1: 1, 2: 2, 3: 3, 5: 4, 6: 5, 7: 6, 8: 7, 10: 8, 11: 9, 12: 10, 13: 11, 15: 12, 16: 13,
        #                  17: 14, 18: 15}
        #     outskirt = [1, 2, 3, 4, 5, 9]
        #     blank_offset = [0, 0]
        # elif quadrant == 3:
        #     indices = list(map(lambda x: x + 4, indices1))
        #     index_map = {5: 0, 6: 1, 7: 2, 8: 3, 10: 4, 11: 5, 12: 6, 13: 7, 15: 8, 16: 9, 17: 10, 18: 11, 20: 12, 21: 13,
        #                  22: 14, 23: 15}
        #     outskirt = [1, 5, 9, 13, 14, 15]
        #     blank_offset = [-1, 0]
        # elif quadrant == 4:
        #     indices = list(map(lambda x: x + 5, indices1))
        #     index_map = {6: 0, 7: 1, 8: 2, 9: 3, 11: 4, 12: 5, 13: 6, 14: 7, 16: 8, 17: 9, 18: 10, 19: 11, 21: 12,
        #                  22: 13, 23: 14, 24: 15}
        #     outskirt = [4, 8, 12, 13, 14, 15]
            # blank_offset = [-1, -1]

        # When the quadrant does not contain all the needed color pieces, append the indices of the missing color tiles
        # to the outskirt list.
        # if not np.all(np.asarray(count_in_quadrant) >= np.asarray(count_in_goal)):
        #     for i in range(len(count_in_goal)):
        #         if count_in_goal[i] > count_in_quadrant[i]:
        #             outskirt.extend(color_list[i][count_in_quadrant[i]:])
        
        # index_map = {1:0, 2:1, 3:1, 4:1, 6:1, 7:2, 8:, 9:7, 11:8, 12:9, 13:10, 14:11, 16:12, 17:13, 18:14, 19:15}
        outskirt = [1, 2, 3, 4, 5, 6,10, 11, 15, 16, 20, 21, 22, 23, 24]
        blank_offset = [0, 0]
        assigned = [0, 0, 0, 0, 0, 0]   # r, o, y, g, b, w
        outlist_board = []
        fifteen_seq = np.ones((25), dtype=np.int32)
        color_list_quadrant = [[], [], [], [], [], []]

        # Assigning indices to the tiles in the quadrant. The color tiles in the quadrant that are needed in the goal
        # will be assigned their corresponding indices first. Then outskirt indices will be assigned to the rest of the
        # tiles. Position of the blank space will be recorded.
        print(self)
        count_board, rlist_board, olist_board, ylist_board, glist_board, blist_board, wlist_board = self.colorcount_target(indices)
        print(f'rlist, rlist board {rlist} {rlist_board}')
        fifteen_seq, color_quadrant, outlist_board, outskirt_list = self.assign_tiles(rlist, rlist_board, indices, fifteen_seq, outlist_board)
        color_list_quadrant[0] = color_quadrant
        print('ColorList Quadrant - ', color_quadrant)
        print(f'red fifteen_seq, color_quadrant, outlist_board, outskirt_list, {fifteen_seq}, {color_quadrant}, {outlist_board}, {outskirt_list}')
        #outskirt.extend(outskirt_list)
        fifteen_seq, color_quadrant, outlist_board, outskirt_list = self.assign_tiles(olist, olist_board, indices, fifteen_seq, outlist_board)
        color_list_quadrant[1] = color_quadrant
        #outskirt.extend(outskirt_list)
        print(f'orange fifteen_seq, color_quadrant, outlist_board, outskirt_list, {fifteen_seq}, {color_quadrant}, {outlist_board}, {outskirt_list}')
        fifteen_seq, color_quadrant, outlist_board, outskirt_list = self.assign_tiles(ylist, ylist_board, indices, fifteen_seq, outlist_board)
        color_list_quadrant[2] = color_quadrant
        #outskirt.extend(outskirt_list)
        print(f'yellow fifteen_seq, color_quadrant, outlist_board, outskirt_list, {fifteen_seq}, {color_quadrant}, {outlist_board}, {outskirt_list}')
        fifteen_seq, color_quadrant, outlist_board, outskirt_list = self.assign_tiles(glist, glist_board, indices, fifteen_seq, outlist_board)
        color_list_quadrant[3] = color_quadrant
        #outskirt.extend(outskirt_list)
        print(f'green fifteen_seq, color_quadrant, outlist_board, outskirt_list, {fifteen_seq}, {color_quadrant}, {outlist_board}, {outskirt_list}')
        fifteen_seq, color_quadrant, outlist_board, outskirt_list = self.assign_tiles(blist, blist_board, indices, fifteen_seq, outlist_board)
        color_list_quadrant[4] = color_quadrant
        #outskirt.extend(outskirt_list)
        print(f'blue fifteen_seq, color_quadrant, outlist_board, outskirt_list, {fifteen_seq}, {color_quadrant}, {outlist_board}, {outskirt_list}')
        fifteen_seq, color_quadrant, outlist_board, outskirt_list = self.assign_tiles(wlist, wlist_board, indices, fifteen_seq, outlist_board)
        color_list_quadrant[5] = color_quadrant
        #outskirt.extend(outskirt_list)
        print(f'white fifteen_seq, color_quadrant, outlist_board, outskirt_list, {fifteen_seq}, {color_quadrant}, {outlist_board}, {outskirt_list}')
        print(f'color_list_quadrant {color_list_quadrant}')
        outlist_board_copy = outlist_board[:]
        #print(f'outskirt after extend {outskirt}')
       # fifteen_seq, outskirt_assigned = self.assign_outskirt(outskirt, outlist_board, indices, fifteen_seq)
        print(f'outlist_board_copy {outlist_board_copy}, fifteen_seq {fifteen_seq}, outskirt {outskirt}')
        # for x in outlist_board_copy:
        #     print(x)
        #     s = self.board[x].get_color()
        #     print(s)
        #     if s == 'red':
        #         color_list_quadrant[0].append(fifteen_seq[x])
        #     elif s == 'orange':
        #         color_list_quadrant[1].append(fifteen_seq[x])
        #     elif s == 'yellow':
        #         color_list_quadrant[2].append(fifteen_seq[x])
        #     elif s == 'green':
        #         color_list_quadrant[3].append(fifteen_seq[x])
        #     elif s == 'blue':
        #         color_list_quadrant[4].append(fifteen_seq[x])
        #     elif s == 'white':
        #         color_list_quadrant[5].append(fifteen_seq[x])
        
        
        # print(color_list_quadrant)
        # #check if it makes sense    
        for x in indices:
            s = self.board[x].get_color()
            
            if s == 'black':
                print(x)
                fifteen_seq[x] = 0
                blank_row = (x // self.size) + blank_offset[0]
                blank_column = (x % self.size) + blank_offset[1]
                blank_pos = (blank_row, blank_column)
        
        # print(self)
        
        print('Fifteen Seq - ', fifteen_seq)
        # If the fifteen puzzle is not solvable, pick a pair of same color in the quadrant and swap their positions.
        # Only swap once, this should change the parity of the sequence (odd->even, even->odd) and makes it solvable.
        # if not self.solvable(fifteen_seq, 5):
        #     for i in range(len(count_in_quadrant)):
        #         if count_in_quadrant[i] >= 2:
        #             print('Swapped  - ', i)
        #             pos1 = fifteen_seq.index(color_list_quadrant[i][0])
        #             pos2 = fifteen_seq.index(color_list_quadrant[i][1])
        #             fifteen_seq[pos1], fifteen_seq[pos2] = fifteen_seq[pos2], fifteen_seq[pos1]
        #             break

        # cast the fifteen puzzle sequence into a list of four rows. (to match the fifteen puzzle format)
        fifteen_puzzle = [[],[],[],[],[]]
        for i in range(5):
            for j in range(5):
                fifteen_puzzle[i].append(fifteen_seq[i*5+j])
        #fifteen_puzzle = (fifteen_seq[0:5], fifteen_seq[5:10], fifteen_seq[10:15], fifteen_seq[15:20])
        print('Goal indexes - ', fifteen_puzzle)
        # print(self.get_empty_index())
        return fifteen_puzzle, blank_pos

    def solvable(self, a, n):  # assumed sorted(a) == range(n*n)
        # check the solvability of a N-puzzle
        a = list(a)  # copy
        h = a.index(0)  # locate hole
        a.pop(h)  # remove hole
        print('inside solvable')
        print(a)
        t = n & 1 or h // n  # handle odd or even nxn board
        for i, x in enumerate(a, 1):
            print(f'i, x {i}, {x}')
            if x != i:
                print(f'a inxex, i {a.index(i, i)}, {i}')
                a[a.index(i, i)] = x
                t += 1  # add selection sort swaps
        return t & 1 != 0

    def colorlist_map(self,rlist,olist,ylist,glist,blist,wlist,quadrant):
        # return the indices of each color based on different quadrants
        rlist = self.scolor_map(rlist, quadrant)
        olist = self.scolor_map(olist, quadrant)
        ylist = self.scolor_map(ylist, quadrant)
        glist = self.scolor_map(glist, quadrant)
        blist = self.scolor_map(blist, quadrant)
        wlist = self.scolor_map(wlist, quadrant)
        return rlist, olist, ylist, glist, blist, wlist

    def scolor_map(self,slist,quadrant):
        # map the indices of the goal (0-8) to the indices of the 5 by 5 board based on different quadrants
        offset = [7,9,11]
        # if quadrant == 1:
        #     offset = [0,0,0]
        # if quadrant == 2:
        #     offset = [6, 7, 7]
        # if quadrant == 3:
        #     offset = [2, 3, 4]
        # if quadrant == 4:
        #     offset = [1, 2, 3]
        for i in range(len(slist)):
            if slist[i] < 3:
                slist[i] += offset[0]
            elif slist[i] < 6:
                slist[i] += offset[1]
            else:
                slist[i] += offset[2]
        return slist

class Reference(Board):
    def __init__(self, size=5):
        super().__init__(size)
        self.shuffle()

    def shuffle(self, moves=100):
        super().shuffle(moves)
        interior = self.get_interior_tiles()
        for tile in interior:
            if tile.get_color() == 'black':
                empty_index = self.get_empty_index()
                self.swap(empty_index, 0)

    def __str__(self):
        s = ''
        tiles = self.get_interior_tiles()
        size = math.sqrt(len(tiles))
        for i in range(len(tiles)):
            s += tiles[i].get_color()[0] + ' '
            if i % size == size - 1:
                s += '\n'
        return s

    def colorcount(self):
        # return the count of different colors in the goal and also their corresponding indices
        tiles = self.get_interior_tiles()
        count = [0, 0, 0, 0, 0, 0]    # in the sequence of r o y g b w
        rlist = []
        olist = []
        ylist = []
        glist = []
        blist = []
        wlist = []
        for i in range(len(tiles)):
            s = tiles[i].get_color()[0]
            if s == 'r':
                count[0] += 1
                rlist.append(i)
            elif s == 'o':
                count[1] += 1
                olist.append(i)
            elif s == 'y':
                count[2] += 1
                ylist.append(i)
            elif s == 'g':
                count[3] += 1
                glist.append(i)
            elif s == 'b':
                count[4] += 1
                blist.append(i)
            elif s == 'w':
                count[5] += 1
                wlist.append(i)
        return count, rlist, olist, ylist, glist, blist, wlist



if __name__ == '__main__':
    running = True

    board = Board()
    reference = Reference()

    while running:

        print('-----------board-----------')
        print(board)
        print('-----------reference-----------')
        print(reference)

        move = input('choose index to move (0-24):')
        board.update(int(move))

        if board.get_interior_tiles() == reference.get_interior_tiles():
            running = False
            print('congratulations! you won!')

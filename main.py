import model
import ai
import csv


class Research():
     
    def main(self):
        self.result = []
        self.solving_time = []
        self.solving_moves = []

        for _ in range(0,50):
            puzzle = model.Puzzle(boardSize=5)
            self.solution, self.time, self.max_depth = ai.idaStar(puzzle)
            self.board = model.Puzzle().board
            count = self.check_complexity(size=5)
            self.solving_time.append(self.time)
            self.solving_moves.append(len(self.solution) if self.solution else None)
            if self.solution:
                print("Solution found:")
                print(self.solution)
                self.result.append((self.board, len(self.solution), self.time, count, self.max_depth))
            else:
                print("No solution available.")
                self.result.append((self.board, None, None, None, None))

        average_time = sum(self.solving_time) / len(self.solving_time)
        max_time = max(self.solving_time)
        average_solution_length = sum(filter(None, self.solving_moves)) / len(self.solving_moves)
        max_solution_length = max(self.solving_moves)

        print(f'Average Solving Time:{average_time}\nMaximum Solving Time:{max_time}\nAverage Moves Taken:{average_solution_length} \
              \nMaximum Moves Taken:{max_solution_length}')


    def check_complexity(self, size=5):
        # Middle 3x3 square indices
        indices = [6, 7, 8, 11, 12, 13, 16, 17, 18]
        count = 0

        for index in indices:
            row = index // size
            col = index % size
            if self.board[row][col] == index+1:
                count += 1
        
        return count
    
    def create_csv(self, filename='puzzle_solving_data.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Board', 'Moves', 'Time','Mid_Target_Tiles','Max_Depth'])
            for result in self.result:
                writer.writerow(result)
            print('Here')

           
if __name__ == "__main__":
    m = model.Puzzle()
    res = Research()
    res.main()
    res.create_csv()


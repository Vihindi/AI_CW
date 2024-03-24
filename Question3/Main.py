import tkinter as tk
from queue import PriorityQueue
from Maze import Maze, depth_first_search, a_star_search

class MazeGUI:
    def __init__(self, master, maze):
        self.master = master
        self.master.title("Maze Solver")
        self.maze = maze
        self.cell_size = 40  # Adjust the cell size based on your preference
        self.canvas = tk.Canvas(master, width=maze.columns * self.cell_size, height=maze.rows * self.cell_size)
        self.canvas.pack()

        self.run_dfs_button = tk.Button(master, text="Run DFS", command=self.run_dfs)
        self.run_dfs_button.pack()

        self.run_a_star_button = tk.Button(master, text="Run A*", command=self.run_a_star)
        self.run_a_star_button.pack()

        self.draw_maze()

    def draw_maze(self):
        for i in range(self.maze.rows):
            for j in range(self.maze.columns):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                if self.maze.maze[i][j] == 'S':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='red')
                elif self.maze.maze[i][j] == 'G':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green')
                elif self.maze.maze[i][j] == 'X':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')

    def draw_path(self, path, color):
        for node in path:
            x, y = node
            x1, y1 = x * self.cell_size, y * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def run_dfs(self):
        dfs_path, time, visited = depth_first_search(self.maze)
        print("VIsited list in DFS",visited)
        print("Time of DFS",time)
        self.draw_path(dfs_path, 'yellow')

    def run_a_star(self):
        a_star_path, time, visited = a_star_search(self.maze)
        print("VIsited list in A*", visited)
        print("Time of A*", time)
        self.draw_path(a_star_path, 'orange')

    def run(self):
        self.master.mainloop()

# Usage example
if __name__ == "__main__":
    root = tk.Tk()

    maze = Maze()
    maze_gui = MazeGUI(root, maze)

    maze_gui.run()

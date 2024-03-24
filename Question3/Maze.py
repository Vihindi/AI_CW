import random
from queue import PriorityQueue


class Maze:
    def __init__(self):
        self.rows = 6
        self.columns = 6
        self.maze = [[''] * self.columns for _ in range(self.rows)]
        self.start_node = None
        self.goal_node = None
        self.barrier_nodes = []
        self.generate_maze()

    def generate_maze(self):
        # Randomly select starting node
        self.start_node = self.get_random_node(0, 11)

        # Randomly select goal node
        self.goal_node = self.get_random_node(24, 35)

        # Randomly select barrier nodes
        while len(self.barrier_nodes) < 4:
            barrier = self.get_random_node(0, 35)
            if (barrier != self.start_node) and (barrier != self.goal_node) and (barrier not in self.barrier_nodes):
                self.barrier_nodes.append(barrier)

        # Populate maze
        for i in range(self.rows):
            for j in range(self.columns):
                node = (j, i)
                if node == self.start_node:
                    self.maze[i][j] = 'S'
                elif node == self.goal_node:
                    self.maze[i][j] = 'G'
                elif node in self.barrier_nodes:
                    self.maze[i][j] = 'X'
                else:
                    self.maze[i][j] = '.'

    def get_random_node(self, start, end):
        x = random.randint(start % self.columns, end % self.columns)
        y = random.randint(start // self.columns, end // self.columns)
        return x, y

    def is_valid_move(self, x, y):
        return 0 <= x < self.columns and 0 <= y < self.rows and (x, y) not in self.barrier_nodes

    def print_maze(self):
        for row in self.maze:
            print(' '.join(row))

    #Print mazr
    def print_maze1(self, path):
        for i in range(6):
            for j in range(6):
                if any(k == (j, i) for k in path):
                    if (j, i) == path[0] or (j, i) == path[-1]:
                        print("\033[92m*\033[0m", end=" ")  # Green for first and last stars
                    else:
                        print("\033[91m*\033[0m", end=" ")  # Red for other stars
                else:
                    print(self.maze[i][j], end=" ")
            print()

    #Calculate manhattan distance
    def manhattan_distance(self, node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def heuristic_cost(self, current_node):
        return self.manhattan_distance(current_node, self.goal_node)


#DFS algorithm
def depth_first_search(maze):
    # Initialize the stack with the start node
    stack = [(maze.start_node, [maze.start_node])]
    # Set the initial time to 0 minutes
    initial_time = 0
    # Set to keep track of visited nodes
    visited = set()

    # Continue the search as long as there are nodes in the stack
    while stack:
        # Pop the top node and its path from the stack
        current_node, path = stack.pop()

        # Check if the goal node is reached
        if current_node == maze.goal_node:
            # Print the visited nodes and return the path, total time, and visited set
            return path, initial_time, visited

        # Check if the current node has not been visited
        if current_node not in visited:
            # Mark the current node as visited
            visited.add(current_node)
            initial_time += 1  # Add 1 minute for each visited node

            # Generate neighbors for the current node
            neighbors = [
                (current_node[0] + dx, current_node[1] + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (dx != 0 or dy != 0) and maze.is_valid_move(current_node[0] + dx, current_node[1] + dy)
            ]
            # Sort neighbors in increasing order and reverse to process in the order of [-1, 0, 1]
            neighbors.sort()  # Process neighbors in increasing order
            neighbors.reverse()

            for neighbor in neighbors:
                # Check if the neighbor has not been visited
                if neighbor not in visited:
                    # Add the neighbor and the updated path to the stack
                    stack.append((neighbor, path + [neighbor]))

    return None, 0

# A* search algorithm
def a_star_search(maze):
    # Initialize priority queue
    priority_queue = PriorityQueue()
    # Get start and goal nodes from the maze
    start_node = maze.start_node
    goal_node = maze.goal_node
    visited = set()

    # Put the start node and its path with priority 0 into the priority queue
    priority_queue.put((0, start_node, [start_node]))

    # Continue the search as long as the priority queue is not empty
    while not priority_queue.empty():
        # Get the node with the highest priority (the lowest cost)
        _, current_node, path = priority_queue.get()

        # Check if the goal node is reached
        if current_node == goal_node:
            return path, len(path) - 1, visited

        # Check if the current node has not been visited
        if current_node not in visited:
            visited.add(current_node)

            # Generate neighbors for the current node
            neighbors = [
                (current_node[0] + dx, current_node[1] + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (dx != 0 or dy != 0) and maze.is_valid_move(current_node[0] + dx, current_node[1] + dy)
            ]

            for neighbor in neighbors:
                # Check if the neighbor has not been visited
                if neighbor not in visited:
                    # Create a new path by extending the current path with the neighbor
                    new_path = path + [neighbor]
                    # Calculate the cost (path length + heuristic cost)
                    cost = len(new_path) - 1 + maze.heuristic_cost(neighbor)
                    # Put the neighbor, new path, and cost into the priority queue
                    priority_queue.put((cost, neighbor, new_path))


    return None, 0, visited

def main():
    maze = Maze()

    print("Generated Maze:")
    maze.print_maze()

    print()
    final_path,new_time,visitedList = depth_first_search(maze)
    maze.print_maze1(final_path)
    print()
    path,time,visitedList2= a_star_search(maze)
    maze.print_maze1(path)


    print("\nDFS Results:")
    if final_path:
        print("Visited Nodes:", len(final_path))
        print("Time: ",new_time,"minutes")
        print("Final Path:", final_path)
        print("Visited list",visitedList)
    else:
        print("Goal not reachable")

    print()
    print("\nA* Results:")
    if final_path:
        print("Visited Nodes:", len(path))
        print("Time: ", time, "minutes")
        print("Final Path:", path)
        print("Visited list", visitedList2)
    else:
        print("Goal not reachable")

if __name__ == "__main__":
    main()

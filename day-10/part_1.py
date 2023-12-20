'''
The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
'''
from pprint import pprint
from typing import Optional
from collections import deque

def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample.txt' if use_sample else 'input.txt'
    with open(f'day-10/{filename}') as f:
        return [line.strip() for line in f.readlines()]

'''
https://en.wikipedia.org/wiki/Depth-first_search
procedure DFS_iterative(G, v) is
    let S be a stack
    S.push(v)
    while S is not empty do
        v = S.pop()
        if v is not labeled as discovered then
            label v as discovered
            for all edges from v to w in G.adjacentEdges(v) do 
                S.push(w)
'''

def is_cyclic(
    g: dict[tuple[int,int], set[tuple[int,int]]], 
    v: tuple[int, int],
) -> bool:
    stack = [v]
    discovered = set()
    parent = {
        v: None
    }
    while len(stack) > 0:
        v = stack.pop()
        if v not in discovered:
            discovered.add(v)
            for neighbor in g[v]:
                # back edge (apparently)
                if neighbor in discovered and parent[v] != neighbor:
                    return True
                stack.append(neighbor)
                parent[neighbor] = v
    return False



# def is_cycle(
#     g: dict[tuple[int,int], set[tuple[int,int]]], 
#     v: tuple[int,int], 
#     visited: Optional[set[tuple[int,int]]]=None, 
#     parent: Optional[tuple[int,int]]=None
# ):
#     if visited is None:
#         visited = set()
#     visited.add(v)
#     for neighbor in g[v]:
#         if neighbor not in visited:
#             if(is_cycle(g, neighbor, visited, v)):
#                 return True
#         elif parent != neighbor:
#             return True
#     return False

def test_is_cycic() -> None:
    # Actual sample input
    graph = {
        (1, 1): {(1, 2), (2, 1)},
        (1, 2): {(1, 1), (1, 3)},
        (1, 3): {(2, 3), (1, 2)},
        (2, 1): {(3, 1), (1, 1)},
        (2, 3): {(3, 3), (1, 3)},
        (3, 1): {(3, 2), (2, 1)},
        (3, 2): {(3, 1), (3, 3)},
        (3, 3): {(2, 3), (3, 2)}
    }
    assert is_cyclic(graph, (1, 1))
    # Sample input if we interpret S as -
    graph = {
        (1, 1): {(1, 2)},
        (1, 2): {(1, 1), (1, 3)},
        (1, 3): {(2, 3), (1, 2)},
        (2, 1): {(3, 1)},
        (2, 3): {(3, 3), (1, 3)},
        (3, 1): {(3, 2), (2, 1)},
        (3, 2): {(3, 1), (3, 3)},
        (3, 3): {(2, 3), (3, 2)}
    }
    assert not is_cyclic(graph, (1, 1))
# test_is_cycic()

_CONNECTS_UP_SYMBOLS = {'|', 'L', 'J'}
_CONNECTS_DOWN_SYMBOLS = {'|', '7', 'F'}
_CONNECTS_LEFT_SYMBOLS = {'-', 'J', '7'}
_CONNECTS_RIGHT_SYMBOLS = {'-', 'L', 'F'}

# Construct an adjacency set for each node
def construct_graph(input_lines: list[str]) -> tuple[
    dict[
        tuple[int,int], 
        set[tuple[int,int]]
    ], 
    tuple[int, int], 
    str
]:
    def connects_up(r, c):
        return input_lines[r][c] in _CONNECTS_UP_SYMBOLS
    
    def connects_down(r, c):
        return input_lines[r][c] in _CONNECTS_DOWN_SYMBOLS
    
    def connects_left(r, c):
        return input_lines[r][c] in _CONNECTS_LEFT_SYMBOLS
    
    def connects_right(r, c):
        return input_lines[r][c] in _CONNECTS_RIGHT_SYMBOLS
    
    def add_neighbor(g, node, neighbor):
        if g[node] is None:
            g[node] = {neighbor}
        else:
            g[node].add(neighbor)
    
    def add_above_neighbor(g, r, c):
        if r - 1 >= 0 and connects_down(r-1, c):
            add_neighbor(g,(r, c), (r-1, c))

    def add_below_neighbor(g, r, c):
        if r + 1 < len(input_lines) and connects_up(r+1, c):
            add_neighbor(g,(r, c), (r+1, c))

    def add_left_neighbor(g, r, c):
        if c - 1 >= 0 and connects_right(r, c-1):
           add_neighbor(g,(r, c), (r, c-1))

    def add_right_neighbor(g, r, c):
        if c + 1 < len(input_lines[0]) and connects_left(r, c + 1):
            add_neighbor(g,(r, c), (r, c+1))

    s_row = None
    s_col = None 
    for row in range(len(input_lines)):
        for col in range(len(input_lines[row])):
            if input_lines[row][col] == 'S':
                s_row = row
                s_col = col
                break
        if s_row is not None:
            break
    original_s_row = input_lines[s_row]

    for possible_S_symbol in _CONNECTS_UP_SYMBOLS.union(_CONNECTS_DOWN_SYMBOLS).union(_CONNECTS_RIGHT_SYMBOLS).union(_CONNECTS_LEFT_SYMBOLS):
        input_lines[s_row] = original_s_row.replace('S', possible_S_symbol)
        candidate_graph = {
            (row, col): None
            for row in range(len(input_lines))
            for col in range(len(input_lines[0]))
        }
        for row in range(len(input_lines)):
            for col in range(len(input_lines[row])):
                symb = input_lines[row][col]
                if symb in _CONNECTS_UP_SYMBOLS:
                    add_above_neighbor(candidate_graph, row, col)
                if symb in _CONNECTS_DOWN_SYMBOLS:
                    add_below_neighbor(candidate_graph, row, col)
                if symb in _CONNECTS_LEFT_SYMBOLS:
                    add_left_neighbor(candidate_graph, row, col)
                if symb in _CONNECTS_RIGHT_SYMBOLS:
                    add_right_neighbor(candidate_graph, row, col)
        candidate_graph = {
            node: node_neighbors
            for node, node_neighbors in candidate_graph.items()
            if node_neighbors is not None
        }
        cycle_at_s = is_cyclic(candidate_graph, (s_row, s_col)) if (s_row, s_col) in candidate_graph else False
        if cycle_at_s:
            print(f'Cycle at S ({s_row}, {s_col}) when S is {possible_S_symbol}')
            return candidate_graph, (s_row, s_col), possible_S_symbol

    

def test_construct_graph() -> None:
    graph, start_node, s_char = construct_graph(get_input_lines(use_sample=True))
    assert graph == {
        (0, 2): {(1, 2), (0, 3)},
        (0, 3): {(0, 2), (1, 3)},
        (1, 1): {(1, 2), (2, 1)},
        (1, 2): {(1, 1), (0, 2)},
        (1, 3): {(2, 3), (0, 3)},
        (2, 0): {(2, 1), (3, 0)},
        (2, 1): {(1, 1), (2, 0)},
        (2, 3): {(2, 4), (1, 3)},
        (2, 4): {(2, 3), (3, 4)},
        (3, 0): {(4, 0), (2, 0)},
        (3, 1): {(3, 2), (4, 1)},
        (3, 2): {(3, 1), (3, 3)},
        (3, 3): {(3, 2), (3, 4)},
        (3, 4): {(2, 4), (3, 3)},
        (4, 0): {(4, 1), (3, 0)},
        (4, 1): {(3, 1), (4, 0)}
    }
    assert start_node == (2, 0)
# test_construct_graph()

'''
 1  procedure BFS(G, root) is
 2      let Q be a queue
 3      label root as explored
 4      Q.enqueue(root)
 5      while Q is not empty do
 6          v := Q.dequeue()
 7          if v is the goal then
 8              return v
 9          for all edges from v to w in G.adjacentEdges(v) do
10              if w is not labeled as explored then
11                  label w as explored
12                  w.parent := v
13                  Q.enqueue(w)
'''

def get_distances(
    s: tuple[int, int], 
    graph: dict[tuple[int,int], set[tuple[int,int]]]
) -> dict[tuple[int, int], int]:
    dist = 0
    dists = dict()
    parents = dict()
    queue = deque([s])
    while len(queue) > 0:
        v = queue.popleft()
        dists[v] = dists[parents[v]] + 1 if v != s else 0
        for neighbor in graph[v]:
            if not dists.get(neighbor):
                parents[neighbor] = v
                queue.append(neighbor)
        dist += 1
    return dists

def test_get_distances() -> None:
    graph = {
        (0, 2): {(1, 2), (0, 3)},
        (0, 3): {(0, 2), (1, 3)},
        (1, 1): {(1, 2), (2, 1)},
        (1, 2): {(1, 1), (0, 2)},
        (1, 3): {(2, 3), (0, 3)},
        (2, 0): {(2, 1), (3, 0)},
        (2, 1): {(1, 1), (2, 0)},
        (2, 3): {(2, 4), (1, 3)},
        (2, 4): {(2, 3), (3, 4)},
        (3, 0): {(4, 0), (2, 0)},
        (3, 1): {(3, 2), (4, 1)},
        (3, 2): {(3, 1), (3, 3)},
        (3, 3): {(3, 2), (3, 4)},
        (3, 4): {(2, 4), (3, 3)},
        (4, 0): {(4, 1), (3, 0)},
        (4, 1): {(3, 1), (4, 0)}
    }
    distances = get_distances((2, 0), graph)
    print('DISTANCES')
    pprint(distances)
    assert distances == {
        (0, 2): 4,
        (0, 3): 5,
        (1, 1): 2,
        (1, 2): 3,
        (1, 3): 6,
        (2, 0): 0,
        (2, 1): 1,
        (2, 3): 7,
        (2, 4): 8,
        (3, 0): 1,
        (3, 1): 4,
        (3, 2): 5,
        (3, 3): 6,
        (3, 4): 7,
        (4, 0): 2,
        (4, 1): 3
    }
test_get_distances()

def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    graph, start_node, s_node_char = construct_graph(input_lines)
    print(s_node_char)
    dists = get_distances(start_node, graph)
    answer = max(dists.values())
    print(f'Final answer: {answer}')
    
if __name__ == '__main__':
    main()
'''
To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........

The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....

In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........

In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...

The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO

In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?
'''
# Can we construct a wider grid that has the spaces between each node?
# That space is open for a certain direction of travel based on the nodes around it
# E.g., 
'''
7||.|' -> VV**
---||     HHHVV
'''

# Every node has a space above, below, right, and left
# A space is H if below node does not connect to above node
# A space is V if left node does not connect to right node
# A space is * if both H and V?

'''
               *X*X*X*
---    ---     *XHXHX*
...            *X*X*X*
---    ...     *X*X*X*
|||            *X*X*X*
|||    ---     *XHXHX*
               *X*X*X*
       |||     *XVXVXV
               *XVXVX*
       |||     *XVXVX*
'''
# 1 extra char per line
# 2*num(lines) + 1 (each line contributes itself and an above line. final line contributes a below line as well)
# (r, c) = H if

# Can we construct a graph of valid moves?
# A location is a 4-tuple of coordinates? Like the coordinates of the pipes in each direction?

# New idea: you can travel along a pipe in its exact direction
# Also, . can connect in any direction; the adjacent pipe just needs to be able to connect to the . space
# Translating to a graph:
# (r, c) connects to (r', c') if the pipes work or one of them is a '.' and the other is a pipe that connects to that '.' space or both are '.'
from collections import deque
from part_1 import construct_graph
def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample_2.txt' if use_sample else 'input.txt'
    with open(f'day-10/{filename}') as f:
        return [line.strip() for line in f.readlines()]

_CONNECTS_UP_SYMBOLS = {'|', 'L', 'J', '.'}
_CONNECTS_DOWN_SYMBOLS = {'|', '7', 'F', '.'}
_CONNECTS_LEFT_SYMBOLS = {'-', 'J', '7', '.'}
_CONNECTS_RIGHT_SYMBOLS = {'-', 'L', 'F', '.'}

# Construct an adjacency set for each node
def construct_escape_graph(
    input_lines: list[str], 
    start_node_char: str, 
    start_node_row: int,
    start_node_col: int
) -> tuple[
    dict[tuple[int,int], set[tuple[int,int]]],
    list[list[str]]
]:
    grid = [['.' for c in range(len(input_lines[0]) + 2)]] + [
        ['.'] + [
            input_lines[r][c]
            for c in range(len(input_lines[0]))
        ] + ['.']
        for r in range(len(input_lines))
    ] + [['.' for c in range(len(input_lines[0]) + 2)]]
    grid[start_node_row+1][start_node_col+1] = start_node_char
    def connects_up(r, c):
        return grid[r][c] in _CONNECTS_UP_SYMBOLS
    
    def connects_down(r, c):
        return grid[r][c] in _CONNECTS_DOWN_SYMBOLS
    
    def connects_left(r, c):
        return grid[r][c] in _CONNECTS_LEFT_SYMBOLS
    
    def connects_right(r, c):
        return grid[r][c] in _CONNECTS_RIGHT_SYMBOLS
    
    def add_neighbor(g, node, neighbor):
        if g[node] is None:
            g[node] = {neighbor}
        else:
            g[node].add(neighbor)
    
    def add_above_neighbor(g, r, c):
        if r - 1 >= 0 and connects_down(r-1, c):
            add_neighbor(g,(r, c), (r-1, c))

    def add_below_neighbor(g, r, c):
        if r + 1 < len(grid) and connects_up(r+1, c):
            add_neighbor(g,(r, c), (r+1, c))

    def add_left_neighbor(g, r, c):
        if c - 1 >= 0 and connects_right(r, c-1):
           add_neighbor(g,(r, c), (r, c-1))

    def add_right_neighbor(g, r, c):
        if c + 1 < len(grid[0]) and connects_left(r, c + 1):
            add_neighbor(g,(r, c), (r, c+1))
    graph = {
        (row, col): None
        for row in range(len(grid))
        for col in range(len(grid[0]))
    }
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            symb = grid[row][col]
            if symb in _CONNECTS_UP_SYMBOLS:
                add_above_neighbor(graph, row, col)
            if symb in _CONNECTS_DOWN_SYMBOLS:
                add_below_neighbor(graph, row, col)
            if symb in _CONNECTS_LEFT_SYMBOLS:
                add_left_neighbor(graph, row, col)
            if symb in _CONNECTS_RIGHT_SYMBOLS:
                add_right_neighbor(graph, row, col)
    graph = {
        node: node_neighbors
        for node, node_neighbors in graph.items()
        if node_neighbors is not None
    }
    return graph, grid

def test_construct_escape_graph() -> None:
    input_lines = get_input_lines(use_sample=True)
    graph, start_node, start_node_char = construct_graph(input_lines)
    escape_graph, grid = construct_escape_graph(
        input_lines,
        start_node_char,
        start_node[0],
        start_node[1]
    )
    print(escape_graph)
    for row in grid:
        print(''.join(row))
test_construct_escape_graph()

def can_escape(
    s: tuple[int, int], 
    graph: dict[tuple[int,int], set[tuple[int,int]]],
    grid_ver_length: int,
    grid_hor_length: int
) -> dict[tuple[int, int], int]:
    visited = set()
    queue = deque([s])
    while len(queue) > 0:
        v = queue.popleft()
        if (
            v[0] == 0 
            or v[1] == 0 
            or v[0] == grid_ver_length - 1 
            or v[1] == grid_hor_length - 1
        ):
            return True
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                queue.append(neighbor)

def bfs_mark_nodes_escapable(s: tuple[int, int], escape_graph: dict[tuple[int, int], set[tuple[int, int]]], grid: list[list[str]], s_loop: set[tuple[int, int]]) -> None:
    visited = set()
    queue = deque([s])
    escapable = False
    while len(queue) > 0:
        v = queue.popleft()
        if s[_ROW_INDEX] == 4 == s[_COL_INDEX]:
            print(v)
        if (
            v[0] == 0 
            or v[1] == 0 
            or v[0] == len(grid) - 1 
            or v[1] == len(grid[0]) - 1
        ):
            escapable = True
        visited.add(v)
        for neighbor in escape_graph[v]:
            if neighbor not in visited:
                queue.append(neighbor)
    symb = 'O' if escapable else 'I'
    for r, c in visited:
        if (r, c) not in s_loop:
            grid[r][c] = symb

_ROW_INDEX = 0
_COL_INDEX = 1
def node_in_loop(node: tuple[int, int], loop: set[tuple[int, int]]) -> bool:
    max_r = max(v[_ROW_INDEX] for v in loop) + 1
    max_c = max(v[_COL_INDEX] for v in loop) + 1
    node_r, node_c = node
    loop_upper_bound = False
    for r in range(node_r):
        if (r, node_c) in loop:
            loop_upper_bound = True
            break
    if not loop_upper_bound:
        return False
    
    loop_lower_bound = False
    for r in range(node_r, max_r):
        if (r, node_c) in loop:
            loop_lower_bound = True
            break
    if not loop_lower_bound:
        return False
    
    loop_left_bound = False
    for c in range(node_c):
        if (node_r, c) in loop:
            loop_left_bound = True
            break
    if not loop_left_bound:
        return False
    
    loop_right_bound = False
    for c in range(node_c, max_c):
        if (node_r, c) in loop:
            loop_right_bound = True
            break
    return loop_right_bound

def test_node_in_loop() -> None:
    loop = {(1, 3), (2, 4), (4, 0), (1, 2), (3, 4), (2, 1), (3, 1), (1, 1), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (3, 2), (4, 1)}
    assert node_in_loop((2, 2), loop)
    assert not node_in_loop((0, 0), loop)
    assert not node_in_loop((0, 1), loop)
    assert not node_in_loop((0, 4), loop)
    assert not node_in_loop((1, 0), loop)
    assert not node_in_loop((1, 4), loop)
    assert not node_in_loop((4, 2), loop)
    assert not node_in_loop((4, 3), loop)
    assert not node_in_loop((4, 4), loop)
test_node_in_loop()

def get_cycle_if_exists(
    g: dict[tuple[int,int], set[tuple[int,int]]], 
    source: tuple[int, int],
) -> set[tuple[int,int]] | None:
    v = source
    stack = [v]
    discovered = set()
    parent = {
        v: None
    }
    while len(stack) > 0:
        v = stack.pop()
        if v not in discovered:
            discovered.add(v)
            for neighbor in g.get(v, set()):
                # back edge (apparently)
                if neighbor in discovered and parent[v] != neighbor:
                    # I think given the constraints of the pipes
                    # the loop is always just everything discovered
                    return discovered
                stack.append(neighbor)
                parent[neighbor] = v
    return None

# For each tile contained within the loop, check if it has a path to an outer node
# If not, then mark it as 'I'. 
def main() -> None:
    print('***MAIN***')
    input_lines = get_input_lines(use_sample=True)
    graph, start_node, start_node_char = construct_graph(input_lines)
    escape_graph, grid = construct_escape_graph(
        input_lines,
        start_node_char,
        start_node[_ROW_INDEX],
        start_node[_COL_INDEX]
    )
    s_loop = get_cycle_if_exists(graph, start_node)
    s_loop_in_escape_grid = {
        (r+1, c+1) for r, c in s_loop
    }
    print('s_loop_in_escape_grid')
    print(sorted(list(s_loop_in_escape_grid), key=lambda v: v[_ROW_INDEX]*100 + v[_COL_INDEX]))
    min_r = min(v[_ROW_INDEX] for v in s_loop_in_escape_grid)
    min_c = min(v[_COL_INDEX] for v in s_loop_in_escape_grid)
    max_r = max(v[_ROW_INDEX] for v in s_loop_in_escape_grid)
    max_c = max(v[_COL_INDEX] for v in s_loop_in_escape_grid)
    # Shouldn't need + 1 for upper bound here
    # as anything on max_r / max_c either forms the loop or is outside the loop
    for r in range(min_r, max_r):
        for c in range(min_c, max_c):
            bfs_mark_nodes_escapable((r, c), escape_graph, grid, s_loop_in_escape_grid)

    for row in grid:
        print(''.join(row))

if __name__ == '__main__':
    main()


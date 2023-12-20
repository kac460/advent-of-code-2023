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
# We need to create a grid of the spaces between pipes
# A space (r, c) connects to (r, c + 1) if the pipe to the bottom right of (r, c) does not connect up to to the pipe to the pipe to the top right of (r, c)
# TODO: define terms like "pipe to the bottom right of a space (r, c)"
# If either of those tiles are a "." then certainly (r, c) connects to (r, c + 1)
'''
               *X*X*X*
---    ---     
...            *X*X*X*
---    ...     
|||            *X*X*X*
|||    ---     
               *X*X*X*
       |||     
               *XVXVX*
       |||    
               *X*X*X*
'''
# TODO - wait but what about spaces between pipes within the pipe row?
# Actually, maybe it's fine
# Directly top/right/left/bottom of space would be another space, not a pipe
# Top right of space (r, c) is (r-1, c)
# Top left of space (r, c) is (r-1, c-1)
# Bottom right of space (r, c) is (r, c)
# Bottom left of space (r, c) is (r, c-1)

from collections import deque
from part_1 import construct_graph

def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample_2.txt' if use_sample else 'input.txt'
    with open(f'day-10/{filename}') as f:
        return [line.strip() for line in f.readlines()]


def construct_space_graph(pipe_graph: dict[tuple[int, int], set[tuple[int, int]]], input_grid_rows, input_grid_cols) -> dict[tuple[int, int], set[tuple[int, int]]]:
    space_graph = {
        (r, c): set()
        for c in range(input_grid_cols + 1) 
        for r in range(input_grid_rows + 1)
    }
    def pipe_neighbors(v):
        return pipe_graph.get(v, set())
    for r, c in space_graph.keys():
        top_right = (r-1, c)
        top_left = (r-1, c-1)
        bottom_right = (r, c)
        bottom_left = (r, c-1)

        # TODO - decide how to deal with bounds
        # Maybe just say if we can reach a node that is out of bounds, then it's escapable?
        if top_right not in pipe_neighbors(bottom_right):
            space_graph[(r, c)].add((r, c+1))

        if top_left not in pipe_neighbors(bottom_left):
            space_graph[(r, c)].add((r, c-1))
        
        if top_left not in pipe_neighbors(top_right):
            space_graph[(r, c)].add((r-1, c))

        if bottom_left not in pipe_neighbors(bottom_right):
            space_graph[(r, c)].add((r+1, c))
    return space_graph


# Top right of space (r, c) is (r-1, c)
# Top left of space (r, c) is (r-1, c-1)
# Bottom right of space (r, c) is (r, c)
# Bottom left of space (r, c) is (r, c-1)

'''
               *X*X*X*
---    ---     
...            *X*X*X*
---    ...     
|||            *X*X*X*
|||    ---     
               *X*X*X*
       |||     
               *XVXVX*
       |||    
               *X*X*X*
'''

def tile_to_spaces(row: int, col: int) -> tuple[
    tuple[int, int], 
    tuple[int, int], 
    tuple[int, int], 
    tuple[int, int]
]:
    return (
        (row, col),
        (row, col+1),
        (row+1, col),
        (row+1, col+1)
    )
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
'''
def update_escapable_tiles(
    source_row: int, 
    source_col: int,
    grid_num_rows: int, 
    grid_num_cols: int,
    space_graph: dict[tuple[int, int], set[tuple[int, int]]],
    escape_grid: list[list[str]],
    s_loop: set[tuple[int, int]]
) -> None:
    spaces = tile_to_spaces(source_row, source_col)
    escapable = False
    # print(f'Source: {(source_row, source_col)}')
    # print(space_graph)
    for space in spaces:
        visited = set()
        queue = deque([space])
        # print(f'Checking {space}')
        while len(queue) > 0:
            # print(len(visited))
            v = queue.popleft()
            if v in visited:
                # print(f'somehow visiting the same node twice {v}')
                continue
            visited.add(v)
            # print(f'v: {v}')
            if v[_ROW_INDEX] in (-1, grid_num_rows) or v[_COL_INDEX] in (-1, grid_num_cols):
                continue
            for neighbor in space_graph[v]:
                if (
                    neighbor[0] in (0, grid_num_rows)
                    or neighbor[1] in (0, grid_num_cols)
                ):
                    escapable = True
                if neighbor not in visited:
                    queue.append(neighbor)

    for r, c in visited:
        if (0 <= r < len(escape_grid)) and (0 <= c < len(escape_grid[0])) and (r, c) not in s_loop:
            escape_grid[r][c] = 'O' if escapable else 'I'
    print('X')

_ROW_INDEX = 0
_COL_INDEX = 1
def node_in_loop_bounds(node: tuple[int, int], loop: set[tuple[int, int]]) -> bool:
    max_r = max(v[_ROW_INDEX] for v in loop)
    max_c = max(v[_COL_INDEX] for v in loop)
    min_r = min(v[_ROW_INDEX] for v in loop)
    min_c = min(v[_COL_INDEX] for v in loop)
    node_r, node_c = node
    return (min_r < node_r < max_r) and (min_c < node_c < max_c)


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


def main() -> None:
    input_lines = get_input_lines(use_sample=True)
    escape_grid = [
        [input_line[c] for c in range(len(input_line))]
        for input_line in input_lines
    ]
    pipe_graph, start_node, s_node_char = construct_graph(input_lines)
    s_loop = get_cycle_if_exists(pipe_graph, start_node)
    space_graph = construct_space_graph(
        pipe_graph,
        input_grid_rows=len(input_lines),
        input_grid_cols=len(input_lines[0])
    )
    for r in range(len(input_lines)):
        for c in range(len(input_lines[0])):
            if (r, c) not in s_loop and node_in_loop_bounds((r, c), s_loop) and escape_grid[r][c] not in ('I', 'O'):
                update_escapable_tiles(
                    r,
                    c,
                    len(input_lines),
                    len(input_lines[0]),
                    space_graph,
                    escape_grid,
                    s_loop
                )
                
    count = 0
    for line in escape_grid:
        print(''.join(line))
        for char in line:
            if char == 'I':
                count += 1

    print('FINAL ANSWER:')
    print(count)
                    
if __name__ == '__main__':
    main()
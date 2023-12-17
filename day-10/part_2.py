# '''
# To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

# ...........
# .S-------7.
# .|F-----7|.
# .||.....||.
# .||.....||.
# .|L-7.F-J|.
# .|..|.|..|.
# .L--J.L--J.
# ...........

# The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

# ...........
# .S-------7.
# .|F-----7|.
# .||OOOOO||.
# .||OOOOO||.
# .|L-7OF-J|.
# .|II|O|II|.
# .L--JOL--J.
# .....O.....

# In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

# ..........
# .S------7.
# .|F----7|.
# .||OOOO||.
# .||OOOO||.
# .|L-7F-J|.
# .|II||II|.
# .L--JL--J.
# ..........

# In both of the above examples, 4 tiles are enclosed by the loop.

# Here's a larger example:

# .F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ...

# The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

# OF----7F7F7F7F-7OOOO
# O|F--7||||||||FJOOOO
# O||OFJ||||||||L7OOOO
# FJL7L7LJLJ||LJIL-7OO
# L--JOL7IIILJS7F-7L7O
# OOOOF-JIIF7FJ|L7L7L7
# OOOOL7IF7||L7|IL7L7|
# OOOOO|FJLJ|FJ|F7|OLJ
# OOOOFJL-7O||O||||OOO
# OOOOL---JOLJOLJLJOOO

# In this larger example, 8 tiles are enclosed by the loop.

# Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

# FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L

# Here are just the tiles that are enclosed by the loop marked with I:

# FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJIF7FJ-
# L---JF-JLJIIIIFJLJJ7
# |F|F-JF---7IIIL7L|7|
# |FFJF7L7F-JF7IIL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L

# In this last example, 10 tiles are enclosed by the loop.

# Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?
# '''
# # Idea:
# # Create function get_cycle_if_exists that returns all the nodes of a cycle (use is_cyclic for reference but traverse parents from the final node up through start node--return these)
# # Ignoring the special "cannot be part of an inner loop" rule, (r, c) is contained by a a loop if you eventually hit part of the loop going in all 4 directions from (r, c)
# # Create a function is_inside_loop implementing the above
# #   Label all "." as O if not is_inside_loop of the S loop
# # Find all loops in whole graph via get_cycle_if_exists
# #   A loop can be stored as a set
# #   We can maintain a dict mapping (r, c) to the loop that it helps form for every (r, c) in the graph
# # Label all the "." as O if is_inside_loop for some non-S loop
# # Final answer: the count of "." that have not been labeled as O
# from part_1 import construct_graph

# def get_input_lines(use_sample: bool) -> list[str]:
#     filename = 'sample_2.txt' if use_sample else 'input.txt'
#     with open(f'day-10/{filename}') as f:
#         return [line.strip() for line in f.readlines()]

# def get_cycle_if_exists(
#     g: dict[tuple[int,int], set[tuple[int,int]]], 
#     source: tuple[int, int],
# ) -> set[tuple[int,int]] | None:
#     v = source
#     stack = [v]
#     discovered = set()
#     parent = {
#         v: None
#     }
#     while len(stack) > 0:
#         v = stack.pop()
#         if v not in discovered:
#             discovered.add(v)
#             for neighbor in g.get(v, set()):
#                 # back edge (apparently)
#                 if neighbor in discovered and parent[v] != neighbor:
#                     # I think given the constraints of the pipes
#                     # the loop is always just everything discovered
#                     return discovered
#                 stack.append(neighbor)
#                 parent[neighbor] = v
#     return None

# def test_get_cycle_if_exists() -> None:
#     graph, start_node = construct_graph(get_input_lines(use_sample=True))
#     print('foo', start_node)
#     cycle = get_cycle_if_exists(graph, (2, 0))
#     print(cycle)
#     grid = [['.' for c in range(5)] for r in range(5)]
#     for r, c in cycle:
#         grid[r][c] = 'X'
#     for row in grid:
#         print(row)
# # test_get_cycle_if_exists()
# _ROW_INDEX = 0
# _COL_INDEX = 1
# def node_in_loop(node: tuple[int, int], loop: set[tuple[int, int]]) -> bool:
#     max_r = max(v[_ROW_INDEX] for v in loop) + 1
#     max_c = max(v[_COL_INDEX] for v in loop) + 1
#     node_r, node_c = node
#     loop_upper_bound = False
#     for r in range(node_r):
#         if (r, node_c) in loop:
#             loop_upper_bound = True
#             break
#     if not loop_upper_bound:
#         return False
    
#     loop_lower_bound = False
#     for r in range(node_r, max_r):
#         if (r, node_c) in loop:
#             loop_lower_bound = True
#             break
#     if not loop_lower_bound:
#         return False
    
#     loop_left_bound = False
#     for c in range(node_c):
#         if (node_r, c) in loop:
#             loop_left_bound = True
#             break
#     if not loop_left_bound:
#         return False
    
#     loop_right_bound = False
#     for c in range(node_c, max_c):
#         if (node_r, c) in loop:
#             loop_right_bound = True
#             break
#     return loop_right_bound

# def test_node_in_loop() -> None:
#     loop = {(1, 3), (2, 4), (4, 0), (1, 2), (3, 4), (2, 1), (3, 1), (1, 1), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (3, 2), (4, 1)}
#     assert node_in_loop((2, 2), loop)
#     assert not node_in_loop((0, 0), loop)
#     assert not node_in_loop((0, 1), loop)
#     assert not node_in_loop((0, 4), loop)
#     assert not node_in_loop((1, 0), loop)
#     assert not node_in_loop((1, 4), loop)
#     assert not node_in_loop((4, 2), loop)
#     assert not node_in_loop((4, 3), loop)
#     assert not node_in_loop((4, 4), loop)
# test_node_in_loop()

# def construct_grid(graph: dict[tuple[int,int], set[tuple[int,int]]], start_node: tuple[int, int], input_lines: list[str]) -> list[list[str]]:
#     s_loop = get_cycle_if_exists(graph, start_node)
#     # We can reduce search space to just the s_loop bounds
#     max_grid_r = max(v[_ROW_INDEX] for v in s_loop) + 1
#     max_grid_c = max(v[_COL_INDEX] for v in s_loop) + 1
#     grid = [['.' for c in range(max_grid_c)] for r in range(max_grid_r)]
#     loops = [s_loop]
#     def forms_part_of_known_loop(node):
#         for loop in loops:
#             if node in loop:
#                 return True
#         return False
#     for r in range(max_grid_r):
#         for c in range(max_grid_c):
#             if input_lines[r][c] != '.':
#                 grid[r][c] = 'P'
#                 if not forms_part_of_known_loop((r, c)):
#                     loop = get_cycle_if_exists(graph, (r, c))
#                     if loop is not None:
#                         loops.append(loop)
#     print(f'Known non-s-loops: {loops[1:]}')
#     for r in range(max_grid_r):
#         for c in range(max_grid_c):
#             if grid[r][c] == '.':
#                 if node_in_loop((r, c), s_loop):
#                     print(f'{(r, c)} is in s_loop')
#                     grid[r][c] = 'I'
#                     for loop in loops[1:]:
#                         if node_in_loop((r, c), loop):
#                             grid[r][c] = 'O'
#                             break
#                 # Technically not necessary
#                 # As we plan to just count the 'I'
#                 # But for sanity:
#                 if grid[r][c] == '.':
#                     grid[r][c] = 'O'
#     return grid

# def test_construct_grid() -> None:
#     input_lines = get_input_lines(use_sample=True)
#     graph, start_node = construct_graph(input_lines)
#     grid = construct_grid(graph, start_node, input_lines)
#     for row in grid:
#         print(''.join(row))
# test_construct_grid()

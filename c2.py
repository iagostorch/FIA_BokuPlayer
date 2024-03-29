# AUXILIARY VARIABLES
max_depth = 2 # max tree depth evaluated

# SCORES FOR EACH PARAMETER
TWO_SEQ = 150
THREE_SEQ = 750
FOUR_SEQ = 3000
FIVE_SEQ = 500000

EXTRA_EMPTY_EDGES_TWO = 50
EXTRA_EMPTY_EDGES_THREE = 500
EXTRA_EMPTY_EDGES_FOUR = 10000	# this state almost guarantees victory

BLOCK_TWO_SEQ = 100
BLOCK_THREE_SEQ = 1000
BLOCK_FOUR_SEQ = 50000

BLOCK_THREE_EMPTY = 150
BLOCK_FOUR_EMPTY = 300
BLOCK_FIVE_EMPTY = 100000


MAKE_SANDWISH = 1000

# OCCURRENCES OF EACH HEURISTIC	
P1_OCCUR_TWO_SEQ = 0
P1_OCCUR_THREE_SEQ = 0
P1_OCCUR_FOUR_SEQ = 0
P1_OCCUR_FIVE_SEQ = 0

P1_OCCUR_BLOCK_TWO_SEQ = 0
P1_OCCUR_BLOCK_THREE_SEQ = 0
P1_OCCUR_BLOCK_FOUR_SEQ = 0

P1_OCCUR_BLOCK_THREE_EMPTY = 0
P1_OCCUR_BLOCK_FOUR_EMPTY = 0
P1_OCCUR_BLOCK_FIVE_EMPTY = 0

P1_OCCUR_MAKE_SANDWISH = 0


P2_OCCUR_TWO_SEQ = 0
P2_OCCUR_THREE_SEQ = 0
P2_OCCUR_FOUR_SEQ = 0
P2_OCCUR_FIVE_SEQ = 0

P2_OCCUR_BLOCK_TWO_SEQ = 0
P2_OCCUR_BLOCK_THREE_SEQ = 0
P2_OCCUR_BLOCK_FOUR_SEQ = 0

P2_OCCUR_BLOCK_THREE_EMPTY = 0
P2_OCCUR_BLOCK_FOUR_EMPTY = 0
P2_OCCUR_BLOCK_FIVE_EMPTY = 0

P2_OCCUR_MAKE_SANDWISH = 0


# COORDINATES FOR EACH DIAGONAL
primary_diags = [
[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0]],
[[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,0]],
[[0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,1],[7,0]],
[[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,2],[7,1],[8,0]],
[[0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,3],[7,2],[8,1],[9,0]],
[[1,5],[2,5],[3,5],[4,5],[5,5],[6,4],[7,3],[8,2],[9,1],[10,0]],
[[2,6],[3,6],[4,6],[5,6],[6,5],[7,4],[8,3],[9,2],[10,1]],
[[3,7],[4,7],[5,7],[6,6],[7,5],[8,4],[9,3],[10,2]],
[[4,8],[5,8],[6,7],[7,6],[8,5],[9,4],[10,3]],
[[5,9],[6,8],[7,7],[8,6],[9,5],[10,4]]
]

secondary_diags = [
[[5,0],[6,0],[7,0],[8,0],[9,0],[10,0]],
[[4,0],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1]],
[[3,0],[4,1],[5,2],[6,2],[7,2],[8,2],[9,2],[10,2]],
[[2,0],[3,1],[4,2],[5,3,],[6,3],[7,3],[8,3],[9,3],[10,3]],
[[1,0],[2,1],[3,2],[4,3],[5,4],[6,4],[7,4],[8,4],[9,4],[10,4]],
[[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,5],[7,5],[8,5],[9,5]],
[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,6],[7,6],[8,6]],
[[0,2],[1,3],[2,4],[3,5],[4,6],[5,7],[6,7],[7,7]],
[[0,3],[1,4],[2,5],[3,6],[4,7],[5,8],[6,8]],
[[0,4],[1,5],[2,6],[3,7],[4,8],[5,9]]
]
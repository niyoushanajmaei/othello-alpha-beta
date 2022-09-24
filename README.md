# othello-alpha-beta
AI agent to play Othello using the alphabet method

## Method
Alpha-beta pruning is used with the maximum depth of d = 3

## Result
The agent was tested against a normal alpha-beta player with depth 8, and won
    (heuristic of normal alpha-beta player: difference of tiles of the two players.)
A game of the agent against a random greedy player takes about 20 seconds (without graphics)


## Heuristic
Heuristic function takes the following strategies into consideration
1. Parity:
    The greedy heuristic, maximizing agent's number of tiles
    parity = # agent tiles - # opponent tiles
2. Weighted square strategy:
    a. Corners and edges are the most important cells
    b. Cells that lead to the opponent taking corners and edges shouldn't ba taken
    Weight matrix:
    
         4, -3,  2,  2,  2,  2, -3,  4
         
        -3, -4, -1, -1, -1, -1, -4, -3
        
         2, -1,  1,  0,  0,  1, -1,  2
         
         2, -1,  0,  1,  1,  0, -1,  2
         
         2, -1,  0,  1,  1,  0, -1,  2
         
         2, -1,  1,  0,  0,  1, -1,  2
         
        -3, -4, -1, -1, -1, -1, -4, -3
        
         4, -3,  2,  2,  2,  2, -3,  4
    points = sum of points of agent - sum of points of opponent
    Weight matrix is from:
    https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
3. Current mobility
    Having no  moves leads to a turn skip so this should be avoided.
    Current mobility is less important than capturing corners and more important cells
    But, having no moves has -3*weighted_ratio points
    Mobility = # moves of agent - #moves of opponent
    The idea was adapted from:
    https://link.springer.com/content/pdf/10.1007/978-0-387-35660-0_10.pdf
Heuristic = parity_ratio * parity + weighted_ratio * weighted_points + mobility
(weighted ratio was set to 50, parity ratio was set to 500)

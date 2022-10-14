# Group
King

## Team Members
Rohan Anand
Jai Patel
Ishan Rathi
_________________________________________________________________________________
# Member Contributions
Tasks were designated during group meetings and assigned as issues in our UTTT repository.

## Issues
UX Design of Simple Board (Rohan) - Changed the design of the board so it's easier visualize the game 

Minimax Implementation (Ishan) - Traverse through game tree and pick move with the best utility value

Alpha-Beta Pruning (Jai) - Prune subtrees that aren't worth checking to improve speed

Heuristic Evaluation Function (Rohan) - Given any global board state, assign a score to indicate which player is winning based on positive or negative values

Heuristic Expansion Strategy (Jai) - To speed up search, implement progressive deepening strategy to obey time limit

Playing "Reasonably Well" (Rohan, Jai, Ishan) - Implementing minimax, alpha-beta, and heuristic functions take care of this and optimizing values in regards to scoring of the board and any bugs issues along the way

Referee Interaction & Documentation (Rohan and Jai) - Allow program to interact with referee.py properly and document all group efforts
_________________________________________________________________________________
# Compiling and Running

## Using default time limit
To run our program: first run king.py, then the second agent, followed by referee.py:

`python king.py`

`python secondagent.py`

`python referee.py`

## Using different time limit
If a new time limit is to be initialized, this would be the new sequence to run the program:

`python king.py --time_limit=x`

`python secondagent.py`

`python referee.py --time_limit=x`

In this case, x would signify the new time limit for the game. Default value if no time limit is specified will be 10 seconds.
_________________________________________________________________________________  
# Utility Function

Our utility function takes in an end-state global board and assigns an end value to it depending upon whether it has been won by a player or a draw. A win by a player gives +infinity points and a lose results in -infinity points.
_________________________________________________________________________________
# Evaluation Function

Our evaluation function takes in a global board state at any given time during the game, and calculates the heuristic value of that board. Points are provided for having won a local board, having tiles in a row within a local board, and so on.
_________________________________________________________________________________
# Heuristic Strategies

To ensure we didn't exceed the time limit, we implemented a type of progressive deepening, with two time checks within our minimax function.

The first check is done after the program checks if a winner has been declared. If the time limit has not been exceeded, the program continues. Else, the program will return the last move to avoid breaking the time limit.

The second check is done after the program executes alpha beta pruning on a subtree. If the time limit has not been exceeded, the program continues. Else, the program will break out of the for loop of moves within the game tree to ensure a move can be returned in constant time.
_________________________________________________________________________________
# Conclusions and Results

## Test Strategy 1

We tested our program against itself (AI vs AI)

Doing so allowed us to view the offensive and defensive behavior of our agent

It also allowed us to see that since our agent is playing against itself, it should be approximately an equal number of wins for X and O.

Our program performed well during testing and throughout testing we made appropriate changes to strengthen our agent

## Test Strategy 2

Another test we conducted to see the performance of the AI was to play against a human

We gave the human 100 seconds to think and input their move and gave the AI its default 10 seconds

Doing this allowed us to see certain patterns the AI played and see how it responded to certain situations

Our program performed decently during this type of testing where it would sometimes make good defensive or offensive moves throughout the game

## Program Strengths

-> Evidence of "smart" decisions

-> Developed own user-friendly version of GUI

-> Good at attacking and taking control of a local board

## Program Weaknesses

-> Occasionally the agent doesn't make the BEST possible move

-> Not so great at defending a local board

-> Sometimes it doesnt play the winning move to end the game

_________________________________________________________________________________
# Why our program has a smart evaluation function and smart heuristics

The heuristic strategy that we implemented, progressive deepening, is a great choice for exploring the minimax tree in UTTT. UTTT has an extremely wide game tree, and to explore all possible states within the provided time limit of 10 seconds would be difficult. Progressive deepening allows us to increase the depth level of the tree as time permits, and if the time limit is reached, return the optimal board state at the given point.

Our evaluation function is another great choice for UTTT, as it allows us to declare certain moves as having a more positive value than others. Points are designated to players following a local board win, being one tile away from winning a local board, being one local board away from winning a global board, and also for a defensive move to block a three in a row for the opponent.
_________________________________________________________________________
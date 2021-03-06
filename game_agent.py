"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Return score using heuristic 3
    return custom_score3(game,player)

def custom_score1(game, player):
    """
    Heuristic 1: Aggressive Improved Score Heuristic
    This heuristic is similar to the improved score heuristic except that the number
    of opponent moves are weighted more heavily

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # Get number of own moves and opponent moves
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves-2*opp_moves)

def custom_score2(game, player):
    """
    Heuristic 2: Euclidean Distance from center and opponent.
    In this heuristic we assume that moves closer to the middle of the board is
    better than moves further to the side of the board. In addition, we assume
    that it is better to be further away from the opponent at the same time.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # Calculate the enclidean distance from current player location to the middle_width
    # of board
    row, col = game.get_player_location(player)
    middle_col = (game.width)//2
    middle_row = (game.height)//2
    euclidean_dist = ((row-middle_row)**2+(col-middle_col)**2)**0.5

    # Calculate the enclidean distance from current player location to opponent's
    # location
    row_opp, col_opp = game.get_player_location(game.get_opponent(player))
    opp_euclidean_dist = ((row_opp-middle_row)**2+(col_opp-middle_col)**2)**0.5
    dist_opp = ((row_opp-row)**2+(col_opp-col)**2)**0.5

    # Return sum of negative enclidean distance to center (since the further it is the
    # less desirable the move) and positive encliden distance to opponent (since the
    # further the opponent is the better)
    return -euclidean_dist + dist_opp

def custom_score3(game, player):
    """
    Heuristic 3: Combination of improved score heuristic and heuristic 2
    This heuristic uses a weighted combination of the improved heuristic score
    and heuristic 2. At the start of the game, heuristic 2 is weighted more heavily,
    whereas at the end of the game, improved score heuristic is weighted more heavily

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.

    """

    # Find % of board still empty
    board_size = game.width*game.height
    empty_size = len(game.get_blank_spaces())
    empty_ratio = empty_size/board_size

    # Calculate the enclidean distance from current player location to the middle_width
    # of board
    row, col = game.get_player_location(player)
    middle_col = (game.width)//2
    middle_row = (game.height)//2
    euclidean_dist = ((row-middle_row)**2+(col-middle_col)**2)**0.5

    # Calculate the enclidean distance from current player location to opponent's
    # location
    row_opp, col_opp = game.get_player_location(game.get_opponent(player))
    opp_euclidean_dist = ((row_opp-middle_row)**2+(col_opp-middle_col)**2)**0.5
    dist_opp = ((row_opp-row)**2+(col_opp-col)**2)**0.5

    # Calculate number of own moves and opponent moves
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # Return weighted score
    return (-euclidean_dist + dist_opp)*empty_ratio + (own_moves-opp_moves)*(1-empty_ratio)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # If there are no legal moves, return immediately
        if not legal_moves:
            return(-1, -1)

        try:
            # Determine which search method to use
            if self.method == 'minimax':
                strategy = self.minimax
            else:
                strategy = self.alphabeta

            # Determine whether iterative deepening needs to be used.
            if self.iterative==True:
                self.search_depth = 1
                while game.get_legal_moves():
                    search_score, search_move = strategy(game, self.search_depth)
                    self.search_depth += 1
            else:
                search_score, search_move = strategy(game, self.search_depth)


        except Timeout:
            return search_move

        # Return the best move from the last completed search iteration
        return search_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()


        # If end of search depth, return value of current node
        if depth == 0:
            return (self.score(game,self), (-1,-1))

        # If it is the maximizing player's turn, find the highest value move assuming that the minimizing player
        # will pick the minimizing moves
        if maximizing_player:
            best_value = float('-inf')
            best_move = (-1,-1)
            for move in game.get_legal_moves():
                (value, new_move) = self.minimax(game.forecast_move(move), depth-1, maximizing_player=False)
                if value > best_value:
                    best_value = value
                    best_move = move

            return best_value, best_move
        # If it it the minimizing player's turn, find the lowest value move assuming that the maximizing player
        # will pick the maximizing moves
        else:
            best_value = float('inf')
            best_move = (-1,-1)
            for move in game.get_legal_moves():
                (value, new_move) = self.minimax(game.forecast_move(move), depth-1, maximizing_player=True)
                if value < best_value:
                    best_value = value
                    best_move = move

            return best_value, best_move



    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # If end of search depth, return value of current node
        if depth == 0:
            return (self.score(game,self), (-1,-1))

        # If it is the maximizing player's turn, find the highest value move assuming that the minimizing player
        # will pick the minimizing moves
        if maximizing_player:
            best_value = float('-inf')
            best_move = (-1,-1)
            for move in game.get_legal_moves():
                (value, new_move) = self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, maximizing_player=False)
                if value > best_value:
                    best_value = value
                    best_move = move

                # If the value of the node is greater than the maximum score for the miminimizing player,
                # the tree can be cut
                if value >= beta:
                    return best_value, best_move

                # Update alpha (the minimum score for the maximizing player)
                alpha = max(alpha,value)



            return best_value, best_move
        # If it it the minimizing player's turn, find the lowest value move assuming that the maximizing player
        # will pick the maximizing moves
        else:
            best_value = float('inf')
            best_move = (-1,-1)
            for move in game.get_legal_moves():
                (value, new_move) = self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, maximizing_player=True)
                if value < best_value:
                    best_value = value
                    best_move = move

                # If the value of the node is less than the minimum score for the maximizing player,
                # the tree can be current
                if value <= alpha:
                    return best_value, best_move

                # Update beta (the maximum score for the minimizing player)
                beta = min(beta,value)


            return best_value, best_move

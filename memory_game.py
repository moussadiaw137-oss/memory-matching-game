"""
Memory Matching Game (Text Version)
------------------------------------
Rules:
  - The board is a grid of hidden cards, each value appearing exactly twice.
  - On each turn, the player reveals two positions.
  - If the two cards match, they stay revealed and the player scores a point.
  - If they don't match, both cards are hidden again.
  - The game ends when every pair has been found.

Players: one human player (score attempt count / try to beat your best score).
Could easily be extended to two humans taking turns (see comments at the bottom).
"""

import random

# ---------------------------------------------------------------------------
# Board setup
# ---------------------------------------------------------------------------

# Values used to build pairs. Add more if you want a bigger board.
SYMBOLS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


def create_board(num_pairs):
    """
    Build a shuffled list of `num_pairs` pairs (so 2 * num_pairs cards total).
    Example for num_pairs=4: ['C', 'A', 'A', 'D', 'B', 'C', 'D', 'B']
    """
    values = SYMBOLS[:num_pairs] * 2   # duplicate each symbol
    random.shuffle(values)             # shuffle positions
    return values


def display_board(board, matched, extra_revealed=None):
    """
    Print the board.
    - `matched`: list of booleans, True for pairs already permanently found.
    - `extra_revealed`: positions to show just for this turn (the 1 or 2
      cards the player is currently looking at), even if not matched yet.
    Hidden cards show their position number so the player knows what to type.
    """
    if extra_revealed is None:
        extra_revealed = []
    print()
    row = []
    for i in range(len(board)):
        if matched[i] or i in extra_revealed:
            cell = board[i]
        else:
            cell = str(i)
        row.append(cell.center(3))
        # print 4 cards per line to keep the board readable
        if (i + 1) % 4 == 0:
            print(' '.join(row))
            row = []
    if row:
        print(' '.join(row))
    print()


# ---------------------------------------------------------------------------
# Input handling (Extra: user entering wrong formats)
# ---------------------------------------------------------------------------

def get_position(message, board_size, forbidden):
    """
    Ask the player for a position and validate it.
    Keeps asking until the input is a valid, unused position.
    `forbidden` holds positions that cannot be picked: already-matched
    cards, plus (on the second pick) the position just chosen as the first.
    """
    while True:
        choice = input(message)
        if not choice.isdigit():
            print("Invalid input: please type a number.")
            continue
        position = int(choice)
        if position < 0 or position >= board_size:
            print(f"Invalid position: choose a number between 0 and {board_size - 1}.")
            continue
        if position in forbidden:
            print("This card is already matched or already chosen this turn. Pick another one.")
            continue
        return position


# ---------------------------------------------------------------------------
# Game loop
# ---------------------------------------------------------------------------

def play_one_game():
    print("How many pairs do you want to play with? (2 to 8)")
    while True:
        pairs_input = input("Number of pairs: ")
        if pairs_input.isdigit() and 2 <= int(pairs_input) <= len(SYMBOLS):
            num_pairs = int(pairs_input)
            break
        print(f"Please enter a number between 2 and {len(SYMBOLS)}.")

    board = create_board(num_pairs)
    board_size = len(board)
    matched = [False] * board_size  # permanently found pairs only
    score = 0
    attempts = 0

    print("\nWelcome to the Memory Matching Game!")
    print("Cards are shown by their position number. Find all the pairs!")

    while score < num_pairs:
        # positions that can never be picked again: already-matched cards
        already_matched = [i for i, m in enumerate(matched) if m]

        display_board(board, matched)

        first = get_position("Pick your first card (position number): ",
                              board_size, already_matched)
        display_board(board, matched, extra_revealed=[first])

        second = get_position("Pick your second card (position number): ",
                               board_size, already_matched + [first])
        display_board(board, matched, extra_revealed=[first, second])

        attempts += 1

        if board[first] == board[second]:
            print(f"Match! {board[first]} == {board[second]}. You keep this pair.")
            matched[first] = True
            matched[second] = True
            score += 1
        else:
            print(f"No match: {board[first]} != {board[second]}. Hiding both cards again.")

    print(f"\nYou found all {num_pairs} pairs in {attempts} attempts!")


def main():
    play_again = True
    while play_again:
        play_one_game()
        answer = input("\nPlay again? (y/n): ").strip().lower()
        play_again = answer.startswith('y')
    print("Thanks for playing!")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Ideas to extend the game further:
# - Two-player mode: alternate turns, keep a score per player, whoever finds
#   the pair keeps the turn (classic memory rule).
# - Difficulty levels: change the number of pairs / grid width.
# - Track time taken and show it as an extra "difficulty" score.
# ---------------------------------------------------------------------------

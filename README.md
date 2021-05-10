# Guessing Game and Solver

Guessing game with a solver. Not unlike the game [Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Gameplay_and_rules).

![Screenshot of the game](screenshot.png?raw=true "Guessing Game")

## Installation

### Optional - compile fastcheck

If Cython is installed, the fastcheck.pyx module can be compiled, which makes the
solver about 10 times faster.

```bash
pip install cython
python setup.py build_ext --inplace
```

### Install package

```bash
pip install .
```

## Usage

Play game and visual solver:

```bash
guessgame
```

Run solver benchmark:

```bash
guessgame-benchmark [best|goood|fast]
```

## Strategy

The solver's strategy is to maximizes the expected number of potential solutions
eliminated by each guess.

This turns out not to be the optimal strategy.
See [Wikipedia](https://en.wikipedia.org/wiki/Mastermind_\(board_game\)#Best_strategies_with_four_pegs_and_six_colors).

The optimal strategy to minimize worst-case number of guess solves in at most 5 guesses.

The optimal strategy to mimimize average number of guesses solves with an average
of 4.34 guesses, and at most 6 guesses.

The solver has three modes: `best` finds the guess that is expected to eliminate
the most number of potential solutions; `good` finds a guess that is expected to
eliminate at least 5/6th of potential solutions; `fast` finds a
guess that is expected to eliminate at least 1/2 of potential solutions.

These are the benchmark results for solving all 1296 possible puzzles
for the 4 pegs / 6 colors game on my laptop:

| Mode | Avg # Guesses | Max # Guesses | Avg Time / Puzzle |
|------|---------------|---------------|-------------------|
| best | 4.42          | 6             | 2.20s             |
| good | 4.53          | 6             | 0.02s             |
| fast | 4.99          | 8             | 0.01s             |

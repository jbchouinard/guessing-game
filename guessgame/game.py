from random import randint

try:
    from guessgame.fastcheck import check
except ImportError:

    def check(colors, guess, solution):
        count_guess = [0] * colors
        count_soln = [0] * colors
        correct = 0
        for (color_guessed, color_actual) in zip(guess, solution):
            if color_guessed == color_actual:
                correct += 1
            else:
                count_guess[color_guessed - 1] += 1
                count_soln[color_actual - 1] += 1
            incorrect = 0
        for (c1, c2) in zip(count_guess, count_soln):
            incorrect += min(c1, c2)
        return (correct, incorrect)

    print("Could not import fastcheck, was it built with Cython?")
    print("You may try building it with: python setup.py build_ext --inplace")
    print("and re-installing the package.")
    print("Using slower check function.")


class GameFinished(Exception):
    pass


class Game:
    def __init__(self, n=4, colors=6, tries=10):
        self.n = n
        self.tries = tries
        self.colors = colors
        self.solution = [randint(1, colors) for _ in range(n)]
        self.guesses = []

    def guess(self, guess):
        if self.state != "open":
            raise GameFinished()
        response = check(self.colors, guess, self.solution)
        self.guesses.append((guess, response))
        return response

    def restart(self):
        self.guesses = []

    @property
    def state(self):
        if self.guesses and self.guesses[-1][0] == self.solution:
            return "solved"
        elif len(self.guesses) < self.tries:
            return "open"
        else:
            return "failed"

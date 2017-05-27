import itertools
import math

from game import check


def possible_guesses(game):
    return itertools.product(range(1, game.colors+1), repeat=game.n)


class Solver:
    def __init__(self, game):
        self.game = game
        self.possible = list(possible_guesses(game))
        self.first_guess = True

    def filter_solutions(self, solns, guess, response):
        kept = []
        for soln in solns:
            if check(self.game.colors, guess, soln) == response:
                kept.append(soln)
        return kept

    def find_fast_guess(self, treshold=0.5):
        best_guess = self.possible[0]
        best_n = len(self.possible)
        for guess in self.possible:
            expected_n = self.compute_expected_n_solns(guess)
            if expected_n <= math.ceil(len(self.possible) * treshold):
                return guess
            if expected_n < best_n:
                best_guess = guess
                best_n = expected_n
        return best_guess

    def find_best_guess(self):
        best_guess = self.possible[0]
        best_n = len(self.possible)
        for guess in self.possible:
            expected_n = self.compute_expected_n_solns(guess)
            if expected_n < best_n:
                best_guess = guess
                best_n = expected_n
        return best_guess

    def compute_expected_n_solns(self, guess):
        ns = []
        for soln in self.possible:
            response = check(self.game.colors, guess, soln)
            left = self.filter_solutions(self.possible, guess, response)
            ns.append(len(left))
        return sum(ns) / len(ns)

    def guess(self, mode='fast'):
        if self.first_guess and (self.game.n, self.game.colors) == (4, 6):
            guess = [1, 1, 2, 3]
            self.first_guess = False
        else:
            if mode == 'fast':
                guess = self.find_fast_guess()
            else:
                guess = self.find_best_guess()
        response = self.game.guess(list(guess))
        self.possible = self.filter_solutions(self.possible, guess, response)

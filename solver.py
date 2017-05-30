import itertools
from sys import argv

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

    def find_guess(self, treshold, guess_from):
        best_guess = self.possible[0]
        best_n = len(self.possible)
        if guess_from == 'possible':
            to_check = self.possible
        else:
            to_check = possible_guesses(self.game)
        for guess in to_check:
            expected_n = self.compute_expected_n_solns(guess)
            if expected_n <= len(self.possible) * treshold:
                return guess
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

    def guess(self, treshold=0.5, guess_from='possible'):
        # Precomputed best first move
        if self.first_guess:
            if (self.game.n, self.game.colors) == (4, 6):
                guess = [1, 1, 2, 3]
            else:
                guess = self.find_guess(treshold, guess_from)
            self.first_guess = False
        else:
            guess = self.find_guess(treshold, guess_from)
        response = self.game.guess(list(guess))
        self.possible = self.filter_solutions(self.possible, guess, response)


if __name__ == '__main__':
    from game import Game

    n_guesses = []
    game = Game()
    counter = 1

    for soln in possible_guesses(game):
        game.solution = list(soln)
        game.restart()

        print('Solving game %i %s.' % (counter, soln))
        solver = Solver(game)
        while game.state == 'open':
            solver.guess(float(argv[1]), str(argv[2]))
        n = len(game.guesses)
        if game.state == 'solved':
            print('Solved in %i guesses.' % n)
            n_guesses.append(n)
        else:
            print('Failed to solve.')
            n.guesses.append('F')
        counter += 1

    avg = sum(n_guesses) / len(n_guesses)
    with open('n_guesses_%s_%s.txt' % (argv[1], argv[2]), 'w') as f:
        f.write(','.join((str(n) for n in n_guesses)))
    print('Solved all in average of %f guesses.' % avg)
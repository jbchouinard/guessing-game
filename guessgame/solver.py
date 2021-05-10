import argparse
import itertools
import time

from guessgame.game import check


def possible_guesses(game):
    return itertools.product(range(1, game.colors + 1), repeat=game.n)


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

    def find_guess(self, treshold):
        best_guess = self.possible[0]
        best_n = len(self.possible)
        for guess in self.possible:
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

    def guess(self, treshold=0.5):
        # Precomputed best first move
        if self.first_guess:
            if (self.game.n, self.game.colors) == (4, 6):
                guess = [1, 1, 2, 3]
            else:
                guess = self.find_guess(treshold)
            self.first_guess = False
        else:
            guess = self.find_guess(treshold)
        response = self.game.guess(list(guess))
        self.possible = self.filter_solutions(self.possible, guess, response)


def main():
    from guessgame.game import Game

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["best", "good", "fast"])
    args = parser.parse_args()

    treshold = {
        "best": 0,
        "good": 1/6,
        "fast": 1/2,
    }[args.mode]

    game = Game()
    n_guesses = []
    counter = 1

    start_time = time.time()
    permutations = list(possible_guesses(game))
    ntotal = len(permutations)
    for i, soln in enumerate(permutations):
        print("solving game {} of {}".format(i, ntotal))
        game.solution = list(soln)
        game.restart()

        solver = Solver(game)
        while game.state == "open":
            solver.guess(treshold)
        n = len(game.guesses)
        if game.state == "solved":
            n_guesses.append(n)
        else:
            n.guesses.append("F")
        counter += 1

    elapsed = time.time() - start_time
    avg = sum(n_guesses) / len(n_guesses)
    avg_secs = elapsed / len(n_guesses)
    print(
        (
            "Solved all possible puzzles in average of {:.2f} guesses, "
            "max of {:d} guesses, average of {:.3f} seconds/puzzle"
        ).format(avg,  max(n_guesses), avg_secs,)
    )
    with open("n_guesses_{}.txt".format(args.mode), "w") as f:
        f.write(",".join((str(n) for n in n_guesses)))


if __name__ == "__main__":
    main()

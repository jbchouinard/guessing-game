from collections import Counter
from random import randint


class Game:
    def __init__(self, n=4, colors=6, tries=10):
        self.n = n
        self.tries = tries
        self.colors = colors
        self.solution = [randint(1, colors) for _ in range(n)]
        self.guesses = []

    def guess(self, guess):
        response = {'correct': 0}
        not_matched_guess = []
        not_matched_target = []
        for i in range(self.n):
            if guess[i] == self.solution[i]:
                response['correct'] += 1
            else:
                not_matched_guess.append(guess[i])
                not_matched_target.append(self.solution[i])

        incorrect = Counter(not_matched_guess) & Counter(not_matched_target)
        response['incorrect'] = len(list(incorrect.elements()))
        self.guesses.append((guess, response))
        return response

    @property
    def solved(self):
        if self.guesses:
            return self.guesses[-1][0] == self.solution
        else:
            return False

def check(int colors, guess, solution):
    cdef int count_guess[20]
    cdef int count_soln[20]
    cdef int guessarr[10]
    cdef int solnarr[10]
    cdef int correct = 0
    cdef int incorrect = 0
    cdef int i = 0
    cdef int n = len(guess)
    if colors > 20:
        colors = 20
    if n > 10:
        n = 10
    while i < n:
        guessarr[i] = guess[i]
        solnarr[i] = solution[i]
        i += 1
    i = 0
    while i < colors:
        count_guess[i] = 0
        count_soln[i] = 0
        i += 1
    i = 0
    while i < n:
        if guessarr[i] == solnarr[i]:
            correct += 1
        else:
            count_guess[guessarr[i]-1] += 1
            count_soln[solnarr[i]-1] += 1
        i += 1
    i = 0
    while i < colors:
        if count_guess[i] < count_soln[i]:
            incorrect += count_guess[i]
        else:
            incorrect += count_soln[i]
        i += 1
    return (correct, incorrect)
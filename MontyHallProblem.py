""" This code simulates the Monty Hall gameshow, in which contestants try to
guess which of 3 closed doors contains a cash prize. The odds of choosing the
correct door are 1 in 3. As a twist, the host of the show occasionally opens a
door after a contestant makes a choice. This door is always one of the two the
contestant did not pick, and is also always one of the losing doors. Then, the
contestant has the option of keeping the original choice, or swtiching to the
other unopened door. Is there any benefit to switching doors?"""

import numpy as np


def run_sim(nsim=1):
    sims = simulate_prizedoor(nsim)
    guesses = simulate_guess(nsim)
    goatdoors = goat_door(sims, guesses)
    newguess = switch_guess(guesses, goatdoors)

    # Run without switching the guess
    noswitch = win_percentage(guesses, sims)
    print("Win percentage no switch:", noswitch)

    # Run with switching the guess
    switch = win_percentage(newguess, sims)
    print("Win percentage with switch:", switch)


def simulate_prizedoor(nsim=3):
    """ Generate a random array of 0s, 1s, and 2s that
    represent the location of the prize"""
    return np.random.randint(0, 3, (nsim))


def simulate_guess(nsim=3):
    """ Simulate the contestant's guesses for
    nsim simulations"""
    guesses = np.random.randint(0, 3, (nsim))
    return guesses


def goat_door(sims, guesses):
    """Simulate the opening of a "goat door" that doesn't
       contain the prize, and is different from the
       contestant's guess."""

    # Remove the prize door from the list of eligible goat doors.
    x = []
    for si in sims:
        results = [0, 1, 2]
        if si in results:
            results.remove(si)
        x.extend([results])

    # Remove the contestant's guess from the list of eligible goat doors.
    options = []
    goatdoor = []
    for gu in range(0, len(guesses)):
        if guesses[gu] in x[gu]:
            x[gu].remove(guesses[gu])
        options.extend([x[gu]])
        goatdoor.extend(np.random.choice(options[gu], 1))
    return goatdoor


def switch_guess(guesses, goatdoors):
    """This stragey always switches the guess after
    a door is opened"""
    choices = [0, 1, 2]
    newguess = []
    for i in range(0, len(guesses)):
        used = [guesses[i], goatdoors[i]]
        newguess.append(list(set(choices) - set(used)))
    return newguess


def win_percentage(guesses, prizedoors):
    """Calculate the percent of times that a simulation
    of guesses is correct."""

    win_count = 0
    for i in range(0, len(guesses)):
        if guesses[i] == prizedoors[i]:
            win_count = win_count + 1

    win_percent = win_count / len(guesses) * 100
    return round(win_percent, 2)

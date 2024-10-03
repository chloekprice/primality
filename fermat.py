import argparse
import random

from numpy.random import exponential


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[str, str]:
    return fermat(N, k), miller_rabin(N, k)


# You will need to implement this function and change the return value.
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0: # constant (lookup) + constant (comparison)
        return 1 # constant (return)
    z = mod_exp(x, y//2, N) # { constant (assignment) + function call [ constant (lookup) + constant (lookup) + constant (integer division) + constant (lookup)] } * log(n)
    if y % 2 == 0: # constant (lookup) + constant (modulo) + constant (comparison)
        return (z**2) % N # constant (return) + constant (lookup) + constant (exponentiation) + constant (modulo)
    else:
        return (x*z**2) % N  # constant (return) + constant (lookup) constant (exponentiation) + constant (lookup) + constant (multiplication) + constant (modulo)


# You will need to implement this function and change the return value.
def fprobability(k: int) -> float:
    return 1 - (1/(2**k))


# You will need to implement this function and change the return value.
def mprobability(k: int) -> float:
    return 1 - (1/(4**k))


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low, hi) which gives a random integer between low and
# hi, inclusive.
def fermat(N: int, k: int) -> str:
    for i in range(k): # { constant (lookup) + constant (lookup) + constant (comparison)} * k
        a = random.randint(1, N-1) # { constant (assignment) + [constant (lookup) + constant (subtraction) + constant (random num generation) } * k
        if mod_exp(a, N-1, N) == 1: # log(n) (call mod_exp with runtime complexity) + constant (comparison)
            continue # constant
        else:
            return "composite" # constant (return)
    return "prime" # constant (return)


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low, hi) which gives a random integer between low and
# hi, inclusive.
def miller_rabin(N: int, k: int) -> str:
    for i in range(k): # { constant (lookup) + constant (lookup) + constant (comparison)} * k
        a = random.randint(1, N-1) # { constant (assignment) + [constant (lookup) + constant (subtraction) + constant (random num generation) } * k
        if mod_exp(a, N-1, N) == 1: # { log(n) (call mod_exp with runtime complexity) + constant (comparison) } * k
            if (N-1) % 2 == 0: # { constant (lookup) + constant (subtraction) + constant (modulo) + constant (comparison) } * k
                exp = (N-1)//2 # { constant (assignment) + [constant (lookup) + constant (subtraction) + constant (integer division) } * k
                while exp % 2 == 0:# { [ constant (lookup) + constant (modulo) + constant (comparison) ] * log(N) } * k
                    value = mod_exp(a, exp, N) # { [ log(n) (call mod_exp with runtime complexity) ] * log(N) } * k
                    if value == 1: # { [ constant (lookup) + constant (comparison) ] * log(N) } * k
                        exp = exp//2 # { [ constant (assignment) + constant (lookup) + constant (integer division) ] * log(N) } * k
                    elif value == (N-1): # { [ constant (lookup) + constant (subtraction) + constant (comparison) ] * log(N) } * k
                        break # constant
                    else:
                        return "composite" # constant (return)
        else:
            return "composite" # constant (return)
    return "prime" # constant (return)


def main(number: int, k: int):
    fermat_call, miller_rabin_call = prime_test(number, k)
    fermat_prob = fprobability(k)
    mr_prob = mprobability(k)

    print(f'Is {number} prime?')
    print(f'Fermat: {fermat_call} (prob={fermat_prob})')
    print(f'Miller-Rabin: {miller_rabin_call} (prob={mr_prob})')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('k', type=int)
    args = parser.parse_args()
    main(args.number, args.k)

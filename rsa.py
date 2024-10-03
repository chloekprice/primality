import random
import sys

from numpy.f2py.auxfuncs import throw_error

# This may come in handy...
from fermat import miller_rabin, fermat

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    if a > b: # constant (lookup) + constant (lookup) + constant (comparison)
        if b == 0: # constant (lookup) + constant (comparison)
            return 1, 0, a # constant (return) + constant (lookup)
        x, y, d = ext_euclid(b, a % b) # { constant (assignment) + [ constant (function call) + constant (lookup) + constant (lookup) + constant (modulo) ] } * log(n) (idk what base but doesn't matter)
        return y, (x - (a//b) * y), d # { constant (lookup) + [ constant (lookup)*3 + constant (integer division) * constant (multiplication) ] + constant (lookup) } * log(n)
    else:
        a, b = b, a
        if b == 0: # constant (lookup) + constant (comparison)
            return 1, 0, a # constant (return) + constant (lookup)
        x, y, d = ext_euclid(b, a % b) # { constant (assignment) + [ constant (function call) + constant (lookup) + constant (lookup) + constant (modulo) ] } * log(n) (idk what base but doesn't matter)
        return y, (x - (a//b) * y), d # { constant (lookup) + [ constant (lookup)*3 + constant (integer division) * constant (multiplication) ] + constant (lookup) } * log(n)


# Implement this function
def generate_large_prime(bits=512) -> int:
    prime_num = random.getrandbits(bits) # constant (assignment) + constant (generate rand number)
    if miller_rabin(prime_num, 20) == "prime": # m(log^2(n)) (miller_rabin) + constant (comparison)
        return prime_num # constant (return)
    else:
        return generate_large_prime(bits) # { constant (return) } * n


# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:
    p = generate_large_prime(bits) # nmlog^2(n)
    q = generate_large_prime(bits) # nmlog^2(n)
    n = p * q # constant (assignment) + constant (lookup)*2 + constant (multiplication)
    a = (p - 1) * (q - 1) # constant (assignment) + constant (lookup)*2 + constant (subtraction)*2 + constant (multiplication)

    e = 0 # constant (assignment)
    d = 0 # constant (assignment)
    for prime in primes: # constant (will run up to 25 times since there are 25 elements in the list)
        x, y, gcd = ext_euclid(a, prime) # constant (assignment) + log(n)
        if gcd == 1: # constant (comparison)
            e = prime # constant (assignment)
            d = y # constant (assignment)
            break # constant
    if e == 0: # constant (comparison)
        throw_error("none of the provided primes worked") # constant
    return n, e, (d % a) # constant

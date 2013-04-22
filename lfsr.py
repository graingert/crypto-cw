#
# Galois linear feedback shift register (LFSR) in Python
# Copyright (c) 2012 Nayuki Minase
#
# http://nayuki.eigenstate.org/page/galois-linear-feedback-shift-register
#

# Random number generator class (implements most functionality of random.Random)


class LfsrRandom(object):

    def __init__(self, charis, state):

        if charis < 0:
            raise ValueError("Invalid characteristic polynomial - negative")
        if charis.bit_length() < 2:
            raise ValueError("Invalid characteristic polynomial - degree too low")
        if state == 0:
            raise ValueError("Invalid state polynomial - all zero")
        if state.bit_length() > charis.bit_length():
            raise ValueError("Invalid state polynomial - degree >= char poly degree")

        self.characteristic = charis
        self.degree = charis.bit_length()
        self.state = state

    def next(self):
        result = self.state & 1                            # Use bit 0 in the LFSR state as the result
        self.state = self.state << 1                       # Multiply by x
        if (self.state >> self.degree) & 1 != 0:           # If degree of state polynomial matches degree of characteristic polynomial
            self.state = self.state ^ self.characteristic  # Then subtract the characteristic polynomial from the state polynomial
        return result

    def __iter__(self):
        return self


# Demo main program
if __name__ == "__main__":
    # Polynomial: x^16 + x^14 + x^13 + x^11 + x^0
    rand = LfsrRandom(0b10110100000000001, 1)
    for i in xrange(10):
        print rand.random()
    for i in xrange(20):
        print rand.randbit()

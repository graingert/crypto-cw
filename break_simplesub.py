import random
import re

from six import Iterator
from string import maketrans

from ngram_score import ngram_score

fitness = ngram_score('quadgrams.txt')  # load our quadgram model


# helper function, converts an integer 0-25 into a character
def i2a(i):
    return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i % 26]


# decipher a piece of text using the substitution cipher and a certain key
def sub_decipher(text, key, original="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return text.translate(
        maketrans(original, ''.join(key))
    )


def human_sub_decipher(text, key, original="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    key = ''.join(key)
    key = key.upper() + key.lower()
    return text.translate(
        maketrans(original.upper() + original.lower(), key)
    )


def break_simple_sub(ctext, startkey="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    ''' perform hill-climbing with a single start. This function may have to be called many times
    to break a substitution cipher. '''
        # make sure ciphertext has all spacing/punc removed and is uppercase

    original_text = ctext
    ctext = re.sub('[^A-Z]', '', ctext.upper())

    startkey = list(startkey)
    parentkey = list(startkey)
    random.shuffle(parentkey)
    bestscore = fitness.score(sub_decipher(ctext, parentkey))
    bestkey = list(parentkey)
    parentscore = bestscore

    while(True):
        counter = 0
        while(counter < 1000):
            a = random.randint(0, 25)
            b = random.randint(0, 25)
            childkey = list(parentkey)

            # swap two characters in the child
            childkey[a], childkey[b] = childkey[b], childkey[a]

            plaintext = sub_decipher(ctext, childkey)
            score = fitness.score(plaintext)
            # if the child was better, make a new parentkey
            if score > parentscore:
                parentscore = score
                parentkey = childkey
                counter = 0
            else:
                counter += 1

        if parentscore > bestscore:
            bestscore = parentscore
            bestkey = list(parentkey)
            yield bestscore, ''.join(bestkey), human_sub_decipher(original_text, bestkey)

        random.shuffle(parentkey)
        parentscore = fitness.score(sub_decipher(ctext, parentkey))


def print_solution(ctext):
    for (i, (score, key, text)) in enumerate(break_simple_sub(ctext)):
        print """best score so far: {score}, on iteration, {i}
    best key: {key}
    plaintext: {text}
""".format(score=score, key=key, text=text, i=i)

if __name__ == "__main__":

    ctext = """Idiel Aehssh yiv mjhswirhl zq wbh ohashvveml bh vm oshioho.
    Nms wbshh oiqv inwhs wbh ohkejhsq mn bev vahhtb iw wbh kmodh bh kiq ml
    i vmni iw bmgh shthejeld lm mlh ilo dmeld lmybhsh."""

    print "Substitution Cipher solver, you may have to wait several iterations"
    print "for the correct result. Press ctrl+c to exit program."
    # keep going until we are killed by the user
    print_solution(ctext)

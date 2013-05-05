from __future__ import print_function

import random
import re
import sys

from collections import deque
from string import maketrans

from utils.ngram_score import ngram_score

fitness = ngram_score(open('quadgrams.txt'))  # load our quadgram model


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


def break_simple_sub(ctext, max_retries=10, max_failures=1000, startkey="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """generator to break a simple substitution cipher hill-climb
    trying a new start every 1000 failed attempts"""

    original_text = ctext
    # make sure ciphertext has all spacing/punc removed and is uppercase
    ctext = re.sub('[^A-Z]', '', ctext.upper())

    startkey = list(startkey)
    parentkey = list(startkey)
    random.shuffle(parentkey)
    bestscore = fitness.score(sub_decipher(ctext, parentkey))
    bestkey = list(parentkey)
    parentscore = bestscore
    retries = 0
    while(retries < max_retries):
        counter = 0
        # if the counter is greater than 1000 we've tried
        # too many attempts and need to move to a new 'hill'
        while(counter < max_failures):

            # swap two characters in the child
            a = random.randint(0, 25)
            b = random.randint(0, 25)
            childkey = list(parentkey)

            childkey[a], childkey[b] = childkey[b], childkey[a]

            # decipher using this new key
            plaintext = sub_decipher(ctext, childkey)
            score = fitness.score(plaintext)
            # if the child was better, make a new parentkey
            if score > parentscore:
                parentscore = score
                parentkey = childkey
                # also reset counter to 0 because this hill
                # is likely to contain an even better soln
                counter = 0
            else:
                counter += 1

        if parentscore > bestscore:
            bestscore = parentscore
            bestkey = list(parentkey)
            yield {
                "retries": retries,
                "score": bestscore,
                "key": ''.join(bestkey),
                "text": human_sub_decipher(original_text, bestkey)
            }

        else:
            retries += 1
        # try to 'climb' a new 'hill' at random
        random.shuffle(parentkey)
        parentscore = fitness.score(sub_decipher(ctext, parentkey))


if __name__ == "__main__":
    for item in break_simple_sub(open(sys.argv[1]).read()):
        print("""best score so far: {score}
    best key: {key}
    plaintext: {text}
""".format(**item), file=sys.stderr)
    print(item["text"])

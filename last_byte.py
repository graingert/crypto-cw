
def brutforce_last_byte():
    valid_chars = frozenset(chain(string.ascii_lowercase, string.ascii_uppercase, " ,."))

    keys = []

    for i in range(2**8):
        key = bitarray(islice(LfsrRandom(47, 3), 3*8))
        key.frombytes(chr(i))
        keystream = key * int(len(cypher)/len(key))
        plaintext = (cypher ^ keystream).tobytes()
        if valid_chars.issuperset(plaintext):
            keys.append({
                "key": key,
                "keystream": keystream,
                "plaintext": plaintext

            })

    for key in keys:
        print(key["key"])
        print(key["plaintext"])
        print_solution(key["plaintext"])

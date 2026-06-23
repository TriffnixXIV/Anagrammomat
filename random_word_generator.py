import random

CONSONANT_BEFORE_VOWEL_SETS = [
    ("b", 10), ("bj", 3), ("bl", 3), ("br", 3), ("bv", 3), ("bw", 3), ("by", 3),
    ("c", 10), ("ch", 10), ("cj", 3), ("cl", 3), ("cr", 3), ("cv", 3), ("cw", 3), ("cy", 3),
    ("d", 10), ("dj", 3), ("dl", 3), ("dr", 3), ("dv", 3), ("dw", 3), ("dy", 3),
    ("f", 10), ("fj", 3), ("fl", 3), ("fr", 3), ("fv", 3), ("fw", 3), ("fy", 3),
    ("g", 10), ("gj", 3), ("gl", 3), ("gr", 3), ("gv", 3), ("gw", 3), ("gy", 3),
    ("h", 10),
    ("j", 10),
    ("k", 10), ("kj", 3), ("kl", 3), ("kr", 3), ("ks", 3), ("kv", 3), ("kw", 3), ("ky", 3),
    ("l", 10),
    ("m", 10),
    ("n", 10),
    ("p", 10), ("pj", 3), ("pl", 3), ("pr", 3), ("ps", 3), ("pv", 3), ("pw", 3), ("py", 3),
    ("q", 10),
    ("r", 10), ("rh", 3),
    ("s", 10), ("sc", 3), ("sg", 3), ("sh", 10), ("sk", 5), ("sp", 3), ("st", 3),
    ("t", 10), ("th", 10), ("tj", 3), ("tl", 3), ("tr", 3), ("ts", 3), ("tv", 3), ("tw", 3), ("ty", 3),
    ("v", 10),
    ("w", 10),
    ("x", 10),
    ("y", 10),
    ("z", 10)
]

VOWEL_SETS = [
    ("a", 10), ("aa", 1), ("ae", 3), ("ai", 3), ("ao", 1), ("au", 3), ("ay", 5),
    ("e", 10), ("ea", 1), ("ee", 1), ("ei", 1), ("eo", 1), ("eu", 3), ("ey", 5),
    ("i", 15), ("ia", 1), ("ie", 5), ("ii", 1), ("io", 1), ("iu", 1), ("iy", 1),
    ("o", 10), ("oa", 2), ("oe", 5), ("oi", 2), ("oo", 3), ("ou", 3), ("oy", 3),
    ("u", 10), ("ua", 1), ("ue", 3), ("ui", 1), ("uo", 1), ("uu", 1), ("uy", 3),
    ("y", 10)
]

CONSONANT_AFTER_VOWEL_SETS = [
    ("b", 10), ("bs", 3),
    ("c", 10), ("ck", 5),
    ("d", 10),
    ("f", 10),
    ("g", 10),
    ("h", 10), ("hl", 5), ("hm", 5), ("hn", 5), ("hr", 5),
    ("j", 3),
    ("k", 10),
    ("l", 10), ("lb", 3), ("lc", 3), ("ld", 3), ("lf", 3), ("lg", 3), ("lk", 3), ("ll", 5), ("lp", 3), ("lt", 3),
    ("m", 10), ("mb", 1), ("mm", 5),
    ("n", 10), ("nc", 3), ("nd", 3), ("nf", 3), ("ng", 3), ("nk", 3), ("nn", 5), ("nt", 3),
    ("p", 10), ("pp", 3),
    ("q", 10),
    ("r", 10), ("rb", 3), ("rc", 3), ("rd", 3), ("rf", 3), ("rg", 3), ("rk", 3), ("rp", 3), ("rr", 3), ("rt", 3),
    ("s", 10), ("sc", 3), ("sk", 3), ("ss", 5), ("st", 5),
    ("t", 10), ("ts", 5), ("tt", 5),
    ("v", 10),
    ("w", 10),
    ("x", 10),
    ("y", 3),
    ("z", 10)
]

def weighted_pull(weighted_list: list[tuple[object, int]]):
    sum_of_weights = 0
    for obj, weight in weighted_list:
        sum_of_weights += weight
    
    roll = random.randrange(0, sum_of_weights)
    for obj, weight in weighted_list:
        roll -= weight
        if roll < 0:
            return obj
    
    # when the pull fails for some reason, return the first one
    return weighted_list[0][0]

def get_set(set_list: list[tuple[str, int]]):
    return weighted_pull(set_list)

def get_syllable():
    syllable = ""
    if random.randint(0, 3) > 0:
        syllable += get_set(CONSONANT_BEFORE_VOWEL_SETS)
    syllable += get_set(VOWEL_SETS)
    if random.randint(0, 3) > 0:
        syllable += get_set(CONSONANT_AFTER_VOWEL_SETS)
    return syllable

def generate_word():
    word = ""
    while random.randint(1, 2 + len(word)) > len(word):
        word += get_syllable()
    return word

def generate_sentence():
    word_list = []
    while random.randint(3, 7 + len(word_list)) > len(word_list):
        word_list.append(generate_word())
    return " ".join(word_list)

if __name__ == "__main__":
    input_text = "press Enter to continue or type \"/END\" to exit. Same for every following word."
    while True:
        string = input(input_text + " ")
        if string == "/END":
            break
        else:
            # input_text = generate_word()
            input_text = generate_sentence()
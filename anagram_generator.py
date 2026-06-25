from random_word_generator import *
import math

class AnagramGenerator():

    def __init__(self):
        pass
    
    def set_word_list(self, words: list[str]):
        self.set_histogram(generate_histogram("".join(words)))

    def set_string(self, string: str):
        self.set_histogram(generate_histogram(string))

    def set_histogram(self, letter_histogram: dict[str, int]):
        self.vowel_histogram: dict[str, int] = {}
        self.consonant_histogram: dict[str, int] = {}
        self.unknown_character_histogram: dict[str, int] = {}

        self.number_of_vowels: int = 0
        self.number_of_consonants: int = 0

        for letter, amount in letter_histogram.items():
            if letter in "aeiou":
                self.number_of_vowels += amount
                self.vowel_histogram[letter] = amount
            elif letter in "bcdfghjklmnpqrstvwxz":
                self.number_of_consonants += amount
                self.consonant_histogram[letter] = amount
            elif letter == "y":
                vowel_y_amount = math.ceil(amount / 2)
                if vowel_y_amount > 0:
                    self.number_of_vowels += vowel_y_amount
                    self.vowel_histogram[letter] = vowel_y_amount

                consonant_y_amount = math.floor(amount / 2)
                if consonant_y_amount > 0:
                    self.number_of_consonants += consonant_y_amount
                    self.consonant_histogram[letter] = consonant_y_amount
            else:
                self.unknown_character_histogram[letter] = amount

    def generate_anagram(self) -> str:
        remaining_vowels: dict[str, int] = self.vowel_histogram.copy()
        remaining_consonants: dict[str, int] = self.consonant_histogram.copy()
        
        maximum_number_of_syllables = self.number_of_vowels

        # determine sets of consonants
        sets_of_starting_consonants, sets_of_ending_consonants = get_consonant_sets_from_remaining_letters(remaining_consonants, maximum_number_of_syllables)

        # determine number of syllables
        minimum_number_of_syllables = max(len(sets_of_starting_consonants), len(sets_of_ending_consonants), math.ceil(self.number_of_vowels / 2))

        number_of_syllables = random.randint(minimum_number_of_syllables, maximum_number_of_syllables)
        
        # determine number of words
        best_word_amount = number_of_syllables / 2.5
        maximum_distance = number_of_syllables - best_word_amount + 1

        word_length_weights: list[tuple[int, int]] = []
        for amount_of_words in range(1, number_of_syllables + 1):
            distance = abs(amount_of_words - best_word_amount)
            weight = math.ceil((maximum_distance - distance) ** 2)
            word_length_weights.append((amount_of_words, weight))
        
        # print(word_length_weights)
        number_of_words = weighted_pull(word_length_weights)

        # determine sets of vowels
        sets_of_vowels = get_vowel_sets_from_remaining_letters(VOWEL_SETS, remaining_vowels, number_of_syllables)

        # print(f"{sets_of_vowels = }")
        # print(f"{sets_of_starting_consonants = }")
        # print(f"{sets_of_ending_consonants = }")

        # pre-build syllables with only their vowels
        # the 3-list contains the starting consonants, the vowels, and the ending consonants in that order.
        syllables = [["", vowel_set, ""] for vowel_set in sets_of_vowels]

        # determine syllable distribution
        syllable_distribution = [1] * number_of_words
        remaining_syllables = number_of_syllables - number_of_words
        for _ in range(remaining_syllables):
            syllable_distribution[random.randint(0, len(syllable_distribution) - 1)] += 1

        # determine consonants to place at joints (between vowels in the same word)
        joint_indices: list[int] = []
        syllable_index = 0
        for syllable_amount in syllable_distribution:
            if syllable_amount > 1:
                joint_indices += list(range(syllable_index, syllable_index + syllable_amount - 1))
            syllable_index += syllable_amount

        remaining_starting_consonant_indices = list(range(number_of_syllables))
        remaining_ending_consonant_indices = list(range(number_of_syllables))

        for index in joint_indices:
            if random.randint(1, len(sets_of_starting_consonants) + len(sets_of_ending_consonants)) <= len(sets_of_starting_consonants):
                syllables[index + 1][0] = sets_of_starting_consonants.pop()
                remaining_starting_consonant_indices.remove(index + 1)
            else:
                syllables[index][2] = sets_of_ending_consonants.pop()
                remaining_ending_consonant_indices.remove(index)
        
        # randomly distribute remaining consonants among the syllables
        random.shuffle(remaining_starting_consonant_indices)
        random.shuffle(remaining_ending_consonant_indices)

        for starting_consonants in sets_of_starting_consonants:
            index = remaining_starting_consonant_indices.pop()
            syllables[index][0] = starting_consonants
        
        for ending_consonants in sets_of_ending_consonants:
            index = remaining_ending_consonant_indices.pop()
            syllables[index][2] = ending_consonants

        # assemble anagram
        anagram: str = ""
        index: int = 0
        for syllable_amount in syllable_distribution:
            word = ""
            for _ in range(syllable_amount):
                word += "".join(syllables[index])
                index += 1
            
            anagram += word.capitalize() + " "
                
        return anagram.strip()

def generate_histogram(string: str) -> dict[str, int]:
    histogram: dict[str, int] = {}
    for letter in string:
        letter = letter.lower()
        if letter in histogram:
            histogram[letter] += 1
        else:
            histogram[letter] = 1
    
    return histogram

def get_set_from_remaining_letters(letter_set: list[tuple[str, int]], remaining_letters: dict[str, int], length: int = -1):
    # print(f"{remaining_letters = } | {length = }")
    valid_contenders = []
    for letters, weight in letter_set:
        if length > 0 and len(letters) != length:
            continue

        histogram = {}
        for letter in letters:
            if letter in histogram:
                histogram[letter] += 1
            else:
                histogram[letter] = 1
        
        valid_contender = True
        for letter, occurences in histogram.items():
            if not (letter in remaining_letters and remaining_letters[letter] >= occurences):
                valid_contender = False
                break
        
        if valid_contender:
            valid_contenders.append((letters, weight))
    
    # print(f"{valid_contenders = }")
    return get_set(valid_contenders)

def get_vowel_sets_from_remaining_letters(base_letter_set: list[tuple[str, int]], remaining_letters: dict[str, int], number_of_sets: int) -> list[str]:
    # print(f"{remaining_letters = } | {number_of_sets = }")

    number_of_letters = sum(remaining_letters.values())
    letter_sets: list[str] = []
    for i in range(number_of_sets):
        sets_after = number_of_sets - i - 1

        letter_set = get_set_from_remaining_letters(base_letter_set, remaining_letters, 1 if sets_after == number_of_letters - 1 else 2)
        letter_sets.append(letter_set)

        number_of_letters -= len(letter_set)
        for letter in letter_set:
            remaining_letters[letter] -= 1
    
    random.shuffle(letter_sets)
    return letter_sets

def get_consonant_sets_from_remaining_letters(remaining_letters: dict[str, int], maximum_number_of_syllables: int):
    number_of_letters = sum(remaining_letters.values())

    starting_consonant_sets: list[str] = []
    ending_consonant_sets: list[str] = []

    minimum_number_of_consonant_sets = max(maximum_number_of_syllables, math.ceil(number_of_letters / 2))
    maximum_number_of_consonant_sets = min(number_of_letters, maximum_number_of_syllables * 2)

    number_of_sets: int = 0
    while number_of_letters > 0:
        letters = -1
        if number_of_letters == minimum_number_of_consonant_sets - number_of_sets or number_of_letters == 1:
            letters = 1
        elif number_of_letters > maximum_number_of_consonant_sets - number_of_sets:
            letters = 2

        letter_set: str = ""
        if len(starting_consonant_sets) < maximum_number_of_syllables and (random.random() < 0.5 or len(ending_consonant_sets) == maximum_number_of_syllables):
            letter_set = get_set_from_remaining_letters(CONSONANT_BEFORE_VOWEL_SETS, remaining_letters, letters)
            starting_consonant_sets.append(letter_set)
        else:
            letter_set = get_set_from_remaining_letters(CONSONANT_AFTER_VOWEL_SETS, remaining_letters, letters)
            ending_consonant_sets.append(letter_set)
        
        number_of_letters -= len(letter_set)
        for letter in letter_set:
            remaining_letters[letter] -= 1
        
        number_of_sets += 1
    
    random.shuffle(starting_consonant_sets)
    random.shuffle(ending_consonant_sets)
    # print(f"{starting_consonant_sets = } | {ending_consonant_sets = }")
    return starting_consonant_sets, ending_consonant_sets

if __name__ == "__main__":
    gen = AnagramGenerator()

    string = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible."

    gen.set_string(string)

    print(string)
    print()
    print(gen.generate_anagram())

    # gen.set_word_list(["Rock", "Stone", "Ice", "Fire", "Earth", "Air"])
    # for _ in range(3):
    #     print(gen.generate_anagram())
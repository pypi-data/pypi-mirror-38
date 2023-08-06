from string import ascii_letters, digits
from typing import List, Set
import os.path


## GLOBAL VARIABLES ##
ALLOWED_CHARACTERS = set(ascii_letters)
ALLOWED_CHARACTERS.update(set(digits))
ALLOWED_CHARACTERS.update(
    set(['@', '!', '$', '^', '*', '&', '\"', '\''])
)

def get_complete_path_of_file(filename: str) -> str:
    """Join the path of the current directory with the input filename."""
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, filename)

def get_start_index_of_next_word(text: str, start_idx: int) -> int:
    start_idx_of_next_word = len(text)
    for index in iter(range(start_idx, len(text))):
        if text[index] not in ALLOWED_CHARACTERS:
            continue
        start_idx_of_next_word = index
        break

    return start_idx_of_next_word

def get_next_word_and_end_index(text: str, start_idx: int):
    next_word = ""
    index = start_idx
    for index in iter(range(start_idx, len(text))):
        char = text[index]
        if char in ALLOWED_CHARACTERS:
            next_word += char
            continue
        break
    return next_word, index

def any_next_words_form_swear_word(cur_word: str, text: str, words_indices: List[tuple], censor_words: Set[str]):
    full_word = cur_word.lower()
    for next_word, end_index in iter(words_indices):
        full_word = "%s %s" % (full_word, next_word.lower())
        if full_word in censor_words:
            return True, end_index
    return False, -1

def get_next_words(text: str, start_idx: int, num_of_next_words: int=1) -> str:
    """Return a list of next words and their end indices."""
    # Find the starting index of the next word
    start_idx_of_next_word = get_start_index_of_next_word(text, start_idx)

    # Return an empty string if there are no other words
    if start_idx_of_next_word >= len(text) - 1:
        return [("", start_idx_of_next_word)]

    # Combine the  words into a list
    next_word, end_index = get_next_word_and_end_index(text, start_idx_of_next_word)
    words =  [(next_word, end_index)]
    if num_of_next_words > 1:
        words.extend(
             get_next_words(text, end_index, num_of_next_words - 1)
        )

    return words

from generate_wordle import generate_wordle

generate_wordle("Abbrle", 
                "Wordle-Variation with Abbreviations", 
                3,
                5,
                '''def get_todays_wordle(possible_words):
    return list(possible_words.keys())[random.randint(0, len(possible_words)-1)]''', 
                "slangle_words/valid_answers.txt", 
                "slangle_words/valid_guesses.txt", 
                True, 
                "slangle")
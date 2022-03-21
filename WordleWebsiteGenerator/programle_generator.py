from generate_wordle import generate_wordle

'''
with open("programle/valid_answers.txt", "r", encoding="utf-8") as file:
    t = [_.split()[0] for _ in file.read().split("\n") if _.strip()]

with open("programle/valid_answers_5_long.txt", "w", encoding="utf-8") as file:
    s = ""
    for item in t:
        s += (item + "\n")
    s = s[:-1]
    file.write(s)
'''

generate_wordle("Programle",
                "Wordle-Variation about Programming",
                5,
                6,
                '''def get_todays_wordle(possible_words):
    return list(possible_words.keys())[random.randint(0, len(possible_words)-1)]''',
                "programle/valid_answers_5_long.txt",
                "slangle_words/valid_guesses.txt",
                False,
                "programleGame")
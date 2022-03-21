import languages, functions

def write(filename, message, language):
    functions.delete_message(filename)
    functions.inject(filename, f"{language} {message}")

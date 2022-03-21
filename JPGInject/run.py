from enum import unique
import functions, languages, uuid, os, sys, io

def run(filename):
    content = functions.get_message(filename)
    language = int(content.split()[0])
    unique_filename = str(uuid.uuid4())
    prog = content[len(str(language))+1:]
    output = None
    if language == languages.Languages.python.value: # python
        old_stdout = sys.stdout 
        new_stdout = io.StringIO() 
        sys.stdout = new_stdout
        exec(prog)
        output = sys.stdout.getvalue().strip()
    elif language == languages.Languages.executable.value: # executable
        unique_filename += ".exe"
        with open(unique_filename, "wb") as file:
            file.write(prog.encode())
        output = os.popen(f".\\{unique_filename}").read()
        os.remove(f".\\{unique_filename}")
    elif language == languages.Languages.cpp.value: # c++
        unique_filename += ".cpp"
        file2 = str(uuid.uuid4()) + ".exe"
        with open(unique_filename, "wb") as file:
            file.write(prog.encode())
        os.system(f"g++ {unique_filename} -o .\\{file2}")
        output = os.popen(f".\\{file2}").read()
        os.remove(unique_filename)
        os.remove(f".\\{file2}")
    return output


import tkinter as tk
import run, create, languages, functions
from tkinter.filedialog import askopenfilename, asksaveasfilename

JPG_FILE = ""

def create_button():
    chosen = clicked.get()
    lang = None
    if chosen == options[0]:
        lang = languages.Languages.python.value
    elif chosen == options[1]:
        lang = languages.Languages.cpp.value
    elif chosen == options[2]:
        lang = languages.Languages.executable.value
    create.write(JPG_FILE + (".jpg" if JPG_FILE.split(".")[-1] != "jpg" else ""), program_entry.get("1.0", tk.END), lang)

def run_button():
    output_label.config(text=run.run(JPG_FILE + (".jpg" if JPG_FILE.split(".")[-1] != "jpg" else "")))

def get_extension(name):
    return extensions[name]

def clear_output_button():
    output_label.config(text="")

def get_language(content):
    n = int(content.split()[0])
    langs = languages.Languages
    if n == langs.python.value:
        return options[0]
    elif n == langs.cpp.value:
        return options[1]
    elif n == langs.exe.value:
        return options[2]

def download_button():
    content = functions.get_message(JPG_FILE)
    l = get_language(content)
    ext = get_extension(l)
    filename = asksaveasfilename(title="Choose Save Destination", defaultextension=ext, filetypes=[(l, ext)])
    with open(filename, "w") as file:
        cont = functions.get_message(JPG_FILE)
        file.write(cont[len(cont.split()[0])+1:])

def choose_file():
    global JPG_FILE
    JPG_FILE = askopenfilename(filetypes=[("JPG Files", ".jpg .jpeg")])
    update_file_display()

def update_file_display():
    jpg_entry.config(text=JPG_FILE)

if __name__ == "__main__":
    window = tk.Tk()
    jpg_label = tk.Label(text="\".jpg\" File:")
    jpg_entry = tk.Label(text="")
    jpg_choose = tk.Button(text="Choose File", command=choose_file)
    program_label = tk.Label(text="Code")
    program_entry = tk.Text()
    output_label = tk.Label(text="")
    jpg_label.pack()
    jpg_entry.pack()
    jpg_choose.pack()
    program_label.pack()
    program_entry.pack()

    create_button = tk.Button(text="Create", command=create_button)
    run_button = tk.Button(text="Run", command=run_button)
    clear_output_button = tk.Button(text="Clear Output", command=clear_output_button)
    download_button = tk.Button(text="Download", command=download_button)

    create_button.pack()
    run_button.pack()
    clear_output_button.pack()
    download_button.pack()
    
    output_label.pack()

    options = [
        "Python",
        "C++",
        "Executable"
    ]

    extensions = {
        options[0]: ".py",
        options[1]: ".cpp",
        options[2]: ".exe"
    }
    
    # datatype of menu text
    clicked = tk.StringVar()
    
    # initial menu text
    clicked.set( options[0] )
    
    # Create Dropdown menu
    drop = tk.OptionMenu( window , clicked , *options )
    drop.pack()

    window.mainloop()
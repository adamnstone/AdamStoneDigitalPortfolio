with open("temp", "r") as file:
    content = file.read()
content = content.replace("\n", r"\n").replace("\\", "\\\\").replace('"', '\\\"')
with open("oneline.txt", "w") as file:
    file.write(content)

with open("oneline.txt", "r") as file:
    content = file.read()
content = content.replace("\\\\n", "\\" + "n")
with open("oneline.txt", "w") as file:
    file.write(content)
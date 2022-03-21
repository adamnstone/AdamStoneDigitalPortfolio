def get_ending(string):
    return string.index(bytes.fromhex('FFD9')) + 2

def inject(filename, message):
    with open(filename, "ab") as file:
        file.write(message.encode())

def get_message(filename):
    with open(filename, "rb") as file:
        content = file.read()
        offset = get_ending(content)

        file.seek(offset)

        return file.read().decode()

def delete_message(filename):
    with open(filename, "rb") as file_read:
            content = file_read.read()
            content = content[:get_ending(content)]
    with open(filename, "wb") as file_write:
        file_write.write(content)
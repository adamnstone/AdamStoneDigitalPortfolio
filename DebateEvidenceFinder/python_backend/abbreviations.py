from typing import Dict
import re
from python_backend.constants import HELPER_FILES_FOLDER, PYTHON_BACKEND_FOLDER

def get_abbreviations(file: str) -> Dict[str, str]:
    with open(file, "r") as file:
        content = file.read().split("\n")
        abbs = []
        for line in content:
            spl = [_.lower().strip() for _ in line.split(",")]
            abbs.append((spl[0], spl[1]))
    return sorted(abbs, key=lambda abb: len(abb[0]))[::-1]

ABBREVIATIONS_FILE = f"{PYTHON_BACKEND_FOLDER}/{HELPER_FILES_FOLDER}/abbreviations.txt"
ABBREVIATIONS = get_abbreviations(ABBREVIATIONS_FILE)

def replace_abbreviations(tag):
    tag = tag.lower()
    formatted_tag = ""
    i = 0
    while i < len(tag):
        for abb in ABBREVIATIONS:
            if i == 0:
                if len(abb[0]) + 1 <= len(tag) and re.match(fr"{abb[0]}[^a-zA-Z]", tag[:i+len(abb[0])+1]):
                    formatted_tag += abb[1]
                    i += len(abb[0])
                    break
                elif len(abb[0]) == len(tag):
                    if abb[0] == tag:
                        formatted_tag += abb[1]
                        i += len(abb[0])
                        break
            if i + len(abb[0]) + 1 <= len(tag) and \
                re.match(fr"[^a-zA-Z]{abb[0]}", tag[i:i+len(abb[0])+1]):
                    if i+len(abb[0])+2 > len(tag):
                        formatted_tag += tag[i] + abb[1]
                        i += len(abb[0])+1
                        break
                    elif re.match(r"[^a-zA-Z]", tag[i+len(abb[0])+1]):
                        formatted_tag += tag[i] + abb[1]
                        i += len(abb[0])+1
                        break
        else:
            formatted_tag += tag[i]
            i += 1
    return formatted_tag
from fuzzywuzzy import fuzz
import python_backend.abbreviations, string, re

class Card(object):
    def __init__(self, tag: str, citation: str, text: str, preview_length_chars=1000) -> None:
        self.original_tag = tag
        tag = tag.lower()
        self.tag = python_backend.abbreviations.replace_abbreviations(tag)
        self.tag_original_no_formatting = tag
        self.tag_original = self.format_tag(tag)
        self.citation = citation
        self.text = text
        self.preview_length_chars = preview_length_chars
        self.preview = self.cut_preview()
        self.formatted_tag_as_filename = self.format_tag_as_filename(self.tag_original)

    def cut_preview(self):
        return f"{self.text.text[:self.preview_length_chars].strip()}..."

    def format_tag_as_filename(self, tag):
        final = "CARD_"
        valid_chars = f"-_(){string.ascii_letters}{string.digits}"
        for char in tag[:25]:
            final += char if char in valid_chars else "_"
        return final + ".docx"

    def remove_tag_excess(self, tag):
        return re.sub("\d*\)", "", re.sub("\[\d*\]", "", tag)).strip()

    def format_tag(self, tag):
        return ". ".join([sentence.strip().capitalize() for sentence in self.remove_tag_excess(tag).split(".")])

    def find_similarity(self, other) -> float:
        other_str = None
        if isinstance(other, type(self)):
            other_str = other.tag
        elif isinstance(other, str):
            other_str = other
        else:
            raise Exception(f"Argument {other} not of Type {type(self)} or str")
        return fuzz.partial_ratio(self.tag, other_str)

    def get_tag(self):
        return self.tag_original

    def __str__(self) -> str:
        return self.original_tag


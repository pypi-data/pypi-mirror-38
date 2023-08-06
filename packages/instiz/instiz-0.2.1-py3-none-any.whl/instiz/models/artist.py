from re import search
from unicodedata import name


class Artist(object):
    def __init__(self, artist):
        self.raw_name = artist
        self.korean_name = None
        self.english_name = None
        self._artist_normalizer()

    def __str__(self):
        return (
            self.korean_name if self.english_name == "" else self.english_name
        )

    def _artist_normalizer(self):
        is_parenthesis = search(r"\(([^)]+)", self.raw_name)
        if is_parenthesis is None:
            self.english_name, self.korean_name = self.raw_name, ""
        else:
            inside_parenthesis = is_parenthesis.group(1)
            outside_parenthesis = (
                self.raw_name.replace(inside_parenthesis, "")
                .replace("()", "")
                .strip()
            )
            self.english_name, self.korean_name = (
                outside_parenthesis,
                inside_parenthesis,
            )
        if self._hangul_checker(self.english_name):
            self.korean_name, self.english_name = (
                self.english_name,
                self.korean_name,
            )

    def _hangul_checker(self, string):
        return "HANGUL" in name(string[0])

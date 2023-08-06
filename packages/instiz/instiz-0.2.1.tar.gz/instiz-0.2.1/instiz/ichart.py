from bs4 import BeautifulSoup
from re import compile
from requests import get
from .CONSTANTS import CHANGES, HEADERS, URL
from .helper import return_int_from_image_url as int_parse
from .models import Entry


class iChart:
    def __init__(self):
        self.entries = []
        self.doc = None
        self._generator = None
        self._post_init()

    def get_next_entry(self):
        """Function that returns the next entry of the iChart onwards"""
        self._add_to_list()
        return self.entries[-1]

    def realtime_top_10(self):
        """Function that returns a list of current top 10 entries on iChart"""
        while len(self.entries) < 10:
            self._add_to_list()
        return self.entries[:10]

    def refresh(self):
        """
        Refreshes the instance.
        Returns self, so the call can be inlined with other function call
        """
        self._make_request()
        self.entries = []
        self._generator = self._entry_iterator()
        return self

    def _add_to_list(self):
        self.entries.append(next(self._generator))

    def _make_request(self):
        request = get(URL, headers=HEADERS, timeout=15)
        self.doc = BeautifulSoup(request.text, "lxml")

    def _entry_iterator(self):
        result_set = self.doc.find_all(
            class_=compile("spage_score_item(_1st)*")
        )
        for div in result_set:
            yield self._parse_score(div)

    def _parse_score(self, div):
        title = div.find(class_=compile("ichart_score[0-9]*_song1")).text
        artist = div.find(class_=compile("ichart_score[0-9]*_artist1")).text
        rank = int_parse(
            div.find(class_=compile("ichart_score[0-9]*_rank")).img["src"]
        )
        change = div.find(class_=compile("ichart_score[0-9]*_change"))
        change_class = CHANGES[change.span["class"][1]]
        change_rank = int(change.text) if change.text != "" else 0
        score_div = div.find(
            class_=compile("ichart_score[0-9]*_score")
        ).find_all("img")
        score = int(
            "".join([str(int_parse(score["src"])) for score in score_div])
        )
        return Entry(title, artist, rank, change_class, change_rank, score)

    def _post_init(self):
        self._make_request()
        self._generator = self._entry_iterator()


import attr
from instiz.models import Artist


@attr.s
class Entry(object):
    title = attr.ib(type=str)
    artist = attr.ib(converter=Artist)
    rank = attr.ib(type=int)
    change_class = attr.ib(type=str)
    change_amount = attr.ib(type=int)
    score = attr.ib(type=int)

    @property
    def change(self):
        return {"class": self.change_class, "amount": self.change_amount}

    @property
    def nice_title(self):
        return str(self.artist) + " - " + self.title

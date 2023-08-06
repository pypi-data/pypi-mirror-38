import attr


@attr.s
class Entry(object):
    title = attr.ib(type=str)
    artist = attr.ib(type=str)
    rank = attr.ib(type=int)
    change_class = attr.ib(type=str)
    change_amount = attr.ib(type=int)
    score = attr.ib(type=int)

    @property
    def change(self):
        return {"class": self.change_class, "amount": self.change_amount}

    def nice_title(self):
        return self.artist + " - " + self.title

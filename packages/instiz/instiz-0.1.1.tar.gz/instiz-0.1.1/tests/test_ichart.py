import pytest
from instiz import iChart


@pytest.fixture
def class_init():
    ichart = iChart()
    return ichart


def test_10(class_init):
    assert len(class_init.realtime_top_10()) == 10


def test_refresh(class_init):
    x = class_init.refresh()
    assert isinstance(x, iChart)


def test_refresh_clear_entries(class_init):
    class_init.realtime_top_10()
    class_init.refresh()
    assert len(class_init.entries) == 0


def test_get_rank(class_init):
    x = class_init.get_next_entry()
    assert x.rank == 1


def test_changes_in_entry(class_init):
    x = class_init.get_next_entry()
    assert "class" in x.change


def test_nice_title_formatting(class_init):
    x = class_init.get_next_entry()
    assert x.nice_title() == x.artist + " - " + x.title

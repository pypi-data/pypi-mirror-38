import pytest
from instiz.models import Artist


@pytest.fixture
def korean_name_only():
    return Artist("황치열")


@pytest.fixture
def english_name_only():
    return Artist("EXO")


@pytest.fixture
def korean_name_inside_spaced_parentheses():
    return Artist("TWICE (트와이스)")


@pytest.fixture
def english_name_inside_spaced_parentheses():
    return Artist("제니 (JENNIE)")


@pytest.fixture
def korean_name_inside_unspaced_parentheses():
    return Artist("Queen(퀸)")


@pytest.fixture
def english_name_inside_unspaced_parentheses():
    return Artist("아이유(IU)")


@pytest.fixture
def two_name_inside_parentheses():
    return Artist("샘김(SAM KIM)")


@pytest.fixture
def two_name_outside_parentheses():
    return Artist("SAM KIM(샘김)")


def test_get_english_name_from_artist_with_english_name_only(english_name_only):
    assert english_name_only.english_name == "EXO"


def test_get_korean_name_from_artist_with_english_name_only(english_name_only):
    assert english_name_only.korean_name == ""


def test_str_if_english_name_only(english_name_only):
    assert str(english_name_only) == "EXO"


def test_get_korean_name_from_artist_with_korean_name_only(korean_name_only):
    assert korean_name_only.korean_name == "황치열"


def test_get_english_name_from_artist_with_korean_name_only(korean_name_only):
    assert korean_name_only.english_name == ""


def test_str_if_korean_name_only(korean_name_only):
    assert str(korean_name_only) == "황치열"


def test_get_english_name_where_(korean_name_inside_spaced_parentheses):
    assert korean_name_inside_spaced_parentheses.english_name == "TWICE"


def test_get_korean_name_where_(korean_name_inside_spaced_parentheses):
    assert korean_name_inside_spaced_parentheses.korean_name == "트와이스"


def test_get_str_where_(korean_name_inside_spaced_parentheses):
    assert str(korean_name_inside_spaced_parentheses) == "TWICE"


def test_english_name_where_(english_name_inside_spaced_parentheses):
    assert english_name_inside_spaced_parentheses.english_name == "JENNIE"


def test_korean_name_where_(english_name_inside_spaced_parentheses):
    assert english_name_inside_spaced_parentheses.korean_name == "제니"


def test_str_where_(english_name_inside_spaced_parentheses):
    assert str(english_name_inside_spaced_parentheses) == "JENNIE"


def test_english_name_where__(korean_name_inside_unspaced_parentheses):
    assert korean_name_inside_unspaced_parentheses.english_name == "Queen"


def test_korean_name_where__(korean_name_inside_unspaced_parentheses):
    assert korean_name_inside_unspaced_parentheses.korean_name == "퀸"


def test_str_where__(korean_name_inside_unspaced_parentheses):
    assert str(korean_name_inside_unspaced_parentheses) == "Queen"


def test_get_english_name_if_(english_name_inside_unspaced_parentheses):
    assert english_name_inside_unspaced_parentheses.english_name == "IU"


def test_get_korean_name_if_(english_name_inside_unspaced_parentheses):
    assert english_name_inside_unspaced_parentheses.korean_name == "아이유"


def test_get_str_if_(english_name_inside_unspaced_parentheses):
    assert str(english_name_inside_unspaced_parentheses) == "IU"


def test_english_name_if_(two_name_inside_parentheses):
    assert two_name_inside_parentheses.english_name == "SAM KIM"


def test_korean_name_if_(two_name_inside_parentheses):
    assert two_name_inside_parentheses.korean_name == "샘김"


def test_str_if_(two_name_inside_parentheses):
    assert str(two_name_inside_parentheses) == "SAM KIM"


def test_english_name_if__(two_name_outside_parentheses):
    assert two_name_outside_parentheses.english_name == "SAM KIM"


def test_korean_name_if__(two_name_outside_parentheses):
    assert two_name_outside_parentheses.korean_name == "샘김"


def test_str_if__(two_name_outside_parentheses):
    assert str(two_name_outside_parentheses) == "SAM KIM"

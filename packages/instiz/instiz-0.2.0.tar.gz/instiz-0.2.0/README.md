# instiz

A Python3-only library for iChart K-Pop chart scores.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Installation

`pip install instiz`

## Getting Started

Getting started is easy. The following example is to get the top 10 at the realtime chart of iChart.

```python
from instiz import iChart

ichart = iChart()
top_10 = ichart.realtime_top_10()

```

## Type hinting

If you're using Python 3.7+'s type hinting feature, the type used for the return type of the chart can be imported from the `instiz.models` module.

```python
from instiz.models import Entry

def get_name(entry: Entry) -> str:
    return entry.title

```

## Artist name

It's now possible to get the Korean name and the English name of an artist easily, alongside with the raw artist name provided from iChart's site. Nice title property will always return the English name, unless unavailable. If one of the names are unavailable, the property will return an empty string.

```python
from instiz import iChart

ichart = iChart()
first_place = ichart.get_next_entry()
nice_title = first_place.nice_title # JENNIE - SOLO
raw_artist_name = first_place.artist.raw_name # 제니 (JENNIE)
english_artist_name = first_place.artist.english_name # JENNIE
korean_artist_name = first_place.artist.korean_name # 제니

```

## Contributing

* Fork the repo
* Make your changes
* Write your tests so I don't accidentally remove it when updating
* Run the tests.
* Make a pull request.

## TODO

- [ ] Document the API
- [ ] Weekly chart
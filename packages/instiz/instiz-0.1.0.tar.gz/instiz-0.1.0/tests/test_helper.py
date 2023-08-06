import pytest
from instiz.helper import return_int_from_image_url


def test_return_int_from_image_url():
    assert (
        return_int_from_image_url(
            "http://cfs.tistory.com/custom/blog/44/444693/skin/images/1.png"
        )
        == 1
    )


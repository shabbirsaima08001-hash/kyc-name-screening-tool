"""Simple tests. Run with:  python -m pytest   (or just: python test_screening.py)"""
import pandas as pd
from screening import normalize, match_score, classify, screen_name

WATCHLIST = pd.DataFrame({"name": ["Mohammad Al Hassan", "Viktor Petrovich Ivanov"],
                          "list_type": ["SANCTIONS", "SANCTIONS"]})


def test_normalize():
    assert normalize("  José-Maria  O'Neil ") == "jose maria o neil"


def test_spelling_variant_is_a_hit():
    assert classify(match_score("Muhammad Al Hasan", "Mohammad Al Hassan")) == "HIT"


def test_word_order_does_not_matter():
    assert match_score("Hassan Mohammad Al", "Mohammad Al Hassan") >= 85


def test_missing_middle_name_still_matches():
    assert classify(match_score("Viktor Ivanov", "Viktor Petrovich Ivanov")) == "HIT"


def test_different_name_is_clear():
    assert screen_name("Sara Verdi", WATCHLIST).iloc[0]["status"] == "CLEAR"


if __name__ == "__main__":
    for t in [test_normalize, test_spelling_variant_is_a_hit, test_word_order_does_not_matter,
              test_missing_middle_name_still_matches, test_different_name_is_clear]:
        t()
        print("OK ", t.__name__)

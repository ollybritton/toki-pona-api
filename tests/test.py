import unittest
from server import fetch_word_data, search_data


def test_fetch_word_data():
    word_data = fetch_word_data()
    assert type(word_data) == list


def test_search_data_type():
    word_data = fetch_word_data()
    example_search = search_data("a", word_data)
    assert type(example_search) == list


def test_search_data_results():
    word_data = fetch_word_data()
    example_search = search_data("a", word_data)
    assert len(example_search) > 0


def test_search_data_accurate():
    word_data = fetch_word_data()
    example_search = search_data("a", word_data)
    assert example_search[0]['word'] == "a"


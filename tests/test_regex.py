
import pytest

from core.regex_parser import RegexParser


def test_simple_expression():
    parser = RegexParser("ab")
    assert parser.to_postfix() == ["a", "b", "."]


def test_union():
    parser = RegexParser("a|b")
    assert parser.to_postfix() == ["a", "b", "|"]


def test_kleene_star():
    parser = RegexParser("a*")
    assert parser.to_postfix() == ["a", "*"]


def test_parentheses():
    parser = RegexParser("(a|b)*")
    assert parser.to_postfix() == ["a", "b", "|", "*"]


def test_complex_expression():
    parser = RegexParser("(a|b)*abb")
    assert parser.to_postfix() == [
        "a", "b", "|", "*",
        "a", ".", "b", ".", "b", "."
    ]


def test_invalid_expression():
    with pytest.raises(ValueError):
        RegexParser("a|").to_postfix()


import pytest

from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa
from core.recognizer import DFARecognizer
from core.equivalence import check_equivalence


def build_engine(expression):
    parser = RegexParser(expression)

    nfa = build_nfa(parser.to_postfix())

    dfa = convert_nfa_to_dfa(nfa)

    minimized = minimize_dfa(dfa)

    return nfa, dfa, minimized


def test_complete_pipeline():
    nfa, dfa, minimized = build_engine("(a|b)*abb")

    assert len(nfa.states) == 14
    assert len(dfa.states) == 5
    assert len(minimized.states) == 4


def test_language_recognition_across_patterns():

    test_cases = [
        ("a*", ["", "a", "aa", "aaa"], ["b", "ab"]),
        ("a|b", ["a", "b"], ["", "ab", "ba"]),
        ("ab*", ["a", "ab", "abb"], ["", "b", "ba"]),
        ("(a|b)*", ["", "a", "b", "ab", "ba"], ["c"])
    ]

    for expression, accepted, rejected in test_cases:

        _, _, minimized = build_engine(expression)

        recognizer = DFARecognizer(minimized)

        for string in accepted:
            result = recognizer.recognize(string)
            assert result["accepted"], (
                f"{expression} should accept {string!r}"
            )

        for string in rejected:
            result = recognizer.recognize(string)
            assert not result["accepted"], (
                f"{expression} should reject {string!r}"
            )


def test_equivalent_expressions():
    _, _, dfa1 = build_engine("(a|b)*")

    _, _, dfa2 = build_engine("(b|a)*")

    result = check_equivalence(dfa1, dfa2)

    assert result["equivalent"] is True


def test_non_equivalent_expressions():
    _, _, dfa1 = build_engine("a*")

    _, _, dfa2 = build_engine("b*")

    result = check_equivalence(dfa1, dfa2)

    assert result["equivalent"] is False
    assert result["counterexample"] is not None


def test_invalid_expression_handling():

    invalid_expressions = [
        "",
        "a|",
        "|a",
        "(ab",
        "ab)",
        "*a"
    ]

    for expression in invalid_expressions:

        with pytest.raises(ValueError):
            build_engine(expression)


def test_minimized_dfa_is_not_larger_than_original():

    expressions = [
        "a",
        "a*",
        "a|b",
        "ab",
        "(a|b)*abb",
        "(a|b)*"
    ]

    for expression in expressions:

        _, dfa, minimized = build_engine(expression)

        assert len(minimized.states) <= len(dfa.states)

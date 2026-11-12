
import pytest

from core.regex_parser import RegexParser
from core.nfa import build_nfa


def create_nfa(expression):
    parser = RegexParser(expression)
    postfix = parser.to_postfix()

    return build_nfa(postfix)


def test_single_symbol():
    nfa = create_nfa("a")

    assert len(nfa.states) == 2
    assert nfa.alphabet == {"a"}

    assert nfa.start_state != nfa.accept_state

    assert nfa.get_transitions(
        nfa.start_state, "a"
    ) == {nfa.accept_state}


def test_union():
    nfa = create_nfa("a|b")

    assert len(nfa.states) == 6

    assert nfa.alphabet == {"a", "b"}

    assert nfa.get_transitions(
        nfa.start_state, "ε"
    )


def test_concatenation():
    nfa = create_nfa("ab")

    assert len(nfa.states) == 4

    assert nfa.get_transitions(
        1, "ε"
    ) == {2}


def test_kleene_star():
    nfa = create_nfa("a*")

    assert len(nfa.states) == 4

    assert nfa.get_transitions(
        nfa.start_state, "ε"
    )

    assert nfa.get_transitions(
        1, "ε"
    )


def test_complex_expression():
    nfa = create_nfa("(a|b)*abb")

    assert len(nfa.states) == 14

    assert nfa.alphabet == {"a", "b"}


def test_invalid_postfix():
    with pytest.raises(ValueError):
        build_nfa(["a", "|"])


def test_extra_operands():
    with pytest.raises(ValueError):
        build_nfa(["a", "b"])


def test_empty_postfix():
    with pytest.raises(ValueError):
        build_nfa([])

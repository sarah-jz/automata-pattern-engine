
import pytest

from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa, SubsetConstruction


def create_nfa(expression):
    parser = RegexParser(expression)
    return build_nfa(parser.to_postfix())


def create_dfa(expression):
    nfa = create_nfa(expression)
    return convert_nfa_to_dfa(nfa)


def accepts(dfa, string):
    """Small helper to test DFA acceptance."""

    current_state = dfa.start_state

    for symbol in string:

        current_state = dfa.get_transition(
            current_state,
            symbol
        )

        if current_state is None:
            return False

    return current_state in dfa.accept_states


def test_epsilon_closure():
    nfa = create_nfa("a|b")

    converter = SubsetConstruction(nfa)

    closure = converter.epsilon_closure(
        {nfa.start_state}
    )

    assert nfa.start_state in closure
    assert len(closure) > 1


def test_move():
    nfa = create_nfa("a")

    converter = SubsetConstruction(nfa)

    result = converter.move(
        {nfa.start_state},
        "a"
    )

    assert result == {nfa.accept_state}


def test_dfa_creation():
    dfa = create_dfa("a")

    assert len(dfa.states) == 3
    assert dfa.alphabet == {"a"}
    assert dfa.start_state == 0


def test_dfa_is_deterministic():
    dfa = create_dfa("(a|b)*abb")

    for state in dfa.states:
        for symbol in dfa.alphabet:

            assert (
                state, symbol
            ) in dfa.transitions


def test_dfa_accepts_correct_strings():
    dfa = create_dfa("(a|b)*abb")

    assert accepts(dfa, "abb")
    assert accepts(dfa, "aabb")
    assert accepts(dfa, "babb")
    assert accepts(dfa, "aaabb")


def test_dfa_rejects_incorrect_strings():
    dfa = create_dfa("(a|b)*abb")

    assert not accepts(dfa, "ab")
    assert not accepts(dfa, "aba")
    assert not accepts(dfa, "abba")
    assert not accepts(dfa, "aab")


def test_empty_string():
    dfa = create_dfa("a*")

    assert accepts(dfa, "")


def test_dead_state():
    dfa = create_dfa("a")

    dead_state = dfa.get_transition(
        dfa.start_state,
        "a"
    )

    # The empty subset must be reachable on another 'a'.
    empty_state = dfa.get_transition(
        dead_state,
        "a"
    )

    assert empty_state is not None

    # Once reached, the dead state loops to itself.
    assert dfa.get_transition(
        empty_state,
        "a"
    ) == empty_state

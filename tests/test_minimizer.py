
import itertools

from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa


def create_dfa(expression):
    parser = RegexParser(expression)
    nfa = build_nfa(parser.to_postfix())
    return convert_nfa_to_dfa(nfa)


def accepts(dfa, string):
    current_state = dfa.start_state

    for symbol in string:
        current_state = dfa.get_transition(
            current_state,
            symbol
        )

    return current_state in dfa.accept_states


def test_minimization_reduces_state_count():
    dfa = create_dfa("(a|b)*abb")

    minimized = minimize_dfa(dfa)

    assert len(dfa.states) == 5
    assert len(minimized.states) == 4


def test_minimized_dfa_accepts_correct_strings():
    minimized = minimize_dfa(
        create_dfa("(a|b)*abb")
    )

    assert accepts(minimized, "abb")
    assert accepts(minimized, "aabb")
    assert accepts(minimized, "babb")
    assert accepts(minimized, "aaabb")


def test_minimized_dfa_rejects_incorrect_strings():
    minimized = minimize_dfa(
        create_dfa("(a|b)*abb")
    )

    assert not accepts(minimized, "ab")
    assert not accepts(minimized, "aba")
    assert not accepts(minimized, "abba")
    assert not accepts(minimized, "aab")


def test_minimization_preserves_language():
    original = create_dfa("(a|b)*abb")
    minimized = minimize_dfa(original)

    # Compare both automata on every string of length 0 to 6.
    for length in range(7):

        for characters in itertools.product("ab", repeat=length):

            string = "".join(characters)

            assert accepts(original, string) == accepts(
                minimized,
                string
            )


def test_minimize_single_symbol():
    dfa = create_dfa("a")
    minimized = minimize_dfa(dfa)

    assert len(minimized.states) == 3


def test_minimize_kleene_star():
    dfa = create_dfa("a*")
    minimized = minimize_dfa(dfa)

    assert len(minimized.states) == 1

    assert accepts(minimized, "")
    assert accepts(minimized, "a")
    assert accepts(minimized, "aaaa")

    assert not accepts(minimized, "b")

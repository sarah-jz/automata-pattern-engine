
from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa
from core.equivalence import check_equivalence


def create_minimized_dfa(expression):
    parser = RegexParser(expression)
    nfa = build_nfa(parser.to_postfix())
    dfa = convert_nfa_to_dfa(nfa)

    return minimize_dfa(dfa)


def test_identical_expressions_are_equivalent():
    dfa1 = create_minimized_dfa("a*")
    dfa2 = create_minimized_dfa("a*")

    result = check_equivalence(dfa1, dfa2)

    assert result["equivalent"] is True
    assert result["counterexample"] is None


def test_different_expressions_can_be_equivalent():
    # a*a* and a* describe the same language.
    dfa1 = create_minimized_dfa("a*")
    dfa2 = create_minimized_dfa("a*a*")

    result = check_equivalence(dfa1, dfa2)

    assert result["equivalent"] is True


def test_non_equivalent_expressions():
    dfa1 = create_minimized_dfa("a*")
    dfa2 = create_minimized_dfa("a")

    result = check_equivalence(dfa1, dfa2)

    assert result["equivalent"] is False
    assert result["counterexample"] == ""



def test_counterexample_is_valid():
    dfa1 = create_minimized_dfa("a*")
    dfa2 = create_minimized_dfa("b*")

    result = check_equivalence(dfa1, dfa2)

    counterexample = result["counterexample"]

    assert result["equivalent"] is False

    def accepts(dfa, word):
        state = dfa.start_state

        for symbol in word:
            state = dfa.get_transition(state, symbol)

            if state is None:
                return False

        return state in dfa.accept_states

    assert accepts(dfa1, counterexample) != accepts(
        dfa2, counterexample
    )

def test_different_alphabets():
    dfa1 = create_minimized_dfa("a*")
    dfa2 = create_minimized_dfa("b*")

    result = check_equivalence(dfa1, dfa2)

    assert result["equivalent"] is False
    assert result["counterexample"] is not None


def test_equivalent_complex_expressions():
    dfa1 = create_minimized_dfa("(a|b)*")
    dfa2 = create_minimized_dfa("(b|a)*")

    result = check_equivalence(dfa1, dfa2)

    assert result["equivalent"] is True


def test_shortest_counterexample():
    dfa1 = create_minimized_dfa("(a|b)*abb")
    dfa2 = create_minimized_dfa("(a|b)*ab")

    result = check_equivalence(dfa1, dfa2)

    assert result["equivalent"] is False
    assert len(result["counterexample"]) == 2

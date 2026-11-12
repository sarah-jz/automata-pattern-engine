
from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa
from core.recognizer import DFARecognizer


def create_minimized_dfa(expression):
    parser = RegexParser(expression)
    nfa = build_nfa(parser.to_postfix())
    dfa = convert_nfa_to_dfa(nfa)

    return minimize_dfa(dfa)


def test_accept_valid_string():
    dfa = create_minimized_dfa("(a|b)*abb")
    recognizer = DFARecognizer(dfa)

    result = recognizer.recognize("abb")

    assert result["accepted"] is True


def test_reject_invalid_string():
    dfa = create_minimized_dfa("(a|b)*abb")
    recognizer = DFARecognizer(dfa)

    result = recognizer.recognize("aba")

    assert result["accepted"] is False


def test_trace_records_every_transition():
    dfa = create_minimized_dfa("(a|b)*abb")
    recognizer = DFARecognizer(dfa)

    result = recognizer.recognize("abb")

    assert len(result["trace"]) == 3

    for step in result["trace"]:
        assert step["status"] == "success"


def test_final_state_is_correct():
    dfa = create_minimized_dfa("(a|b)*abb")
    recognizer = DFARecognizer(dfa)

    result = recognizer.recognize("abb")

    assert result["final_state"] in dfa.accept_states


def test_invalid_alphabet_symbol():
    dfa = create_minimized_dfa("(a|b)*abb")
    recognizer = DFARecognizer(dfa)

    result = recognizer.recognize("abc")

    assert result["accepted"] is False
    assert result["trace"][-1]["status"] == "invalid_symbol"


def test_empty_string():
    dfa = create_minimized_dfa("a*")
    recognizer = DFARecognizer(dfa)

    result = recognizer.recognize("")

    assert result["accepted"] is True
    assert len(result["trace"]) == 0


def test_rejection_after_valid_transitions():
    dfa = create_minimized_dfa("(a|b)*abb")
    recognizer = DFARecognizer(dfa)

    result = recognizer.recognize("ab")

    assert result["accepted"] is False
    assert len(result["trace"]) == 2

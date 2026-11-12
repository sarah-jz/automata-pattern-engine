
from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa

from visualization.automata_graph import (
    create_nfa_graph,
    create_dfa_graph
)


def create_automata(expression):
    parser = RegexParser(expression)
    nfa = build_nfa(parser.to_postfix())

    dfa = convert_nfa_to_dfa(nfa)
    minimized = minimize_dfa(dfa)

    return nfa, dfa, minimized


def test_nfa_graph_creation():
    nfa, _, _ = create_automata("(a|b)*abb")

    graph = create_nfa_graph(nfa)

    assert graph is not None
    assert "Epsilon-NFA" in graph.source


def test_nfa_graph_contains_epsilon_transitions():
    nfa, _, _ = create_automata("(a|b)*abb")

    graph = create_nfa_graph(nfa)

    assert "ε" in graph.source


def test_dfa_graph_creation():
    _, dfa, _ = create_automata("(a|b)*abb")

    graph = create_dfa_graph(dfa)

    assert graph is not None
    assert "Deterministic Finite Automaton" in graph.source


def test_minimized_dfa_graph_creation():
    _, _, minimized = create_automata("(a|b)*abb")

    graph = create_dfa_graph(minimized)

    assert graph is not None
    assert len(minimized.states) == 4


def test_graph_contains_start_state():
    _, dfa, _ = create_automata("(a|b)*abb")

    graph = create_dfa_graph(dfa)

    expected_start_arrow = f"start -> {dfa.start_state}"

    assert expected_start_arrow in graph.source

def test_graph_contains_accepting_states():
    _, dfa, _ = create_automata("(a|b)*abb")

    graph = create_dfa_graph(dfa)

    assert "doublecircle" in graph.source

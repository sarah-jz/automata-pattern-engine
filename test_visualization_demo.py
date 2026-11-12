
from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa

from visualization.automata_graph import (
    create_nfa_graph,
    create_dfa_graph
)


expression = "(a|b)*abb"

parser = RegexParser(expression)

nfa = build_nfa(parser.to_postfix())
dfa = convert_nfa_to_dfa(nfa)
minimized = minimize_dfa(dfa)

# Generate diagrams.
nfa_graph = create_nfa_graph(nfa)
dfa_graph = create_dfa_graph(dfa)
minimized_graph = create_dfa_graph(minimized)

# Save diagrams as SVG files.
nfa_graph.render(
    "nfa_diagram",
    cleanup=True,
    view=False
)

dfa_graph.render(
    "dfa_diagram",
    cleanup=True,
    view=False
)

minimized_graph.render(
    "minimized_dfa_diagram",
    cleanup=True,
    view=False
)

print("Automata diagrams generated successfully!")

print("NFA states:", len(nfa.states))
print("DFA states:", len(dfa.states))
print("Minimized DFA states:", len(minimized.states))

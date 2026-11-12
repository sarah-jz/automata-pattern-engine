
from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa


def build_automata(expression):
    """
    Convert a regular expression into an epsilon-NFA,
    DFA and minimized DFA.

    Returns all generated automata and the postfix expression.
    """

    if not expression or not expression.strip():
        raise ValueError("Please enter a regular expression.")

    parser = RegexParser(expression)

    postfix = parser.to_postfix()

    nfa = build_nfa(postfix)

    dfa = convert_nfa_to_dfa(nfa)

    minimized_dfa = minimize_dfa(dfa)

    return {
        "postfix": postfix,
        "nfa": nfa,
        "dfa": dfa,
        "minimized_dfa": minimized_dfa
    }


from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa
from core.equivalence import check_equivalence


def build_automaton(expression):
    parser = RegexParser(expression)
    nfa = build_nfa(parser.to_postfix())
    dfa = convert_nfa_to_dfa(nfa)

    return minimize_dfa(dfa)


expression1 = "(a|b)*abb"
expression2 = "(a|b)*ab"

dfa1 = build_automaton(expression1)
dfa2 = build_automaton(expression2)

result = check_equivalence(dfa1, dfa2)

print("\nAUTOMATA EQUIVALENCE CHECK")
print("--------------------------")

print("Expression 1:", expression1)
print("Expression 2:", expression2)

print("\nEquivalent:", result["equivalent"])
print("Message:", result["message"])

if not result["equivalent"]:
    print(
        "Counterexample:",
        repr(result["counterexample"])
    )

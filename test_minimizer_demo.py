
from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa


expression = "(a|b)*abb"

# Construct NFA
parser = RegexParser(expression)
nfa = build_nfa(parser.to_postfix())

# Convert to DFA
dfa = convert_nfa_to_dfa(nfa)

# Minimize DFA
minimized = minimize_dfa(dfa)

print("\nREGULAR EXPRESSION:", expression)

print("\nSTATE COUNT COMPARISON")
print("----------------------")
print("NFA:", len(nfa.states))
print("DFA:", len(dfa.states))
print("Minimized DFA:", len(minimized.states))

print("\nMINIMIZED DFA")
minimized.display()

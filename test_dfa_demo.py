
from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa


expression = "(a|b)*abb"

# Step 1: Parse the regular expression
parser = RegexParser(expression)
postfix = parser.to_postfix()

# Step 2: Construct the NFA
nfa = build_nfa(postfix)

# Step 3: Convert NFA into DFA
dfa = convert_nfa_to_dfa(nfa)

# Display results
print("Original expression:", expression)
print("Postfix:", postfix)

print("\nNFA state count:", len(nfa.states))
print("DFA state count:", len(dfa.states))

dfa.display()

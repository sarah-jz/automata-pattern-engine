
from core.regex_parser import RegexParser
from core.nfa import build_nfa

expression = "(a|b)*abb"

parser = RegexParser(expression)

postfix = parser.to_postfix()

nfa = build_nfa(postfix)

print("Original expression:", expression)
print("Postfix expression:", postfix)

nfa.display()

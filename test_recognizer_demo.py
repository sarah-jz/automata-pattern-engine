
from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa
from core.recognizer import DFARecognizer


expression = "(a|b)*abb"

parser = RegexParser(expression)
nfa = build_nfa(parser.to_postfix())

dfa = convert_nfa_to_dfa(nfa)
minimized_dfa = minimize_dfa(dfa)

recognizer = DFARecognizer(minimized_dfa)

test_strings = [
    "abb",
    "aabb",
    "babb",
    "aba",
    "ab",
    "abba",
    "abc"
]

for string in test_strings:

    print("\nTesting string:", repr(string))

    result = recognizer.recognize(string)

    recognizer.display_trace(result)

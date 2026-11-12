
from services.automata_service import build_automata
from core.equivalence import check_equivalence


def compare_expressions(first_dfa, second_expression):
    """
    Compare two regular expressions by checking
    the equivalence of their minimized DFAs.
    """

    second_result = build_automata(second_expression)

    comparison = check_equivalence(
        first_dfa,
        second_result["minimized_dfa"]
    )

    return {
        "comparison": comparison,
        "second_automata": second_result
    }

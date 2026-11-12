
from core.recognizer import DFARecognizer


def recognize_string(dfa, input_string):
    """
    Recognize a single input string using the supplied DFA.
    """
    recognizer = DFARecognizer(dfa)

    return recognizer.recognize(input_string)


def recognize_batch(dfa, strings):
    """
    Recognize multiple input strings using the supplied DFA.
    """

    recognizer = DFARecognizer(dfa)

    results = []

    for string in strings:

        recognition = recognizer.recognize(string)

        results.append({
            "Input String": repr(string),
            "Result": (
                "Accepted"
                if recognition["accepted"]
                else "Rejected"
            ),
            "Final State": recognition["final_state"]
        })

    return results

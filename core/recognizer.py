
class DFARecognizer:
    """
    Recognizes strings using a DFA and records
    every transition made during recognition.
    """

    def __init__(self, dfa):
        self.dfa = dfa

    def recognize(self, input_string):
        """
        Process an input string using the DFA.

        Returns:
            accepted: Whether the string is accepted.
            trace: List of transitions.
            final_state: State reached after processing.
            message: Explanation of the result.
        """

        current_state = self.dfa.start_state
        trace = []

        for position, symbol in enumerate(input_string):

            # Reject symbols outside the DFA alphabet.
            if symbol not in self.dfa.alphabet:

                trace.append({
                    "position": position,
                    "from_state": current_state,
                    "symbol": symbol,
                    "to_state": None,
                    "status": "invalid_symbol"
                })

                return {
                    "accepted": False,
                    "trace": trace,
                    "final_state": current_state,
                    "message": (
                        f"Rejected: '{symbol}' is not in the "
                        "automaton's alphabet."
                    )
                }

            next_state = self.dfa.get_transition(
                current_state,
                symbol
            )

            # Handle a missing transition safely.
            if next_state is None:

                trace.append({
                    "position": position,
                    "from_state": current_state,
                    "symbol": symbol,
                    "to_state": None,
                    "status": "missing_transition"
                })

                return {
                    "accepted": False,
                    "trace": trace,
                    "final_state": current_state,
                    "message": "Rejected: no valid transition exists."
                }

            trace.append({
                "position": position,
                "from_state": current_state,
                "symbol": symbol,
                "to_state": next_state,
                "status": "success"
            })

            current_state = next_state

        # Check whether the final state is accepting.
        accepted = current_state in self.dfa.accept_states

        if accepted:
            message = "Accepted: the string ends in an accepting state."
        else:
            message = "Rejected: the string ends in a non-accepting state."

        return {
            "accepted": accepted,
            "trace": trace,
            "final_state": current_state,
            "message": message
        }

    def display_trace(self, result):
        """Print a readable transition-by-transition trace."""

        print("\n========== RECOGNITION TRACE ==========")

        print("Result:", result["message"])

        print("\nTransitions:")

        if not result["trace"]:
            print("No transitions required (empty string).")

        for step in result["trace"]:

            if step["status"] == "success":
                print(
                    f"Position {step['position']}: "
                    f"D{step['from_state']} "
                    f"--{step['symbol']}--> "
                    f"D{step['to_state']}"
                )

            else:
                print(
                    f"Position {step['position']}: "
                    f"Invalid transition on "
                    f"'{step['symbol']}'"
                )

        print("\nFinal state:", result["final_state"])
        print("Accepted:", result["accepted"])

        print("=======================================\n")


def recognize_string(dfa, input_string):
    """Convenience function for recognizing a string."""

    recognizer = DFARecognizer(dfa)

    return recognizer.recognize(input_string)

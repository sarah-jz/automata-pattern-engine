
from collections import deque


class DFAEquivalenceChecker:
    """
    Checks whether two DFAs recognize the same language.

    Uses BFS on the product automaton and returns a
    shortest counterexample if the languages differ.
    """

    def __init__(self, dfa1, dfa2):
        self.dfa1 = dfa1
        self.dfa2 = dfa2

        # Both automata must be considered over the same alphabet.
        self.alphabet = sorted(
            dfa1.alphabet | dfa2.alphabet
        )

    def transition(self, dfa, state, symbol):
        """
        Get a transition safely.

        None represents an implicit dead state.
        """

        if state is None:
            return None

        if symbol not in dfa.alphabet:
            return None

        return dfa.get_transition(state, symbol)

    def is_accepting(self, dfa, state):
        """Check whether a state is accepting."""

        return (
            state is not None
            and state in dfa.accept_states
        )

    def check(self):
        """
        Compare the languages of two DFAs.

        Returns:
            equivalent: True if languages are equal.
            counterexample: Shortest distinguishing string,
                            or None if equivalent.
        """

        start_pair = (
            self.dfa1.start_state,
            self.dfa2.start_state
        )

        queue = deque([
            (start_pair, "")
        ])

        visited = {start_pair}

        while queue:

            (state1, state2), word = queue.popleft()

            accepting1 = self.is_accepting(
                self.dfa1,
                state1
            )

            accepting2 = self.is_accepting(
                self.dfa2,
                state2
            )

            # If only one DFA accepts this word,
            # the languages are different.
            if accepting1 != accepting2:

                return {
                    "equivalent": False,
                    "counterexample": word,
                    "message": (
                        "The automata recognize different languages."
                    )
                }

            # Explore transitions in alphabetical order.
            for symbol in self.alphabet:

                next_state1 = self.transition(
                    self.dfa1,
                    state1,
                    symbol
                )

                next_state2 = self.transition(
                    self.dfa2,
                    state2,
                    symbol
                )

                next_pair = (
                    next_state1,
                    next_state2
                )

                if next_pair not in visited:

                    visited.add(next_pair)

                    queue.append((
                        next_pair,
                        word + symbol
                    ))

        return {
            "equivalent": True,
            "counterexample": None,
            "message": (
                "The automata recognize the same language."
            )
        }


def check_equivalence(dfa1, dfa2):
    """Convenience function for comparing two DFAs."""

    checker = DFAEquivalenceChecker(dfa1, dfa2)

    return checker.check()

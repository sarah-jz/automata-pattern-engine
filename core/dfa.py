
from collections import deque


class DFA:
    """
    Represents a Deterministic Finite Automaton.
    """

    def __init__(
        self,
        states,
        alphabet,
        start_state,
        accept_states,
        transitions,
        state_subsets=None
    ):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

        # Maps DFA state IDs to their corresponding NFA state subsets.
        self.state_subsets = state_subsets or {}

    def get_transition(self, state, symbol):
        """Return the destination state for a given input."""

        return self.transitions.get((state, symbol))

    def display(self):
        """Display the DFA and its transitions."""

        print("\n========== DFA ==========")

        print("States:", sorted(self.states))
        print("Alphabet:", sorted(self.alphabet))
        print("Start state:", self.start_state)
        print("Accept states:", sorted(self.accept_states))

        print("\nState subsets:")

        for state in sorted(self.state_subsets):
            subset = sorted(self.state_subsets[state])
            print(f"D{state} = {subset}")

        print("\nTransitions:")

        for (source, symbol), destination in sorted(
            self.transitions.items(),
            key=lambda item: (item[0][0], item[0][1])
        ):
            print(f"D{source} --{symbol}--> D{destination}")

        print("=========================\n")


class SubsetConstruction:
    """
    Converts an epsilon-NFA into an equivalent DFA
    using subset construction.
    """

    EPSILON = "ε"

    def __init__(self, nfa):
        self.nfa = nfa

    def epsilon_closure(self, states):
        """
        Find all states reachable through epsilon transitions.

        The original states are always included.
        """

        closure = set(states)

        stack = list(states)

        while stack:

            current_state = stack.pop()

            epsilon_destinations = self.nfa.get_transitions(
                current_state,
                self.EPSILON
            )

            for destination in epsilon_destinations:

                if destination not in closure:
                    closure.add(destination)
                    stack.append(destination)

        return frozenset(closure)

    def move(self, states, symbol):
        """
        Find all states reachable from a set of states
        using a particular input symbol.
        """

        result = set()

        for state in states:

            destinations = self.nfa.get_transitions(
                state,
                symbol
            )

            result.update(destinations)

        return result

    def convert(self):
        """Perform subset construction."""

        start_subset = self.epsilon_closure(
            {self.nfa.start_state}
        )

        # Each distinct NFA subset becomes one DFA state.
        subset_to_id = {
            start_subset: 0
        }

        id_to_subset = {
            0: start_subset
        }

        queue = deque([start_subset])

        transitions = {}
        accept_states = set()

        while queue:

            current_subset = queue.popleft()

            current_id = subset_to_id[current_subset]

            # A DFA state is accepting if its subset
            # contains the NFA's accepting state.
            if self.nfa.accept_state in current_subset:
                accept_states.add(current_id)

            for symbol in sorted(self.nfa.alphabet):

                moved_states = self.move(
                    current_subset,
                    symbol
                )

                next_subset = self.epsilon_closure(
                    moved_states
                )

                # Create a new DFA state if necessary.
                if next_subset not in subset_to_id:

                    new_id = len(subset_to_id)

                    subset_to_id[next_subset] = new_id
                    id_to_subset[new_id] = next_subset

                    queue.append(next_subset)

                destination_id = subset_to_id[next_subset]

                transitions[(current_id, symbol)] = destination_id

        return DFA(
            states=set(id_to_subset.keys()),
            alphabet=set(self.nfa.alphabet),
            start_state=0,
            accept_states=accept_states,
            transitions=transitions,
            state_subsets=id_to_subset
        )


def convert_nfa_to_dfa(nfa):
    """Convenience function for NFA-to-DFA conversion."""

    converter = SubsetConstruction(nfa)

    return converter.convert()


class NFA:
    """
    Represents a Non-deterministic Finite Automaton
    with epsilon transitions.
    """

    def __init__(self, states, alphabet, start_state, accept_state, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_state = accept_state
        self.transitions = transitions

    def add_transition(self, source, symbol, destination):
        """Add a transition to the automaton."""

        key = (source, symbol)

        if key not in self.transitions:
            self.transitions[key] = set()

        self.transitions[key].add(destination)

    def get_transitions(self, state, symbol):
        """Return all destinations for a state and symbol."""

        return self.transitions.get((state, symbol), set())

    def display(self):
        """Print the automaton's states and transitions."""

        print("\n========== NFA ==========")

        print("States:", sorted(self.states))
        print("Alphabet:", sorted(self.alphabet))
        print("Start state:", self.start_state)
        print("Accept state:", self.accept_state)

        print("\nTransitions:")

        for (source, symbol), destinations in sorted(
            self.transitions.items(),
            key=lambda item: (item[0][0], item[0][1])
        ):
            for destination in sorted(destinations):
                print(f"q{source} --{symbol}--> q{destination}")

        print("=========================\n")


class ThompsonConstructor:
    """
    Constructs an epsilon-NFA from postfix regular expression.
    """

    EPSILON = "ε"

    def __init__(self):
        self.state_count = 0
        self.states = set()
        self.alphabet = set()
        self.transitions = {}

    def new_state(self):
        """Create a new state with a unique ID."""

        state = self.state_count
        self.state_count += 1

        self.states.add(state)

        return state

    def add_transition(self, source, symbol, destination):
        """Add a transition between two states."""

        key = (source, symbol)

        if key not in self.transitions:
            self.transitions[key] = set()

        self.transitions[key].add(destination)

    def construct(self, postfix):
        """
        Build an NFA using Thompson's construction.

        Each stack item contains:
            (start_state, accept_state)
        """

        stack = []

        for token in postfix:

            # CASE 1: Literal symbol
            if token not in {"|", ".", "*"}:

                if token == self.EPSILON:
                    raise ValueError(
                        "The epsilon symbol is reserved."
                    )

                start = self.new_state()
                accept = self.new_state()

                self.alphabet.add(token)

                self.add_transition(
                    start,
                    token,
                    accept
                )

                stack.append((start, accept))

            # CASE 2: Concatenation
            elif token == ".":

                if len(stack) < 2:
                    raise ValueError(
                        "Invalid concatenation expression."
                    )

                second = stack.pop()
                first = stack.pop()

                first_start, first_accept = first
                second_start, second_accept = second

                self.add_transition(
                    first_accept,
                    self.EPSILON,
                    second_start
                )

                stack.append(
                    (first_start, second_accept)
                )

            # CASE 3: Union
            elif token == "|":

                if len(stack) < 2:
                    raise ValueError(
                        "Invalid union expression."
                    )

                second = stack.pop()
                first = stack.pop()

                first_start, first_accept = first
                second_start, second_accept = second

                start = self.new_state()
                accept = self.new_state()

                self.add_transition(
                    start,
                    self.EPSILON,
                    first_start
                )

                self.add_transition(
                    start,
                    self.EPSILON,
                    second_start
                )

                self.add_transition(
                    first_accept,
                    self.EPSILON,
                    accept
                )

                self.add_transition(
                    second_accept,
                    self.EPSILON,
                    accept
                )

                stack.append((start, accept))

            # CASE 4: Kleene star
            elif token == "*":

                if len(stack) < 1:
                    raise ValueError(
                        "Invalid Kleene star expression."
                    )

                fragment = stack.pop()

                fragment_start, fragment_accept = fragment

                start = self.new_state()
                accept = self.new_state()

                # Zero occurrences
                self.add_transition(
                    start,
                    self.EPSILON,
                    accept
                )

                # Enter the original automaton
                self.add_transition(
                    start,
                    self.EPSILON,
                    fragment_start
                )

                # Repeat the automaton
                self.add_transition(
                    fragment_accept,
                    self.EPSILON,
                    fragment_start
                )

                # Exit the automaton
                self.add_transition(
                    fragment_accept,
                    self.EPSILON,
                    accept
                )

                stack.append((start, accept))

        if len(stack) != 1:
            raise ValueError(
                "Invalid postfix expression."
            )

        start_state, accept_state = stack.pop()

        return NFA(
            states=self.states,
            alphabet=self.alphabet,
            start_state=start_state,
            accept_state=accept_state,
            transitions=self.transitions
        )


def build_nfa(postfix):
    """Convenience function for constructing an NFA."""

    constructor = ThompsonConstructor()

    return constructor.construct(postfix)

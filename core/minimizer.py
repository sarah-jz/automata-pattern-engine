
from core.dfa import DFA


def minimize_dfa(dfa):
    """
    Minimize a complete DFA using partition refinement.

    Returns a new DFA with equivalent states merged.
    """

    states = set(dfa.states)
    alphabet = set(dfa.alphabet)

    # Step 1: Separate accepting and non-accepting states.
    accepting = set(dfa.accept_states)
    non_accepting = states - accepting

    partitions = []

    if accepting:
        partitions.append(accepting)

    if non_accepting:
        partitions.append(non_accepting)

    # Step 2: Refine partitions until no more splitting is possible.
    changed = True

    while changed:

        changed = False
        new_partitions = []

        for group in partitions:

            groups_by_signature = {}

            for state in group:

                # Determine which partition each transition reaches.
                signature = []

                for symbol in sorted(alphabet):

                    destination = dfa.get_transition(
                        state,
                        symbol
                    )

                    destination_group = next(
                        (
                            i
                            for i, partition in enumerate(partitions)
                            if destination in partition
                        ),
                        None
                    )

                    signature.append(destination_group)

                signature = tuple(signature)

                if signature not in groups_by_signature:
                    groups_by_signature[signature] = set()

                groups_by_signature[signature].add(state)

            # A partition has been split.
            new_groups = list(groups_by_signature.values())

            if len(new_groups) > 1:
                changed = True

            new_partitions.extend(new_groups)

        partitions = new_partitions

    # Step 3: Assign a new ID to every partition.
    state_to_group = {}

    for group_id, group in enumerate(partitions):

        for state in group:
            state_to_group[state] = group_id

    # Step 4: Build minimized transitions.
    minimized_transitions = {}

    for group_id, group in enumerate(partitions):

        representative = next(iter(group))

        for symbol in sorted(alphabet):

            destination = dfa.get_transition(
                representative,
                symbol
            )

            destination_group = state_to_group[destination]

            minimized_transitions[
                (group_id, symbol)
            ] = destination_group

    # Step 5: Identify minimized accepting states.
    minimized_accepting = set()

    for group_id, group in enumerate(partitions):

        if group & accepting:
            minimized_accepting.add(group_id)

    minimized_start = state_to_group[dfa.start_state]

    # Preserve the original DFA state groups for explanation.
    minimized_subsets = {
        group_id: set(group)
        for group_id, group in enumerate(partitions)
    }

    return DFA(
        states=set(range(len(partitions))),
        alphabet=alphabet,
        start_state=minimized_start,
        accept_states=minimized_accepting,
        transitions=minimized_transitions,
        state_subsets=minimized_subsets
    )

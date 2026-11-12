
from graphviz import Digraph


def create_nfa_graph(nfa):
    """
    Generate a Graphviz diagram for an epsilon-NFA.
    """

    graph = Digraph("NFA", format="svg")

    graph.attr(
        rankdir="LR",
        label="Epsilon-NFA",
        labelloc="t",
        fontsize="18"
    )

    graph.attr("node", shape="circle")

    # Invisible starting point.
    graph.node("start", shape="point")

    # Add NFA states.
    for state in sorted(nfa.states):

        if state == nfa.accept_state:
            graph.node(
                str(state),
                label=f"q{state}",
                shape="doublecircle"
            )
        else:
            graph.node(
                str(state),
                label=f"q{state}"
            )

    # Add start arrow.
    graph.edge("start", str(nfa.start_state))

    # Group labels for transitions with the same source and destination.
    grouped_edges = {}

    for (source, symbol), destinations in nfa.transitions.items():

        for destination in destinations:

            key = (source, destination)

            if key not in grouped_edges:
                grouped_edges[key] = []

            grouped_edges[key].append(symbol)

    for (source, destination), symbols in grouped_edges.items():

        label = ", ".join(sorted(symbols))

        graph.edge(
            str(source),
            str(destination),
            label=label
        )

    return graph


def create_dfa_graph(dfa):
    """
    Generate a Graphviz diagram for a DFA.
    """

    graph = Digraph("DFA", format="svg")

    graph.attr(
        rankdir="LR",
        label="Deterministic Finite Automaton",
        labelloc="t",
        fontsize="18"
    )

    graph.attr("node", shape="circle")

    graph.node("start", shape="point")

    # Add DFA states.
    for state in sorted(dfa.states):

        if state in dfa.accept_states:
            graph.node(
                str(state),
                label=f"D{state}",
                shape="doublecircle"
            )
        else:
            graph.node(
                str(state),
                label=f"D{state}"
            )

    # Add start arrow.
    graph.edge("start", str(dfa.start_state))

    # Add transitions.
    for (source, symbol), destination in sorted(
        dfa.transitions.items(),
        key=lambda item: (item[0][0], item[0][1])
    ):

        graph.edge(
            str(source),
            str(destination),
            label=symbol
        )

    return graph

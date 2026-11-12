
import streamlit as st

from core.regex_parser import RegexParser
from core.nfa import build_nfa
from core.dfa import convert_nfa_to_dfa
from core.minimizer import minimize_dfa
from core.recognizer import DFARecognizer
from core.equivalence import check_equivalence

from visualization.automata_graph import (
    create_nfa_graph,
    create_dfa_graph
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Automata Pattern Recognition Engine",
    page_icon="⚙️",
    layout="wide"
)


# --------------------------------------------------
# AUTOMATA CONSTRUCTION PIPELINE
# --------------------------------------------------

def build_automata(expression):
    if not expression or not expression.strip():
        raise ValueError(
            "Please enter a regular expression."
        )
    parser = RegexParser(expression)

    postfix = parser.to_postfix()

    nfa = build_nfa(postfix)

    dfa = convert_nfa_to_dfa(nfa)

    minimized_dfa = minimize_dfa(dfa)

    return {
        "postfix": postfix,
        "nfa": nfa,
        "dfa": dfa,
        "minimized_dfa": minimized_dfa
    }


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("Automata Pattern Recognition Engine")

st.markdown(
    """
    ### Explore the relationship between regular expressions
    and finite automata.

    Construct, visualize, minimize and test automata
    using fundamental algorithms from Automata Theory.
    """
)

st.caption(
    "Python | Streamlit | Graphviz | Finite Automata"
)

st.divider()


# --------------------------------------------------
# SIDEBAR - REGULAR EXPRESSION INPUT
# --------------------------------------------------

st.sidebar.title("Pattern Builder")

st.sidebar.markdown(
    """
    Build finite automata from regular expressions.

    **Supported operators**

    - `|` Union
    - `*` Kleene star
    - `()` Grouping
    - Implicit concatenation
    """
)

st.sidebar.divider()

expression = st.sidebar.text_input(
    "Enter a regular expression",
    value="(a|b)*abb",
    help="Supported operators: |, *, parentheses and implicit concatenation."
)

generate_button = st.sidebar.button(
    "Generate Automata",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# BUILD AUTOMATA
# --------------------------------------------------

if generate_button:

    try:

        result = build_automata(expression)

        st.session_state["automata_result"] = result
        st.session_state["expression"] = expression
        st.session_state.pop("build_error", None)

    except Exception as error:

        st.session_state.pop("automata_result", None)
        st.session_state["build_error"] = str(error)


if "build_error" in st.session_state:

    st.error(
        f"Unable to process the expression: "
        f"{st.session_state['build_error']}"
    )


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

if "automata_result" in st.session_state:

    result = st.session_state["automata_result"]

    nfa = result["nfa"]
    dfa = result["dfa"]
    minimized_dfa = result["minimized_dfa"]

    current_expression = st.session_state["expression"]

    st.subheader("Pattern Analysis")

    st.code(current_expression, language="text")

    st.write("**Postfix expression:**")

    st.code(" ".join(result["postfix"]))

    # ----------------------------------------------
    # AUTOMATA STATISTICS
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "NFA States",
        len(nfa.states)
    )

    col2.metric(
        "DFA States",
        len(dfa.states)
    )

    col3.metric(
        "Minimized DFA States",
        len(minimized_dfa.states)
    )

    st.divider()

    # ----------------------------------------------
    # APPLICATION TABS
    # ----------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "Automata Visualizer",
        "String Tester",
        "Equivalence Checker",
        "Batch Testing"
    ])

    # ==============================================
    # TAB 1 - AUTOMATA VISUALIZER
    # ==============================================

    with tab1:

        st.header("Automata Visualization")

        st.write(
            "Explore the automata generated from your "
            "regular expression."
        )

        nfa_tab, dfa_tab, minimized_tab = st.tabs([
            "ε-NFA",
            "DFA",
            "Minimized DFA"
        ])

        with nfa_tab:

            st.subheader("Epsilon-NFA")

            st.write(
                f"Total states: {len(nfa.states)}"
            )

            nfa_graph = create_nfa_graph(nfa)

            st.graphviz_chart(nfa_graph.source)

        with dfa_tab:

            st.subheader("Deterministic Finite Automaton")

            st.write(
                f"Total states: {len(dfa.states)}"
            )

            dfa_graph = create_dfa_graph(dfa)

            st.graphviz_chart(dfa_graph.source)

        with minimized_tab:

            st.subheader("Minimized DFA")

            st.write(
                f"Total states: {len(minimized_dfa.states)}"
            )

            minimized_graph = create_dfa_graph(
                minimized_dfa
            )

            st.graphviz_chart(minimized_graph.source)

    # ==============================================
    # TAB 2 - STRING TESTER
    # ==============================================

    with tab2:

        st.header("String Recognition")

        st.write(
            "Enter a string to check whether it belongs "
            "to the language represented by the expression."
        )

        input_string = st.text_input(
            "Input string",
            key="recognition_input"
        )

        if st.button("Test String"):

            recognizer = DFARecognizer(minimized_dfa)

            recognition_result = recognizer.recognize(
                input_string
            )

            if recognition_result["accepted"]:

                st.success("STRING ACCEPTED")

            else:

                st.error("STRING REJECTED")

            st.write(recognition_result["message"])

            st.subheader("Transition Trace")

            if recognition_result["trace"]:

                st.dataframe(
                    recognition_result["trace"],
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "The input is empty. No transitions were required."
                )

            st.write(
                "**Final state:**",
                recognition_result["final_state"]
            )

    # ==============================================
    # TAB 3 - EQUIVALENCE CHECKER
    # ==============================================

    with tab3:

        st.header("Automata Equivalence Checker")

        st.write(
            "Compare the current regular expression with "
            "another expression."
        )

        second_expression = st.text_input(
            "Second regular expression",
            placeholder="For example: (b|a)*abb"
        )

        if st.button("Compare Automata"):

            if not second_expression.strip():

                st.warning(
                    "Please enter a second regular expression."
                )

            else:

                try:

                    second_result = build_automata(
                        second_expression
                    )

                    comparison = check_equivalence(
                        minimized_dfa,
                        second_result["minimized_dfa"]
                    )

                    if comparison["equivalent"]:

                        st.success(
                            "The two expressions are equivalent."
                        )

                    else:

                        st.error(
                            "The two expressions are not equivalent."
                        )

                        st.write(
                            "**Shortest counterexample:**"
                        )

                        st.code(
                            repr(comparison["counterexample"])
                        )

                    st.write(comparison["message"])

                except Exception as error:

                    st.error(
                        f"Could not compare expressions: {error}"
                    )

    # ==============================================
    # TAB 4 - BATCH TESTING
    # ==============================================

    with tab4:

        st.header("Batch String Testing")

        st.write(
            "Enter multiple strings, one per line, "
            "to test them together."
        )

        batch_input = st.text_area(
            "Enter strings",
            placeholder="abb\naabb\nbabb\naba\nab"
        )

        if st.button("Run Batch Test"):

            if not batch_input.strip():

                st.warning(
                    "Please enter at least one string."
                )

            else:

                recognizer = DFARecognizer(
                    minimized_dfa
                )

                strings = batch_input.splitlines()

                results = []

                for string in strings:

                    recognition = recognizer.recognize(
                        string
                    )

                    results.append({
                        "Input String": repr(string),
                        "Result": (
                            "Accepted"
                            if recognition["accepted"]
                            else "Rejected"
                        ),
                        "Final State": recognition["final_state"]
                    })

                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

                accepted_count = sum(
                    row["Result"] == "Accepted"
                    for row in results
                )

                rejected_count = len(results) - accepted_count

                col1, col2 = st.columns(2)

                col1.metric(
                    "Accepted Strings",
                    accepted_count
                )

                col2.metric(
                    "Rejected Strings",
                    rejected_count
                )


# --------------------------------------------------
# INITIAL SCREEN
# --------------------------------------------------

else:

    st.info(
        "Enter a regular expression in the sidebar "
        "and click Generate Automata to get started."
    )

    st.subheader("Supported Regular Expression Syntax")

    st.markdown(
        """
        | Symbol | Meaning | Example |
        |---|---|---|
        | `a`, `b` | Literal symbols | `ab` |
        | `|` | Union | `a|b` |
        | `*` | Kleene star | `a*` |
        | `()` | Grouping | `(a|b)*` |
        | Implicit concatenation | Sequence | `abb` |
        """
    )

    st.caption(
        "The current implementation supports single-character "
        "literals, union, Kleene star, grouping and implicit "
        "concatenation."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Automata Pattern Recognition Engine | "
    "Built using Python, Streamlit and Graphviz"
)

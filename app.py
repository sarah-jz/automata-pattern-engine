from ui.styles import load_css
import streamlit as st

from services.automata_service import build_automata
from core.recognizer import DFARecognizer

from services.equivalence_service import compare_expressions

from visualization.automata_graph import (
    create_nfa_graph,
    create_dfa_graph
)

from services.recognition_service import (
    recognize_string,
    recognize_batch
)

from ui.components import (
    automata_metrics,
    section_header,
    recognition_message,
    batch_metrics,
    app_header,
    pattern_builder,
    automata_visualization
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Automata Pattern Recognition Engine",
    page_icon="⚙️",
    layout="wide"
)
load_css()

# --------------------------------------------------
# AUTOMATA CONSTRUCTION PIPELINE
# --------------------------------------------------



# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
app_header()
st.divider()


# --------------------------------------------------
# SIDEBAR - REGULAR EXPRESSION INPUT
# --------------------------------------------------

expression, generate_button = pattern_builder()

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

    automata_metrics(nfa, dfa, minimized_dfa)
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

        section_header(
            "Automata Visualization",
            "Explore the automata generated from your regular expression."
        )

        nfa_tab, dfa_tab, minimized_tab = st.tabs([
            "ε-NFA",
            "DFA",
            "Minimized DFA"
        ])

        with nfa_tab:

            nfa_graph = create_nfa_graph(nfa)

            automata_visualization(
                "Epsilon-NFA",
                "Non-deterministic finite automaton generated using Thompson's Construction.",
                nfa_graph,
                len(nfa.states)
            )


        with dfa_tab:

            dfa_graph = create_dfa_graph(dfa)

            automata_visualization(
                "Deterministic Finite Automaton",
                "Deterministic automaton generated using subset construction.",
                dfa_graph,
                len(dfa.states)
            )
        
        with minimized_tab:

            minimized_graph = create_dfa_graph(minimized_dfa)

            automata_visualization(
                "Minimized DFA",
                "Equivalent deterministic automaton with redundant states removed.",
                minimized_graph,
                len(minimized_dfa.states)
            )
            
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

            recognition_result = recognize_string(
                minimized_dfa,
                input_string
            )

            recognition_message(recognition_result)

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

                    result_data = compare_expressions(
                        minimized_dfa,
                        second_expression
                    )

                    comparison = result_data["comparison"]

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

                results = recognize_batch(
                    minimized_dfa,
                    strings
                )

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

                batch_metrics(results)
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


import streamlit as st


def section_header(title, description=None):
    """Display a consistent section heading."""

    st.header(title)

    if description:
        st.caption(description)


def automata_metrics(nfa, dfa, minimized_dfa):
    """Display automata state counts."""

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


def recognition_message(result):
    """Display a string recognition result."""

    if result["accepted"]:
        st.success("STRING ACCEPTED")
    else:
        st.error("STRING REJECTED")

    st.write(result["message"])


def batch_metrics(results):
    """Display accepted and rejected string counts."""

    accepted = sum(
        row["Result"] == "Accepted"
        for row in results
    )

    rejected = len(results) - accepted

    col1, col2 = st.columns(2)

    col1.metric("Accepted Strings", accepted)
    col2.metric("Rejected Strings", rejected)

def app_header():
    """Display the main application header."""

    st.markdown(
        """
        <div class="hero-header">
            <div class="hero-accent"></div>
            <div class="hero-eyebrow">COMPUTATIONAL AUTOMATA TOOLKIT</div>
            <div class="hero-title">
                Automata Pattern Recognition Engine
            </div>
            <div class="hero-description">
                Transform regular expressions into finite automata.
                Explore state transitions, minimize automata,
                and analyse language equivalence.
            </div>
            <div class="hero-meta">
                PYTHON &nbsp; • &nbsp; FINITE AUTOMATA
                &nbsp; • &nbsp; REGULAR EXPRESSIONS
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def pattern_builder():
    """Render the regular expression input panel."""

    st.sidebar.markdown(
        """
        <div class="sidebar-heading">
            <div class="sidebar-eyebrow">WORKSPACE</div>
            <div class="sidebar-title">Pattern Builder</div>
            <div class="sidebar-description">
                Configure your regular expression and generate
                its corresponding finite automata.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
        <div class="syntax-card">
            <div class="syntax-title">SUPPORTED OPERATORS</div>
            <div class="syntax-row">
                <code>|</code>
                <span>Union</span>
            </div>
            <div class="syntax-row">
                <code>*</code>
                <span>Kleene star</span>
            </div>
            <div class="syntax-row">
                <code>()</code>
                <span>Grouping</span>
            </div>
            <div class="syntax-row">
                <code>ab</code>
                <span>Concatenation</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    expression = st.sidebar.text_input(
        "Regular expression",
        value="(a|b)*abb",
        help="Supported operators: |, *, parentheses and implicit concatenation.",
        key="pattern_expression"
    )

    generate_button = st.sidebar.button(
        "Generate Automata",
        type="primary",
        use_container_width=True
    )

    return expression, generate_button


def automata_visualization(title, description, graph, state_count):
    """Display an automaton inside a styled visualization panel."""

    st.markdown(
        f"""
        <div class="visualization-heading">
            <div class="visualization-title">{title}</div>
            <div class="visualization-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric("Total States", state_count)

    with st.container(border=True):
        st.graphviz_chart(
            graph.source,
            use_container_width=True
        )

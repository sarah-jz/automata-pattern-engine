# Automata Pattern Recognition Engine

An interactive application that converts regular expressions into finite automata, visualizes their structures, recognizes input strings, minimizes deterministic automata, and checks language equivalence.

Built using Python, Streamlit and Graphviz, with the core automata algorithms implemented from scratch.

## Overview

The Automata Pattern Recognition Engine demonstrates fundamental concepts from Automata Theory through a working software application.

Users can enter a regular expression and automatically generate:

- An ε-Non-deterministic Finite Automaton (ε-NFA)
- An equivalent Deterministic Finite Automaton (DFA)
- A minimized DFA

The application also supports string recognition, transition tracing, automata equivalence checking and batch testing.

## Features

### 1. Regular Expression Processing
- Converts infix regular expressions into postfix notation.
- Automatically inserts explicit concatenation operators.
- Validates malformed expressions.

### 2. ε-NFA Construction
- Implements Thompson's construction.
- Supports epsilon transitions.
- Builds an NFA from a postfix regular expression.

### 3. NFA-to-DFA Conversion
- Implements subset construction.
- Calculates epsilon closures.
- Uses reachable state subsets to construct DFA states.

### 4. DFA Minimization
- Implements partition refinement.
- Identifies equivalent states.
- Produces a smaller equivalent DFA.

### 5. String Recognition
- Determines whether an input string belongs to the language.
- Records state transitions.
- Explains acceptance and rejection.

### 6. Automata Equivalence Checking
- Compares two DFAs using a product-automaton BFS.
- Determines whether their recognized languages are equivalent.
- Produces a shortest counterexample when they differ.

### 7. Automata Visualization
- Generates Graphviz diagrams.
- Displays start and accepting states.
- Visualizes NFA, DFA and minimized DFA transitions.

### 8. Batch Testing
- Tests multiple input strings.
- Displays acceptance results.
- Summarizes accepted and rejected strings.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| Streamlit | Interactive web application |
| Graphviz | Automata visualization |
| Pytest | Automated testing |

## Project Architecture

```text
automata-pattern-engine/
│
├── app.py
├── requirements.txt
├── packages.txt
├── README.md
├── .gitignore
│
├── core/
│   ├── regex_parser.py
│   ├── nfa.py
│   ├── dfa.py
│   ├── minimizer.py
│   ├── recognizer.py
│   └── equivalence.py
│
├── visualization/
│   └── automata_graph.py
│
└── tests/
    ├── test_regex.py
    ├── test_nfa.py
    ├── test_dfa.py
    ├── test_minimizer.py
    ├── test_recognizer.py
    ├── test_equivalence.py
    ├── test_visualization.py
    └── test_integration.py
```

## Supported Regular Expression Syntax

| Syntax | Meaning | Example |
|---|---|---|
| `a`, `b` | Single-character literals | `ab` |
| `\|` | Union | `a\|b` |
| `*` | Kleene star | `a*` |
| `()` | Grouping | `(a\|b)*` |
| Implicit concatenation | Sequence of symbols | `abb` |

**Current limitations:** The implementation supports single-character literals, union, Kleene star, parentheses and implicit concatenation. Operators such as `+`, `?`, character classes, escape sequences and explicit epsilon expressions are not currently supported.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Graphviz system application

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd automata-pattern-engine
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Graphviz

Install the Graphviz system application from:

https://graphviz.org/download/

Make sure its `bin` directory is available in your system PATH.

### 5. Run the application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

## Running the Tests

Run the complete automated test suite:

```bash
python -m pytest -v
```

The project currently contains **54 passing automated tests** covering:

- Regular expression parsing
- Thompson's construction
- Subset construction
- DFA minimization
- String recognition
- Automata equivalence
- Graphviz visualization
- End-to-end integration

## Example

Consider the regular expression:

```text
(a|b)*abb
```

It represents all strings over `{a, b}` that end with `abb`.

Example recognition results:

| Input | Result |
|---|---|
| `abb` | Accepted |
| `aabb` | Accepted |
| `babb` | Accepted |
| `aba` | Rejected |
| `ab` | Rejected |
| `abba` | Rejected |

The construction pipeline produces:

| Automaton | Number of states |
|---|---:|
| ε-NFA | 14 |
| DFA | 5 |
| Minimized DFA | 4 |

## Academic Concepts Demonstrated

This project applies the following theoretical concepts:

- Regular languages and regular expressions
- Finite automata
- Nondeterministic finite automata
- Epsilon transitions and epsilon closure
- Thompson's construction
- Subset construction
- DFA minimization and state equivalence
- Language recognition
- Product automata
- Equivalence of regular languages
- Breadth-first search and counterexample generation

## Future Improvements

Potential extensions include:

- Support for additional regular expression operators.
- Exporting automata diagrams in additional formats.
- Interactive step-by-step animation of automata execution.
- More advanced automata comparison tools.
- Expanded pattern testing and analysis.

## Author

Developed as an individual academic project exploring the practical implementation of concepts from Automata Theory.
# Automata Pattern Recognition Engine

An interactive web application that transforms regular expressions into finite automata, visualizes their structures, recognizes input strings, minimizes deterministic automata, and checks language equivalence.

<p align="center">
  <a href="https://automata-pattern-engine.streamlit.app/">
    <strong>Live Application</strong>
  </a>
  |
  <a href="https://github.com/sarah-jz/automata-pattern-engine">
    <strong>GitHub Repository</strong>
  </a>
</p>

---

## Overview

The **Automata Pattern Recognition Engine** is an individual software project developed to demonstrate the practical implementation of fundamental concepts from Automata Theory.

Users can enter regular expressions and automatically generate their equivalent:

- Epsilon-Nondeterministic Finite Automaton (ε-NFA)
- Deterministic Finite Automaton (DFA)
- Minimized DFA

The application combines theoretical automata algorithms with an interactive web interface, allowing users to explore state transitions, test strings, compare regular expressions, and visualize automata.

The core algorithms are implemented from scratch without relying on external automata-processing libraries.

---

## Application Screenshots

### 1. Application Overview

The main interface allows users to enter regular expressions and generate the corresponding automata.

![Application Overview](screenshots/home.png)

### 2. Epsilon-NFA Visualization

Visual representation of the ε-NFA generated using Thompson's Construction.

![Epsilon NFA](screenshots/nfa.png)

### 3. Minimized DFA Visualization

The minimized deterministic finite automaton generated using partition refinement.

![Minimized DFA](screenshots/minimized-dfa.png)
### 4.DFA Equivalence Checker

Compares two regular expressions by checking whether their corresponding finite automata recognize the same language. If they are not equivalent, the application provides a counterexample string.

![DFA Equivalence Checker](screenshots/equivalence-checker.png)

### 5. String Recognition

Tests input strings against the generated automaton and displays the transition trace.

![String Recognition](screenshots/string-testing.png)

### 6. Batch String Testing

Tests multiple strings simultaneously and summarizes accepted and rejected inputs.

![Batch Testing](screenshots/batch-testing.png)

---

## Key Features

### 1. Regular Expression Processing
- Converts infix regular expressions into postfix notation.
- Automatically inserts explicit concatenation operators.
- Validates malformed expressions.

### 2. ε-NFA Construction
- Implements Thompson's Construction.
- Generates epsilon transitions.
- Constructs an NFA from a postfix regular expression.

### 3. NFA-to-DFA Conversion
- Implements the Subset Construction algorithm.
- Calculates epsilon closures.
- Generates reachable DFA states from NFA state subsets.

### 4. DFA Minimization
- Implements partition refinement.
- Identifies equivalent states.
- Produces a minimal equivalent DFA.

### 5. String Recognition
- Determines whether an input string belongs to a regular language.
- Records state-by-state transitions.
- Explains acceptance and rejection.

### 6. Automata Equivalence Checking
- Compares two automata using product-automaton traversal.
- Determines whether two regular expressions represent the same language.
- Generates a shortest counterexample when the languages differ.

### 7. Automata Visualization
- Generates automata diagrams using Graphviz.
- Displays start states, accepting states, and transitions.
- Visualizes ε-NFAs, DFAs, and minimized DFAs.

### 8. Batch String Testing
- Tests multiple strings simultaneously.
- Displays individual recognition results.
- Summarizes accepted and rejected inputs.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core algorithms and application logic |
| Streamlit | Interactive web interface |
| Graphviz | Automata visualization |
| Pytest | Automated testing |
| Git and GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Application deployment |

---

## System Architecture

The application follows a modular architecture separating automata construction, processing, visualization, and user interaction.

```text
              Regular Expression
                      |
                      v
                Regex Parser
                      |
                      v
               Postfix Expression
                      |
                      v
           Thompson's Construction
                      |
                      v
                    ε-NFA
                      |
                      v
              Subset Construction
                      |
                      v
                     DFA
                      |
                      v
              DFA Minimization
                      |
                      v
                Minimized DFA
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       String     Equivalence  Visualization
     Recognition    Checker     (Graphviz)
          |
          v
      Batch Testing
```

### Project Structure

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
│   ├── __init__.py
│   ├── regex_parser.py
│   ├── nfa.py
│   ├── dfa.py
│   ├── minimizer.py
│   ├── recognizer.py
│   └── equivalence.py
│
├── visualization/
│   ├── __init__.py
│   └── automata_graph.py
│
├── tests/
│   ├── test_regex.py
│   ├── test_nfa.py
│   ├── test_dfa.py
│   ├── test_minimizer.py
│   ├── test_recognizer.py
│   ├── test_equivalence.py
│   ├── test_visualization.py
│   └── test_integration.py
│
└── screenshots/
    ├── home.png
    ├── nfa.png
    ├── minimized-dfa.png
    ├── string-testing.png
    └── batch-testing.png
```

---

## Supported Regular Expression Syntax

| Operator | Meaning | Example |
|---|---|---|
| `a`, `b` | Single-character literals | `ab` |
| `\|` | Union | `a\|b` |
| `*` | Kleene Star | `a*` |
| `()` | Grouping | `(a\|b)*` |
| Implicit concatenation | Sequence of symbols | `abb` |

**Current limitations:** The parser supports single-character literals, union, Kleene star, grouping, and implicit concatenation. Operators such as `+`, `?`, character classes, escape sequences, and explicit epsilon expressions are not currently supported.

---

## Example: Automata Construction

Consider the regular expression:

```text
(a|b)*abb
```

This represents all strings over the alphabet `{a, b}` that end with `abb`.

The construction pipeline produces:

| Automaton | Number of States |
|---|---:|
| ε-NFA | 14 |
| DFA | 5 |
| Minimized DFA | 4 |

The minimized DFA recognizes exactly the same language while using fewer states.

### String Recognition Examples

| Input String | Result |
|---|---|
| `abb` | Accepted |
| `aabb` | Accepted |
| `babb` | Accepted |
| `aaabb` | Accepted |
| `aba` | Rejected |
| `ab` | Rejected |
| `abba` | Rejected |

---

## Testing and Validation

The project includes an automated test suite developed using Pytest.

**54 automated tests pass** across the following components:

| Component | Tests |
|---|---:|
| Regular Expression Parser | 6 |
| ε-NFA Construction | 8 |
| DFA Construction | 8 |
| DFA Minimization | 6 |
| String Recognition | 7 |
| Equivalence Checking | 7 |
| Graphviz Visualization | 6 |
| Integration Testing | 6 |
| **Total** | **54** |

Run the complete test suite:

```bash
python -m pytest -v
```

---

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Graphviz system application

### 1. Clone the repository

```bash
git clone https://github.com/sarah-jz/automata-pattern-engine.git

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Graphviz

Download and install Graphviz:

https://graphviz.org/download/

Ensure the Graphviz `bin` directory is available in your system PATH.

### 5. Run the application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## Academic Concepts Demonstrated

This project applies fundamental concepts from Automata Theory and theoretical computer science:

- Regular Expressions and Regular Languages
- Finite Automata
- Nondeterministic Finite Automata
- Epsilon Transitions and Epsilon Closure
- Thompson's Construction
- Subset Construction
- DFA Minimization
- State Equivalence
- Language Recognition
- Product Automata
- Breadth-First Search
- Equivalence of Regular Languages

---

## Future Improvements

Potential extensions include:

- Support for additional regular expression operators.
- Interactive step-by-step animation of automata execution.
- Exporting automata diagrams in multiple formats.
- More advanced regular expression analysis.
- Additional visualization and debugging capabilities.

---

## Deployment

The application is publicly deployed using Streamlit Community Cloud.

**Live Application:**  
https://automata-pattern-engine.streamlit.app/

**Source Code:**  
https://github.com/sarah-jz/automata-pattern-engine

---

## Author

Developed as an individual academic project exploring the implementation and practical application of concepts from Automata Theory.
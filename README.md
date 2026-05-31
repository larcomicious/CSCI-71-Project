# CSCI 71 Project: Multiple Balanced Brackets

A Python simulation of a **Pushdown Automaton (PDA)** that validates and evaluates
strings containing multiple types of balanced brackets.

Built for CSCI 71 (Theory of Computation) at Ateneo de Manila University.

## Overview

The program has two core functions:

- **`is_balanced()`** — simulates a PDA by final state to determine if an input string is valid. A valid string starts and ends with `!`, contains only balanced brackets (`< >`, `{ }`, `[ ]`, `( )`) and the symbol `x` in between.
- **`evaluate()`** — if the string is valid, applies bracket operations to count the resulting number of `x`'s.

### Bracket Operations

| Bracket | Operation | Example |
|---------|-----------|---------|
| `<S>` | doubles the x's inside | `<xx>` → `xxxx` (4) |
| `{S}` | adds one x | `{xx}` → `xxx` (3) |
| `[S]` | empties the x's | `[xxx]` → `` (0) |
| `(xS)` | removes one x | `(xxx)` → `xx` (2) |

## How to Run

### Prerequisites

- Python 3.x (no external libraries needed)

### Setup

1. Clone the repo

```bash
git clone https://github.com/yourusername/pda-brackets.git
cd pda-brackets
```

2. Add your input strings to `input.txt`, one per line. Example:

```
!xx[x({xx})[xxx]x]<xxx>x!
![<]>!
!<x{[()]}x>!
```

3. Run the program

```bash
python main.py
```

## Sample Output

```
Processing !<x{[()]}x>!
ID: (q0, !<x{[()]}x>!, Z)
ID: (q1, <x{[()]}x>!, !Z)
...
q2 is a final state.
!<x{[()]}x>! is valid and has balanced brackets.

!<x{[()]}x>! - Resulting number of x's: 6
![<]>! - Invalid string.
```

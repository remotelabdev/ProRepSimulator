# Proportional Representation Simulator

**Production-ready implementation of proportional representation electoral systems**

Clean, professional Python implementation with comprehensive docstrings following PEP 257.

## About This Branch

This is the **production branch** - a clean, well-documented implementation ready for integration into other projects.

**Looking for the educational version?** Switch to the `main` branch to see the complete development journey with detailed bug explanations and learning notes.

## Features

### Implemented Electoral Methods

- **D'Hondt method**: Divisor-based allocation that slightly favors larger parties
- **Sainte-Laguë method**: Modified divisor method providing more proportional results
- **Open List PR**: Two-stage system where voter preferences override party rankings

### Technical Highlights

- ✅ PEP 8 compliant code
- ✅ Comprehensive docstrings (PEP 257)
- ✅ Type-safe integer arithmetic (avoids floating-point rounding)
- ✅ Clean class-based architecture
- ✅ No external dependencies for core algorithms
- ✅ Well-tested allocation methods

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ProRepSimulator

# Switch to production branch
git checkout production

# No dependencies needed for core algorithms
# Optional: Install visualization dependencies
pip install -r requirements.txt
```

## Quick Start

### D'Hondt Method

```python
from src.main import DHondt

# Define election parameters
election = DHondt(
    parties=['Party A', 'Party B', 'Party C'],
    votes={'Party A': 100000, 'Party B': 80000, 'Party C': 30000},
    total_seats=100
)

# Run allocation
election.dhondt()
print(election._seat_allocation)
# Output: {'Party A': 48, 'Party B': 38, 'Party C': 14}
```

### Sainte-Laguë Method

```python
from src.main import SainteLague

election = SainteLague(
    parties=['Party A', 'Party B', 'Party C'],
    votes={'Party A': 100000, 'Party B': 80000, 'Party C': 30000},
    total_seats=100
)

election.satinelague()
print(election._seat_allocation)
# Output: {'Party A': 48, 'Party B': 38, 'Party C': 14}
```

### Comparing Methods

```python
from src.main import CompareSeatAllocation

params = {
    'parties': ['Party A', 'Party B', 'Party C'],
    'votes': {'Party A': 100000, 'Party B': 80000, 'Party C': 30000},
    'total_seats': 5  # Smaller numbers show differences
}

compare = CompareSeatAllocation(
    method_label1='dhondt',
    method_label2='satine_lague',
    params=params
)

results = compare.run_calculations()
allocations, differences = compare.get_comparison_results()

print(allocations)
# D'Hondt: Party A=3, Party B=2, Party C=0
# Sainte-Laguë: Party A=2, Party B=2, Party C=1
```

### Open List PR

```python
from src.main import Candidate, OpenListPR

# Define candidates with party rankings
candidates = [
    Candidate(name="Alice", party="Party A", list_position=1),
    Candidate(name="Bob", party="Party A", list_position=2),
    Candidate(name="Carol", party="Party A", list_position=3),
]

# Run open list election
election = OpenListPR(
    parties=['Party A'],
    candidates=candidates,
    party_votes={'Party A': 100000},
    candidate_votes={'Alice': 10000, 'Bob': 30000, 'Carol': 25000},
    total_seats=2,
    method='dhondt',
    ranking_variant='pure'
)

results = election.run_election()

# Check results
for candidate in candidates:
    if candidate.elected:
        print(f"{candidate._name}: Elected (rank {candidate.final_rank})")
# Output:
# Bob: Elected (rank 1)    - jumped from position 2
# Carol: Elected (rank 2)  - jumped from position 3
# Alice dropped to rank 5 despite being #1 on party list!
```

## API Reference

### DHondt Class

```python
DHondt(parties: list, votes: dict, total_seats: int)
```

**Methods:**
- `dhondt()`: Run D'Hondt allocation algorithm

**Attributes:**
- `_seat_allocation`: Dictionary mapping parties to seat counts

### SainteLague Class

```python
SainteLague(parties: list, votes: dict, total_seats: int)
```

**Methods:**
- `satinelague()`: Run Sainte-Laguë allocation algorithm

**Attributes:**
- `_seat_allocation`: Dictionary mapping parties to seat counts

### Candidate Class

```python
Candidate(name: str, party: str, list_position: int)
```

**Attributes:**
- `_name`: Candidate name
- `_party`: Party affiliation
- `_list_position`: Position on party list
- `elected`: Boolean indicating if elected
- `final_rank`: Final ranking after preference votes

### OpenListPR Class

```python
OpenListPR(
    parties: list,
    candidates: list,
    party_votes: dict,
    candidate_votes: dict,
    total_seats: int,
    method: str = 'dhondt',
    ranking_variant: str = 'pure'
)
```

**Methods:**
- `run_election()`: Execute two-stage allocation

**Returns:**
- Dictionary with `party_seats`, `elected_candidates`, `candidate_rankings`

## Algorithm Overview

### D'Hondt Method

Uses divisor formula: `votes / (seats + 1)`

Allocates seats iteratively to the party with the highest quotient. Slightly favors larger parties.

### Sainte-Laguë Method

Uses divisor formula: `votes / (2 × seats + 1)`

More proportional than D'Hondt, gives smaller parties fairer representation.

### Open List PR

Two-stage process:
1. **Party allocation**: Seats distributed to parties using D'Hondt or Sainte-Laguë
2. **Candidate selection**: Within each party, candidates ranked by preference votes

Voters can override party rankings through preference voting.

## Project Structure

```
ProRepSimulator-production/
├── src/
│   └── main.py                     # Core implementation
├── docs/
│   ├── OPEN_LIST_DESIGN.md         # Technical specification
│   ├── OPENLIST_QUICKSTART.md      # Conceptual guide
│   └── VISUALIZATION_GUIDE.md      # Chart customization
├── demo_openlist.py                # Demo script
├── visualize_openlist.py           # Visualization generator
├── requirements.txt                # Optional dependencies
└── README.md                       # This file
```

## Educational Resources

For learning materials, bug explanations, and development journey:

```bash
git checkout main
```

The main branch contains:
- Detailed bug documentation (13 bugs explained)
- Vivid analogies for complex concepts
- Personal debugging notes
- Complete learning journey

## Use Cases

- **Electoral Analysis**: Analyze proportional representation outcomes
- **Education**: Teach electoral system mechanics
- **Integration**: Embed in larger voting system projects
- **Research**: Compare different allocation methods
- **Prototyping**: Test electoral scenarios quickly

## Testing

```bash
# Run demo to verify installation
python3 demo_openlist.py

# Generate visualizations (requires matplotlib, numpy)
pip install -r requirements.txt
python3 visualize_openlist.py
```

## Author

Neo

## License

Educational project - free to use for learning and research purposes.

## Contributing

This is an educational project. For bug reports or suggestions, please open an issue on GitHub.

---

**Branch Info**: You are viewing the production branch (clean implementation)
**Educational Version**: Switch to `main` branch for learning materials

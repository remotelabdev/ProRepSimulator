# Proportional Representation Simulator

**Educational tool for exploring proportional representation electoral systems**

This project implements multiple electoral methods used in proportional representation voting systems:

- **D'Hondt method**: Divisor-based method that slightly favors larger parties
- **Sainte-Laguë method**: Modified divisor method that is more proportional
- **Open List PR**: Two-stage system where voters can override party rankings through preference votes

## Two Versions Available

This repository maintains two parallel versions in separate git branches:

### 📚 Main Branch (Educational Version)
**Location**: `ProRepSimulator/` (this directory)

Contains the complete learning journey with detailed bug explanations and personal debugging notes. Every bug that was discovered and fixed during development is documented with:
- Technical explanation of what was wrong
- Vivid analogy to make the concept memorable
- The fix that was applied
- Personal notes about the debugging process

**Purpose**: Portfolio piece and learning artifact demonstrating debugging skills and code evolution

### 🚀 Production Branch (Clean Version)
**Location**: `ProRepSimulator-production/` (separate worktree)

Clean, professional implementation with proper docstrings following PEP 257. All bug explanation comments removed, replaced with standard Python documentation.

**Purpose**: Production-ready code for actual use

## Accessing Both Versions

Both versions are maintained using git worktrees:

```bash
# Current directory (main branch - educational version)
cd ProRepSimulator
git branch  # Shows: * main

# Production directory (production branch - clean version)
cd ../ProRepSimulator-production
git branch  # Shows: * production

# List all worktrees
git worktree list
```

## Features

### Core Algorithms
- ✅ **Two allocation methods**: D'Hondt and Sainte-Laguë
- ✅ **Open List PR**: Voter preferences override party rankings
- ✅ **Comparison framework**: Compare results between methods
- ✅ **PEP 8 compliant**: Clean, properly formatted Python code
- ✅ **Type-safe calculations**: Integer-domain algorithms avoiding floating-point rounding issues

### Educational Materials
- ✅ **Interactive Jupyter notebooks**: Modify scenarios and see results instantly
- ✅ **Command-line demos**: Quick demonstrations (`demo_openlist.py`)
- ✅ **Professional visualizations**: Charts showing candidate "jumps"
- ✅ **Comprehensive documentation**: Quick-start guides and technical specs

## Usage

### Basic Usage

```python
from src.main import DHondt, SatineLague

# Define election parameters
params = {
    'parties': ['Party A', 'Party B', 'Party C'],
    'votes': {'Party A': 100000, 'Party B': 80000, 'Party C': 30000},
    'total_seats': 100
}

# Run D'Hondt method
dhondt = DHondt(**params)
dhondt.dhondt()
print(dhondt._seat_allocation)
# Output: {'Party A': 48, 'Party B': 38, 'Party C': 14}

# Run Sainte-Laguë method
satinelague = SatineLague(**params)
satinelague.satinelague()
print(satinelague._seat_allocation)
# Output: {'Party A': 48, 'Party B': 38, 'Party C': 14}
```

### Comparing Methods

```python
from src.main import CompareSeatAllocation

compare = CompareSeatAllocation(
    method_label1='dhondt',
    method_label2='satine_lague',
    params=params
)

# Run both methods
results = compare.run_calculations()

# Get comparison
party_allocations, differences = compare.get_comparison_results()
print(party_allocations)
print(differences)
```

### Open List PR

```python
from src.main import Candidate, OpenListPR

# Create candidates with list positions
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
# Bob and Carol elected (jumped ahead of Alice!)
```

### Quick Demos

```bash
# Command-line demo
python3 demo_openlist.py

# Generate visualizations (requires matplotlib)
pip install -r requirements.txt
python3 visualize_openlist.py

# Interactive Jupyter notebooks
jupyter notebook openlist_demo.ipynb
jupyter notebook dhondt_visualizer.ipynb
```

## Key Insights

### When Methods Differ

The two methods produce different results with smaller seat counts:

**5 seats**:
- D'Hondt: Party A=3, Party B=2, Party C=0
- Sainte-Laguë: Party A=2, Party B=2, Party C=1

**100 seats**:
- Both methods: Party A=48, Party B=38, Party C=14 (converge to same result)

### Algorithm Comparison

| Method | Formula | Bias |
|--------|---------|------|
| D'Hondt | votes / (seats + 1) | Slightly favors larger parties |
| Sainte-Laguë | votes / (2×seats + 1) | More proportional |

## Development Journey (Main Branch Only)

The main branch documents 13 bugs that were discovered and fixed:

1. **Bug #1**: Type error calling `.keys()` on sorted list
2. **Bug #2**: Wrong sort order (ascending vs descending)
3. **Bug #3**: Double increment awarding 2 seats instead of 1
4. **Bug #4**: Missing iteration logic
5. **Bug #5**: Empty loop body
6. **Bug #6**: Indentation error in elif block
7. **Bug #7**: Not saving/returning results
8. **Bug #8**: String inconsistency in dict keys
9. **Bug #9**: Missing parentheses on `.items()`
10. **Bug #10**: Wrong dict unpacking
11. **Bug #11**: KeyError risk from checking before existence
12. **Bug #12**: Parameter unpacking confusion
13. **Bug #13**: Leftover tuple-based logic after transpose

Each bug is documented in the code with technical explanation, vivid analogy, and the fix applied.

## Project Structure

```
ProRepSimulator/                    # Main branch (educational)
├── src/
│   └── main.py                     # Core algorithms (DHondt, SatineLague, OpenListPR)
├── docs/
│   ├── OPEN_LIST_DESIGN.md         # Technical specification
│   ├── OPENLIST_QUICKSTART.md      # Beginner-friendly guide
│   └── VISUALIZATION_GUIDE.md      # Chart customization
├── demo_openlist.py                # Command-line demonstration
├── openlist_demo.ipynb             # Interactive Open List notebook
├── visualize_openlist.py           # Visualization generator
├── dhondt_visualizer.ipynb         # D'Hondt vs Sainte-Laguë comparison
├── requirements.txt                # Python dependencies
└── README.md                       # This file

ProRepSimulator-production/         # Production branch (clean)
└── src/
    └── main.py                     # Clean implementation
```

## Documentation

- **[Open List Quick Start](docs/OPENLIST_QUICKSTART.md)** - What is Open List PR and why it matters
- **[Technical Design](docs/OPEN_LIST_DESIGN.md)** - Algorithm details and data structures
- **[Visualization Guide](docs/VISUALIZATION_GUIDE.md)** - Customizing charts and graphs

## Author

Neo

## License

Educational project - feel free to use for learning purposes.

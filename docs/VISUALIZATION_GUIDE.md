# Visualization Guide

## Overview

The `visualize_openlist.py` script generates professional-quality charts showing how Open List PR works, including dramatic visualizations of candidates "jumping" positions based on preference votes.

## Installation

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install matplotlib numpy
```

## Running the Visualizations

```bash
python3 visualize_openlist.py
```

This generates 5 PNG files in the project root directory.

## Generated Visualizations

### 1. Party Allocation (`party_allocation.png`)

**Two-panel visualization:**
- **Left panel**: Bar chart comparing vote percentage vs seat percentage
  - Shows proportionality (or lack thereof) in seat allocation
  - Side-by-side bars make differences immediately visible
- **Right panel**: Pie chart of final seat distribution
  - Shows each party's share of total seats
  - Includes both absolute numbers and percentages

**Key insight**: Demonstrates how D'Hondt/Sainte-Laguë converts votes into seats.

### 2. Candidate Jump Visualizations (3 files)

**One chart per party:**
- `candidate_jumps_party_a.png`
- `candidate_jumps_party_b.png`
- `candidate_jumps_party_c.png`

**Each chart shows:**
- **Left boxes**: Party-assigned list positions (beige)
- **Middle section**: Candidate names and preference vote counts
- **Right boxes**: Final ranking after votes counted
  - Green = Elected
  - Gray = Not elected
- **Curved arrows**: Show position jumps
  - ⬆️ indicator shows how many positions jumped

**Example from Party A:**
```
List Position    Name     Votes        Final Rank
#1 ────────────> Alice    8,000    ───────> #5  ✓ ELECTED
#2 ─────⬆️──────> Bob      35,000   ───────> #1  ✓ ELECTED  (⬆️ +1)
#3 ─────⬆️──────> Carol    28,000   ───────> #2  ✓ ELECTED  (⬆️ +1)
#4 ─────⬆️──────> David    15,000   ───────> #3  ✓ ELECTED  (⬆️ +1)
#5 ─────⬆️──────> Eve      10,000   ───────> #4  ✓ ELECTED  (⬆️ +1)
```

**Key insight**: Visually demonstrates voter power to override party rankings.

### 3. Preference Votes Distribution (`preference_votes.png`)

**Three-panel horizontal bar chart:**
- One panel per party
- Candidates sorted by preference votes (most votes at top)
- Elected candidates shown in party color
- Non-elected candidates shown in gray
- Vote counts labeled on bars
- ✓ checkmark indicates elected candidates

**Key insight**: Shows which candidates were popular with voters.

## Customizing Visualizations

### Change the Scenario

Edit the data in `visualize_openlist.py`:

```python
# Modify party votes
party_votes = {
    'Party A': 150000,  # Increased from 100,000
    'Party B': 80000,
    'Party C': 30000,
}

# Modify candidate preference votes
candidate_votes = {
    "Alice": 50000,  # Make Alice more popular
    "Bob": 35000,
    # ...
}
```

### Change Colors

Modify the color scheme:

```python
# Party colors (line 102)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

# Change to different colors
colors = ['#E74C3C', '#3498DB', '#2ECC71']  # Red, Blue, Green
```

### Adjust Chart Size

Modify figure sizes:

```python
# For party allocation (line 23)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))  # Wider

# For candidate jumps (line 70)
fig, ax = plt.subplots(figsize=(14, 10))  # Taller
```

## Using in Jupyter Notebooks

You can import the visualization functions directly:

```python
from visualize_openlist import create_party_allocation_chart
from visualize_openlist import create_candidate_jump_visualization
from visualize_openlist import create_preference_votes_chart

# After running your election...
results = election.run_election()

# Generate charts
fig1 = create_party_allocation_chart(party_votes, results['party_seats'], 10)
fig2 = create_candidate_jump_visualization(candidates, candidate_votes, 'Party A')

# Display in notebook
plt.show()
```

## Understanding the Visual Elements

### Color Coding

| Color | Meaning |
|-------|---------|
| **Green** (#4CAF50) | Elected candidates |
| **Gray** (#CCCCCC) | Non-elected candidates |
| **Beige** (#FFE5B4) | List position boxes (party ranking) |
| **Party A** (#FF6B6B) | Red |
| **Party B** (#4ECDC4) | Teal |
| **Party C** (#45B7D1) | Blue |

### Symbols

| Symbol | Meaning |
|--------|---------|
| ⬆️ | Candidate jumped ahead |
| ✓ | Candidate elected |
| +N | Jumped N positions |
| → | Direction of flow (list → votes → final rank) |

## Technical Details

### Chart Types Used

1. **Bar charts**: Comparisons (votes vs seats)
2. **Pie charts**: Proportions (seat distribution)
3. **Horizontal bar charts**: Rankings (preference votes)
4. **Custom flow diagrams**: Position changes (jumps)

### Libraries

- **matplotlib**: Core plotting library
- **numpy**: Numerical operations for positioning
- **FancyBboxPatch**: Rounded rectangles for position boxes
- **FancyArrowPatch**: Curved arrows showing jumps

### Output Format

- **Format**: PNG (Portable Network Graphics)
- **Resolution**: 300 DPI (print quality)
- **Size**: Variable based on content
- **Typical file size**: 100-300 KB per image

## Tips for Presentations

### For Educational Use

1. **Show party allocation first** - Establishes the context (how many seats each party won)
2. **Then show candidate jumps** - Demonstrates the "surprise" of voter override
3. **End with preference votes** - Explains WHY candidates jumped

### For Comparison Studies

Generate multiple sets with different parameters:

```bash
# Scenario 1: Pure open list
python3 visualize_openlist.py
mv *.png scenario1/

# Scenario 2: Modified candidate votes
# (edit visualize_openlist.py)
python3 visualize_openlist.py
mv *.png scenario2/
```

### For Academic Papers

The 300 DPI resolution is publication-quality. Charts can be directly embedded in LaTeX or Word documents.

## Troubleshooting

### "No module named 'matplotlib'"

```bash
pip install matplotlib numpy
```

### Charts Don't Display

If running on a headless server:

```python
# Add before plt.show()
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

### Font Rendering Issues

If fonts look wrong:

```python
# Add at the top of the script
plt.rcParams['font.family'] = 'DejaVu Sans'
```

### Image Files Not Generated

Check write permissions in the project directory:

```bash
ls -la *.png
```

## Example Output Description

Running the default scenario generates visualizations showing:

- **Party A**: 4 out of 5 elected candidates jumped positions
  - Alice (position 1) drops to rank 5 despite being top of list
  - Bob, Carol, David, Eve all jump ahead

- **Party B**: Grace (position 2) jumps to rank 1
  - Frank (position 1) drops to rank 2

- **Party C**: Kate (position 2) jumps to rank 1
  - Jack (position 1) drops to rank 2 (but not elected)

**Total dramatic effect**: 6 out of 10 elected candidates jumped!

## Next Steps

- Create animated visualizations showing the counting process
- Add interactive HTML visualizations with D3.js
- Generate comparison charts (D'Hondt vs Sainte-Laguë)
- Create "what-if" scenarios with sliders

---

**Remember**: These visualizations make abstract voting concepts concrete. The visual impact of seeing Alice drop from #1 to #5 is far more powerful than reading about it in text!

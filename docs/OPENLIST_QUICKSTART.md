# Open List PR - Quick Start Guide

## What is Open List Proportional Representation?

Open List PR is a **two-stage** electoral system that combines:
1. **Party proportionality** - Seats allocated to parties based on total votes
2. **Voter choice** - Individual voters decide which candidates win seats

Unlike closed list systems where parties control candidate ranking, **voters have the power to override party preferences**.

## How It Works

### Stage 1: Party Seat Allocation
Use D'Hondt or Sainte-Laguë to determine how many seats each party wins.

**Example:**
```
Party A: 100,000 votes → 5 seats
Party B:  80,000 votes → 4 seats
Party C:  30,000 votes → 1 seat
```

### Stage 2: Candidate Selection
Voters cast preference votes for individual candidates. Candidates with the most preference votes win their party's allocated seats.

**Example (Party A won 5 seats):**
```
List Position  Candidate  Preference Votes  Final Rank  Elected?
─────────────────────────────────────────────────────────────────
1              Alice      8,000             5           ✓ Yes
2              Bob        35,000            1           ✓ Yes  ⬆️ JUMPED!
3              Carol      28,000            2           ✓ Yes  ⬆️ JUMPED!
4              David      15,000            3           ✓ Yes  ⬆️ JUMPED!
5              Eve        10,000            4           ✓ Yes  ⬆️ JUMPED!
```

Notice: **Bob, Carol, David, and Eve all jumped ahead of Alice** despite her being #1 on the party list!

## Running the Demo

### Option 1: Jupyter Notebook (Interactive)

```bash
jupyter notebook openlist_demo.ipynb
```

The notebook includes:
- ✅ Pre-configured scenarios with 3 parties, 10 seats
- ✅ Interactive cells you can modify
- ✅ Visualizations showing who "jumped" positions
- ✅ Comparison: Open List vs Closed List
- ✅ Comparison: D'Hondt vs Sainte-Laguë

### Option 2: Python Script (Quick Test)

```python
from src.main import Candidate, OpenListPR

# Create candidates
candidates = [
    Candidate(name="Alice", party="Party A", list_position=1),
    Candidate(name="Bob", party="Party A", list_position=2),
    Candidate(name="Carol", party="Party A", list_position=3),
]

# Run election
election = OpenListPR(
    parties=['Party A'],
    candidates=candidates,
    party_votes={'Party A': 100000},
    candidate_votes={
        'Alice': 10000,
        'Bob': 30000,    # Bob is most popular
        'Carol': 25000,
    },
    total_seats=2,
    method='dhondt',
    ranking_variant='pure'
)

results = election.run_election()

# Show winners
for candidate in results['elected_candidates']:
    print(f"{candidate._name}: rank #{candidate.final_rank}")
# Output:
#   Bob: rank #1    (jumped from position 2!)
#   Carol: rank #2  (jumped from position 3!)
```

## Key Takeaways from the Demo

### 1. **Voters Override Party Rankings**

In the demo scenario:
- **5 out of 10 elected candidates** jumped ahead of their list positions
- Alice (Party A #1) dropped to 5th place despite being top of the list
- Bob (Party A #2) won the most preference votes and jumped to 1st

This is **pure democracy** - voters decide, not party leaders.

### 2. **Popular Candidates Win Regardless of Position**

The three "list position #2" candidates all jumped to #1:
- Bob (Party A): 35,000 preference votes → jumped to #1
- Grace (Party B): 30,000 preference votes → jumped to #1
- Kate (Party C): 20,000 preference votes → jumped to #1

**Lesson**: Being at the top of the party list doesn't guarantee winning!

### 3. **Different from Closed List**

| System | Who Controls Ranking? | Example |
|--------|----------------------|---------|
| **Closed List** | Party leaders decide | Alice (position 1) always wins first seat |
| **Open List** | Voters decide via preference votes | Bob beats Alice if he gets more votes |

### 4. **Method Affects Party Seats, Not Candidate Ranking**

Changing from D'Hondt to Sainte-Laguë:
- ✅ **Changes**: How many seats each party wins
- ❌ **Doesn't change**: Candidate ranking within parties (still by preference votes)

## Three Ranking Variants

### Pure Open List (Implemented)
- **Rule**: Candidates ranked purely by preference votes
- **Effect**: Voters have complete control
- **Used in**: Netherlands, Brazil, Indonesia

### Modified Open List (Coming Soon)
- **Rule**: Need X% of party votes to override list position
- **Effect**: Balance between party and voter control
- **Used in**: Poland, Belgium

### Flexible List (Coming Soon)
- **Rule**: Need majority (>50%) to override
- **Effect**: Party list usually respected, rare exceptions
- **Used in**: Austria, Czech Republic

## Try It Yourself!

**Modify the notebook** to explore different scenarios:

1. **Change preference votes**: What if Alice gets 50,000 votes instead of 8,000?
2. **Add more candidates**: What happens with 10 candidates per party?
3. **Change total seats**: How does increasing to 20 seats affect results?
4. **Adjust party votes**: What if Party C gets 100,000 votes?

## Next Steps

- 📖 Read [OPEN_LIST_DESIGN.md](OPEN_LIST_DESIGN.md) for technical details
- 🎨 Explore the Jupyter notebook (`openlist_demo.ipynb`)
- 🔬 Implement Modified/Flexible variants
- 📊 Create visualizations showing candidate "jumps"

---

**Question**: Why does this matter?

**Answer**: Open List PR gives voters **individual choice** while maintaining **proportional representation**. You can support a party's overall platform while choosing which specific candidates represent you. This is considered one of the most democratic electoral systems.

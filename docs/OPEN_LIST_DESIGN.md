# Open List Proportional Representation: Technical Design

**Focus**: Mathematical algorithms and data structures (no political references)

---

## Concept Overview

**Open List PR** extends basic proportional representation by adding candidate selection:

```
Basic PR:          Voters choose → Party
                   Algorithm determines → Party seat allocation

Open List PR:      Voters choose → Party + Candidates within party
                   Algorithm determines → Party seats + Which candidates win those seats
```

---

## Two-Stage Process

### Stage 1: Party Seat Allocation
Uses existing D'Hondt or Sainte-Laguë algorithms (already implemented).

**Input:**
- Party votes (total votes for each party)
- Total seats to allocate

**Output:**
- Seat count per party

**Example:**
```
Party A: 100,000 votes → 5 seats
Party B:  80,000 votes → 4 seats
Party C:  30,000 votes → 1 seat
```

### Stage 2: Candidate Selection Within Parties
Determines **which specific candidates** fill each party's allocated seats.

**Input:**
- Party's allocated seat count (from Stage 1)
- Candidate list for that party
- Preference votes for each candidate

**Output:**
- Ranked list of candidates
- Top N candidates win seats (N = party's seat count)

---

## Data Structures

### Candidate Class

```python
class Candidate:
    """Represents a candidate on a party's list."""

    def __init__(self, name, party, list_position):
        """
        Args:
            name: Candidate's identifier (e.g., "Candidate A1")
            party: Which party this candidate belongs to
            list_position: Party's suggested ranking (1 = top of list)
        """
        self.name = name
        self.party = party
        self.list_position = list_position
        self.preference_votes = 0
        self.elected = False
        self.final_rank = None  # Determined after counting
```

### Ballot Structure

```python
# Example ballot data
party_vote = "Party A"  # Which party the voter supports
candidate_preferences = ["Candidate A3", "Candidate A1"]  # Optional candidate preferences
```

---

## Ranking Algorithms: Three Variants

### Variant 1: Pure Open List (Most Democratic)

**Rule**: Candidates ranked purely by preference votes

```python
def rank_candidates_pure_open(candidates, preference_votes):
    """
    Rank candidates purely by preference votes.

    List position is ignored completely.
    Used in: Netherlands-style systems
    """
    for candidate in candidates:
        candidate.preference_votes = preference_votes.get(candidate.name, 0)

    # Sort by preference votes (descending)
    ranked = sorted(candidates, key=lambda c: c.preference_votes, reverse=True)
    return ranked
```

**Example:**
```
Party A won 5 seats. Their candidates:

List Position  Candidate  Preference Votes  Final Rank  Elected?
─────────────────────────────────────────────────────────────────
1              Alice      1,000             3           ✓ Yes
2              Bob        5,000             1           ✓ Yes  (jumped!)
3              Carol      3,000             2           ✓ Yes  (jumped!)
4              David        500             4           ✓ Yes
5              Eve          300             5           ✓ Yes
6              Frank        100             6           ✗ No
─────────────────────────────────────────────────────────────────

Bob and Carol received more preference votes than Alice,
so they win seats ahead of her despite lower list positions.
```

### Variant 2: Modified Open List (Threshold Required)

**Rule**: Need minimum preference votes to override list position

```python
def rank_candidates_modified_open(candidates, preference_votes,
                                   party_total_votes, threshold_percent=5.0):
    """
    Rank candidates with threshold requirement.

    Candidates need threshold_percent of party votes to override list position.
    Otherwise, list position is used.

    Args:
        threshold_percent: E.g., 5.0 means candidate needs 5% of party's total votes
    """
    threshold_votes = party_total_votes * (threshold_percent / 100)

    for candidate in candidates:
        pref_votes = preference_votes.get(candidate.name, 0)
        candidate.preference_votes = pref_votes

        # Use preference votes if threshold met, otherwise use list position
        if pref_votes >= threshold_votes:
            # Negate so higher votes = lower rank number
            candidate.rank_score = -pref_votes
        else:
            # Use list position (lower is better)
            candidate.rank_score = candidate.list_position

    # Sort by rank score (lower is better)
    ranked = sorted(candidates, key=lambda c: candidate.rank_score)
    return ranked
```

**Example:**
```
Party A: 100,000 total votes, 5% threshold = 5,000 votes needed

List Position  Candidate  Pref Votes  Threshold Met?  Final Rank  Elected?
────────────────────────────────────────────────────────────────────────────
1              Alice      1,000       ✗ No            1           ✓ Yes
2              Bob        8,000       ✓ Yes           2           ✓ Yes (deserved!)
3              Carol      3,000       ✗ No            3           ✓ Yes
4              David      6,000       ✓ Yes           4           ✓ Yes (deserved!)
5              Eve          500       ✗ No            5           ✓ Yes
6              Frank      2,000       ✗ No            6           ✗ No
────────────────────────────────────────────────────────────────────────────

Bob and David exceed threshold, so they override list position.
Others stay in list order.
```

### Variant 3: Flexible List (Majority Required)

**Rule**: Need majority of party's votes to override

```python
def rank_candidates_flexible(candidates, preference_votes, party_total_votes):
    """
    Rank candidates requiring majority to override.

    Very restrictive - candidate needs >50% of party votes to jump ahead.
    Essentially a closed list with rare exceptions.
    """
    majority_threshold = party_total_votes * 0.5

    # Similar logic to modified open, but with 50% threshold
    return rank_candidates_modified_open(
        candidates, preference_votes, party_total_votes, threshold_percent=50.0
    )
```

---

## Complete Algorithm: OpenListPR Class

```python
class OpenListPR:
    """
    Full open list proportional representation system.

    Combines:
    - Party seat allocation (D'Hondt or Sainte-Laguë)
    - Candidate ranking within parties
    """

    def __init__(self, parties, candidates, party_votes, candidate_votes,
                 total_seats, method='dhondt', ranking_variant='pure'):
        """
        Args:
            parties: List of party names
            candidates: List of Candidate objects
            party_votes: Dict {party_name: vote_count}
            candidate_votes: Dict {candidate_name: preference_vote_count}
            total_seats: Total seats to allocate
            method: 'dhondt' or 'satinelague'
            ranking_variant: 'pure', 'modified', or 'flexible'
        """
        self._parties = parties
        self._candidates = candidates
        self._party_votes = party_votes
        self._candidate_votes = candidate_votes
        self._total_seats = total_seats
        self._method = method
        self._ranking_variant = ranking_variant

        self._party_seats = {}
        self._elected_candidates = []

    def allocate_party_seats(self):
        """Stage 1: Determine how many seats each party gets."""
        if self._method == 'dhondt':
            allocator = DHondt(
                parties=self._parties,
                votes=self._party_votes,
                total_seats=self._total_seats
            )
            allocator.dhondt()
        else:  # satinelague
            allocator = SatineLague(
                parties=self._parties,
                votes=self._party_votes,
                total_seats=self._total_seats
            )
            allocator.satinelague()

        self._party_seats = allocator._seat_allocation
        return self._party_seats

    def rank_party_candidates(self, party):
        """
        Stage 2: Rank candidates within a single party.

        Returns:
            List of candidates sorted by rank (best to worst)
        """
        # Get all candidates from this party
        party_candidates = [c for c in self._candidates if c.party == party]

        # Apply ranking variant
        if self._ranking_variant == 'pure':
            return self._rank_pure_open(party_candidates)
        elif self._ranking_variant == 'modified':
            return self._rank_modified_open(party_candidates, party)
        else:  # flexible
            return self._rank_flexible(party_candidates, party)

    def _rank_pure_open(self, candidates):
        """Pure open list: sort by preference votes only."""
        for candidate in candidates:
            candidate.preference_votes = self._candidate_votes.get(candidate.name, 0)

        return sorted(candidates, key=lambda c: c.preference_votes, reverse=True)

    def _rank_modified_open(self, candidates, party, threshold_percent=5.0):
        """Modified open list: threshold required to override."""
        party_total = self._party_votes[party]
        threshold = party_total * (threshold_percent / 100)

        for candidate in candidates:
            pref_votes = self._candidate_votes.get(candidate.name, 0)
            candidate.preference_votes = pref_votes

            if pref_votes >= threshold:
                candidate.rank_score = -pref_votes  # Higher votes = lower score
            else:
                candidate.rank_score = candidate.list_position

        return sorted(candidates, key=lambda c: c.rank_score)

    def _rank_flexible(self, candidates, party):
        """Flexible list: 50% threshold required."""
        return self._rank_modified_open(candidates, party, threshold_percent=50.0)

    def allocate_candidate_seats(self):
        """
        Stage 2 (for all parties): Determine which candidates win seats.

        For each party:
        1. Rank candidates
        2. Top N candidates win (N = party's seat count)
        """
        self._elected_candidates = []

        for party, seat_count in self._party_seats.items():
            # Rank this party's candidates
            ranked = self.rank_party_candidates(party)

            # Top N win seats
            for i, candidate in enumerate(ranked):
                candidate.final_rank = i + 1

                if i < seat_count:
                    candidate.elected = True
                    self._elected_candidates.append(candidate)

        return self._elected_candidates

    def run_election(self):
        """Execute full open list PR election."""
        # Stage 1: Party seats
        self.allocate_party_seats()

        # Stage 2: Candidate seats
        self.allocate_candidate_seats()

        return {
            'party_seats': self._party_seats,
            'elected_candidates': self._elected_candidates
        }

    def display_results(self):
        """Print election results in readable format."""
        print("=" * 80)
        print("OPEN LIST PR ELECTION RESULTS")
        print("=" * 80)

        print("\nSTAGE 1: PARTY SEAT ALLOCATION")
        print("-" * 80)
        for party, seats in self._party_seats.items():
            votes = self._party_votes[party]
            total_votes = sum(self._party_votes.values())
            vote_pct = (votes / total_votes) * 100
            print(f"{party:15s}: {seats:3d} seats ({vote_pct:5.2f}% of votes)")

        print("\nSTAGE 2: ELECTED CANDIDATES (by party)")
        print("-" * 80)

        for party in self._parties:
            party_elected = [c for c in self._elected_candidates if c.party == party]

            if party_elected:
                print(f"\n{party}:")
                print(f"  {'Candidate':20s} {'List Pos':>8s} {'Pref Votes':>12s} "
                      f"{'Final Rank':>11s} {'Status':>8s}")
                print("  " + "-" * 70)

                # Show all candidates, not just elected
                all_party_cands = sorted(
                    [c for c in self._candidates if c.party == party],
                    key=lambda c: c.final_rank if c.final_rank else 999
                )

                for candidate in all_party_cands:
                    pref = self._candidate_votes.get(candidate.name, 0)
                    status = "✓ ELECTED" if candidate.elected else ""
                    print(f"  {candidate.name:20s} {candidate.list_position:8d} "
                          f"{pref:12,} {candidate.final_rank or '-':>11s} {status:>8s}")
```

---

## Example Usage

```python
# Define candidates
candidates = [
    Candidate("Alice", "Party A", list_position=1),
    Candidate("Bob", "Party A", list_position=2),
    Candidate("Carol", "Party A", list_position=3),
    Candidate("David", "Party A", list_position=4),
    Candidate("Eve", "Party A", list_position=5),

    Candidate("Frank", "Party B", list_position=1),
    Candidate("Grace", "Party B", list_position=2),
    Candidate("Henry", "Party B", list_position=3),
]

# Party votes (Stage 1 input)
party_votes = {
    'Party A': 100000,
    'Party B': 80000,
}

# Candidate preference votes (Stage 2 input)
candidate_votes = {
    # Party A: Bob is most popular!
    "Alice": 10000,
    "Bob": 35000,    # Most preference votes
    "Carol": 25000,  # Second most
    "David": 15000,
    "Eve": 8000,

    # Party B: List order mostly respected
    "Frank": 40000,
    "Grace": 25000,
    "Henry": 10000,
}

# Run election
election = OpenListPR(
    parties=['Party A', 'Party B'],
    candidates=candidates,
    party_votes=party_votes,
    candidate_votes=candidate_votes,
    total_seats=10,
    method='dhondt',
    ranking_variant='pure'  # Pure open list
)

results = election.run_election()
election.display_results()
```

---

## Key Design Decisions

### 1. Separate Party and Candidate Votes

**Why?**
- Party vote determines overall seat allocation
- Candidate votes only affect ranking within party
- Keeps the two stages conceptually distinct

**Alternative**: Count candidate votes toward party total
```python
# Some systems do this:
party_total_votes = sum(candidate_votes for all candidates in party)
```

### 2. Handling Candidates with Zero Preference Votes

**Options:**
1. **Keep list position** (implemented above)
2. **Put at bottom** regardless of list position
3. **Exclude entirely** if no votes received

**We chose option 1**: Voters may not express preferences for all candidates.

### 3. Tie-Breaking

**When candidates have equal preference votes:**
```python
# Use list position as tiebreaker
sorted(candidates, key=lambda c: (-c.preference_votes, c.list_position))
```

---

## Testing Scenarios

### Test 1: Pure Open List

```python
# Expected: Bob (pos 2) beats Alice (pos 1) due to preference votes
assert elected_candidates[0].name == "Bob"
assert elected_candidates[1].name == "Carol"
assert elected_candidates[2].name == "Alice"  # Despite being list #1
```

### Test 2: Modified Open List (5% threshold)

```python
# Party A: 100,000 votes, threshold = 5,000
# Bob has 35,000 (exceeds threshold) → overrides position
# Alice has 1,000 (below threshold) → keeps position 1
assert elected_candidates[0].name == "Alice"  # List position wins
assert elected_candidates[1].name == "Bob"    # Threshold exceeded
```

### Test 3: Party with More Seats than Candidates

```python
# Edge case: Party wins 10 seats but only has 5 candidates
# Result: All 5 candidates elected, 5 seats remain unfilled (rare in practice)
```

---

## Next Steps for Implementation

1. ✅ Create `Candidate` class
2. ✅ Create `OpenListPR` class with three variants
3. ⏳ Add visualization showing candidate "jumps"
4. ⏳ Interactive Jupyter demo
5. ⏳ Integration with existing DHondt/SatineLague classes

---

## Advantages of This Design

✅ **Modular**: Stage 1 and Stage 2 are independent
✅ **Flexible**: Three ranking variants supported
✅ **Testable**: Each stage can be tested separately
✅ **Educational**: Clear separation of concerns
✅ **Non-political**: Uses generic party/candidate names

This design keeps the focus on **algorithms and mathematics**, avoiding political examples entirely.

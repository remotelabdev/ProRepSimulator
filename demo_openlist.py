#!/usr/bin/env python3
"""
Open List PR Demo - Command Line Version

Run this script to see a quick demonstration of open list
proportional representation with voter preference overrides.

Usage:
    python3 demo_openlist.py
"""

import sys
sys.path.append('src')

from main import Candidate, OpenListPR


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80)


def print_section(title):
    """Print a section divider."""
    print("\n" + title)
    print("-" * 80)


def main():
    print_header("OPEN LIST PROPORTIONAL REPRESENTATION DEMO")

    print("\nThis demo shows how voters can override party rankings through")
    print("preference votes. Watch for the ⬆️ arrows - these candidates JUMPED!")

    # Create candidates with party-assigned list positions
    candidates = [
        # Party A candidates (list positions 1-5)
        Candidate(name="Alice", party="Party A", list_position=1),
        Candidate(name="Bob", party="Party A", list_position=2),
        Candidate(name="Carol", party="Party A", list_position=3),
        Candidate(name="David", party="Party A", list_position=4),
        Candidate(name="Eve", party="Party A", list_position=5),

        # Party B candidates (list positions 1-4)
        Candidate(name="Frank", party="Party B", list_position=1),
        Candidate(name="Grace", party="Party B", list_position=2),
        Candidate(name="Henry", party="Party B", list_position=3),
        Candidate(name="Iris", party="Party B", list_position=4),

        # Party C candidates (list positions 1-3)
        Candidate(name="Jack", party="Party C", list_position=1),
        Candidate(name="Kate", party="Party C", list_position=2),
        Candidate(name="Leo", party="Party C", list_position=3),
    ]

    # Party votes (Stage 1 input)
    party_votes = {
        'Party A': 100000,
        'Party B': 80000,
        'Party C': 30000,
    }

    # Candidate preference votes (Stage 2 input)
    # Notice: Some lower-ranked candidates have MORE preference votes!
    candidate_votes = {
        # Party A: Bob (position 2) is most popular!
        "Alice": 8000,    # List position 1, but LOW votes
        "Bob": 35000,     # List position 2, but HIGH votes - will jump!
        "Carol": 28000,   # List position 3, second highest votes
        "David": 15000,   # List position 4
        "Eve": 10000,     # List position 5

        # Party B: Grace (position 2) gets more votes than Frank!
        "Frank": 25000,   # List position 1
        "Grace": 30000,   # List position 2, but more votes - will jump!
        "Henry": 15000,   # List position 3
        "Iris": 8000,     # List position 4

        # Party C: Kate is very popular!
        "Jack": 5000,     # List position 1
        "Kate": 20000,    # List position 2, but most votes - will jump!
        "Leo": 3000,      # List position 3
    }

    # Run the election
    print_section("Running election with D'Hondt method...")

    election = OpenListPR(
        parties=['Party A', 'Party B', 'Party C'],
        candidates=candidates,
        party_votes=party_votes,
        candidate_votes=candidate_votes,
        total_seats=10,
        method='dhondt',
        ranking_variant='pure'  # Pure open list: voters fully control
    )

    results = election.run_election()

    # Display Stage 1 results
    print_header("STAGE 1: PARTY SEAT ALLOCATION (D'Hondt Method)")

    total_votes = sum(party_votes.values())

    print(f"\n{'Party':10s} {'Votes':>12s} {'Vote %':>8s} {'Seats':>7s} {'Seat %':>8s}")
    print("-" * 80)

    for party, seats in results['party_seats'].items():
        votes = party_votes[party]
        vote_pct = (votes / total_votes) * 100
        seat_pct = (seats / 10) * 100
        print(f"{party:10s} {votes:12,} {vote_pct:7.1f}% {seats:7d} {seat_pct:7.1f}%")

    print(f"\n{'Total':10s} {total_votes:12,} {'100.0%':>8s} {10:7d} {'100.0%':>8s}")

    # Display Stage 2 results
    print_header("STAGE 2: ELECTED CANDIDATES (sorted by preference votes)")

    for party in ['Party A', 'Party B', 'Party C']:
        print_section(f"{party} - Won {results['party_seats'][party]} seats")

        print(f"{'Candidate':12s} {'List Pos':>10s} {'Pref Votes':>12s} "
              f"{'Final Rank':>12s} {'Status':>12s}")
        print("-" * 80)

        # Get all candidates from this party, sorted by final rank
        party_candidates = [c for c in candidates if c._party == party]
        party_candidates.sort(key=lambda c: c.final_rank if c.final_rank else 999)

        for candidate in party_candidates:
            pref = candidate_votes.get(candidate._name, 0)
            status = "✓ ELECTED" if candidate.elected else ""
            rank = candidate.final_rank if candidate.final_rank else "-"

            # Mark candidates who jumped ahead of their list position
            jumped = ""
            if candidate.final_rank and candidate.final_rank < candidate._list_position:
                jumped = " ⬆️ JUMPED!"

            print(f"{candidate._name:12s} {candidate._list_position:10d} "
                  f"{pref:12,} {str(rank):>12s} {status:>12s}{jumped}")

    # Analysis
    print_header("ANALYSIS: The Power of Voter Preferences")

    jumpers = []
    for candidate in results['elected_candidates']:
        if candidate.final_rank < candidate._list_position:
            jumpers.append(candidate)

    print(f"\n🎯 {len(jumpers)} out of {len(results['elected_candidates'])} "
          f"elected candidates JUMPED ahead of their list position!")

    print("\nCandidate Jumps:")
    for candidate in jumpers:
        jump_size = candidate._list_position - candidate.final_rank
        print(f"  • {candidate._name:8s} ({candidate._party:8s}): "
              f"Position #{candidate._list_position} → Rank #{candidate.final_rank} "
              f"(jumped {jump_size} position{'s' if jump_size > 1 else ''})")

    print("\n" + "=" * 80)
    print("KEY INSIGHT: In pure open list PR, voters have COMPLETE control.")
    print("Party rankings are just suggestions - preference votes decide!")
    print("=" * 80)

    print("\nTry modifying candidate_votes in the code to see different results!")
    print("Or run 'jupyter notebook openlist_demo.ipynb' for interactive demo.")


if __name__ == '__main__':
    main()

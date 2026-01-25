#!/usr/bin/env python3
"""
Open List PR Visualization Tool

Creates visual charts showing:
1. Party seat allocation (pie chart + bar chart)
2. Candidate ranking changes (before/after comparison)
3. "Jump" analysis showing position changes
4. Preference vote distribution

Usage:
    python3 visualize_openlist.py
"""

import sys
sys.path.append('src')

from main import Candidate, OpenListPR
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np


def create_party_allocation_chart(party_votes, party_seats, total_seats):
    """Create side-by-side comparison of vote % vs seat %."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    parties = list(party_votes.keys())
    votes = list(party_votes.values())
    seats = [party_seats[p] for p in parties]

    total_votes = sum(votes)
    vote_pcts = [(v / total_votes) * 100 for v in votes]
    seat_pcts = [(s / total_seats) * 100 for s in seats]

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

    # Bar chart comparison
    x = np.arange(len(parties))
    width = 0.35

    bars1 = ax1.bar(x - width/2, vote_pcts, width, label='Vote %',
                    color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    bars2 = ax1.bar(x + width/2, seat_pcts, width, label='Seat %',
                    color=colors, alpha=1.0, edgecolor='black', linewidth=1.5)

    ax1.set_xlabel('Party', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Vote Share vs Seat Share', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(parties)
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_ylim(0, max(max(vote_pcts), max(seat_pcts)) * 1.1)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=9)

    # Pie chart for seats
    # Create autopct function that shows both seat count and percentage
    def make_autopct(seats_list):
        def autopct_func(pct):
            # Calculate which slice this is based on percentage
            total = sum(seats_list)
            val = int(round(pct * total / 100.0))
            return f'{val} seats\n({pct:.1f}%)'
        return autopct_func

    wedges, texts, autotexts = ax2.pie(seats, labels=parties, colors=colors,
                                         autopct=make_autopct(seats),
                                         startangle=90, explode=[0.05]*len(parties),
                                         textprops={'fontsize': 11, 'weight': 'bold'},
                                         wedgeprops={'edgecolor': 'black', 'linewidth': 2})

    ax2.set_title(f'Seat Distribution (Total: {total_seats} seats)',
                  fontsize=14, fontweight='bold')

    plt.tight_layout()
    return fig


def create_candidate_jump_visualization(candidates, candidate_votes, party):
    """Create before/after visualization showing candidate position jumps."""
    party_candidates = [c for c in candidates if c._party == party]
    party_candidates_sorted = sorted(party_candidates, key=lambda c: c.final_rank if c.final_rank else 999)

    fig, ax = plt.subplots(figsize=(12, 8))

    n_candidates = len(party_candidates_sorted)
    y_positions = np.arange(n_candidates) * 1.5

    colors_elected = '#4CAF50'
    colors_not_elected = '#CCCCCC'

    for i, candidate in enumerate(party_candidates_sorted):
        y = y_positions[i]

        # Determine color based on election status
        color = colors_elected if candidate.elected else colors_not_elected
        alpha = 1.0 if candidate.elected else 0.5

        # List position box (left side)
        list_box = FancyBboxPatch((0, y - 0.3), 2, 0.6,
                                   boxstyle="round,pad=0.1",
                                   edgecolor='black', facecolor='#FFE5B4',
                                   linewidth=2, alpha=0.8)
        ax.add_patch(list_box)
        ax.text(1, y, f'#{candidate._list_position}',
                ha='center', va='center', fontsize=12, fontweight='bold')

        # Candidate name
        ax.text(2.5, y, candidate._name,
                ha='left', va='center', fontsize=11, fontweight='bold')

        # Preference votes
        pref_votes = candidate_votes.get(candidate._name, 0)
        ax.text(5.5, y, f'{pref_votes:,} votes',
                ha='left', va='center', fontsize=10, color='#555')

        # Final rank box (right side)
        rank = candidate.final_rank if candidate.final_rank else '-'
        final_box = FancyBboxPatch((8, y - 0.3), 2, 0.6,
                                    boxstyle="round,pad=0.1",
                                    edgecolor='black', facecolor=color,
                                    linewidth=2, alpha=alpha)
        ax.add_patch(final_box)
        ax.text(9, y, f'#{rank}' if rank != '-' else '-',
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='white' if candidate.elected else 'black')

        # Draw arrow showing movement
        if candidate.final_rank and candidate.final_rank != candidate._list_position:
            arrow_color = '#FF5722' if candidate.final_rank < candidate._list_position else '#2196F3'

            # Calculate arrow position based on rank difference
            # Higher final rank (lower number) means upward arrow
            if candidate.final_rank < candidate._list_position:
                # Jumped up - show curved arrow
                arrow = FancyArrowPatch((2, y + 0.1), (8, y + 0.1),
                                       connectionstyle="arc3,rad=.3",
                                       arrowstyle='->,head_width=0.4,head_length=0.4',
                                       color=arrow_color, linewidth=3, alpha=0.7)
                ax.add_patch(arrow)

                # Jump indicator
                jump_size = candidate._list_position - candidate.final_rank
                ax.text(5, y + 0.6, f'⬆️ +{jump_size}',
                       ha='center', va='center', fontsize=10,
                       color=arrow_color, fontweight='bold')

    # Labels
    ax.text(1, n_candidates * 1.5 + 0.5, 'List Position\n(Party Ranking)',
            ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax.text(9, n_candidates * 1.5 + 0.5, 'Final Rank\n(After Votes)',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Legend
    elected_patch = mpatches.Patch(color=colors_elected, label='Elected')
    not_elected_patch = mpatches.Patch(color=colors_not_elected, label='Not Elected', alpha=0.5)
    ax.legend(handles=[elected_patch, not_elected_patch], loc='lower right', fontsize=10)

    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1, n_candidates * 1.5 + 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'{party}: Candidate Ranking Changes',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig


def create_preference_votes_chart(candidates, candidate_votes):
    """Create horizontal bar chart of preference votes by party."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))

    parties = ['Party A', 'Party B', 'Party C']
    colors_map = {'Party A': '#FF6B6B', 'Party B': '#4ECDC4', 'Party C': '#45B7D1'}

    for idx, (party, ax) in enumerate(zip(parties, axes)):
        party_candidates = sorted([c for c in candidates if c._party == party],
                                 key=lambda c: candidate_votes.get(c._name, 0),
                                 reverse=True)

        names = [c._name for c in party_candidates]
        votes = [candidate_votes.get(c._name, 0) for c in party_candidates]
        elected = [c.elected for c in party_candidates]

        # Color bars based on election status
        bar_colors = [colors_map[party] if e else '#CCCCCC' for e in elected]

        bars = ax.barh(names, votes, color=bar_colors, edgecolor='black', linewidth=1.5)

        # Add value labels
        for i, (bar, vote) in enumerate(zip(bars, votes)):
            width = bar.get_width()
            label = f'{vote:,}'
            if elected[i]:
                label += ' ✓'
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   label, ha='left', va='center', fontsize=9,
                   fontweight='bold' if elected[i] else 'normal',
                   color=colors_map[party] if elected[i] else '#666')

        ax.set_xlabel('Preference Votes', fontsize=10, fontweight='bold')
        ax.set_title(party, fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        ax.invert_yaxis()

        # Set consistent x-axis range
        ax.set_xlim(0, max(votes) * 1.15)

    plt.tight_layout()
    fig.suptitle('Preference Votes Distribution by Party',
                 fontsize=14, fontweight='bold', y=1.02)
    return fig


def main():
    """Run visualization demo."""
    print("=" * 80)
    print("OPEN LIST PR VISUALIZATION DEMO")
    print("=" * 80)
    print("\nGenerating visualizations...")

    # Create candidates
    candidates = [
        Candidate(name="Alice", party="Party A", list_position=1),
        Candidate(name="Bob", party="Party A", list_position=2),
        Candidate(name="Carol", party="Party A", list_position=3),
        Candidate(name="David", party="Party A", list_position=4),
        Candidate(name="Eve", party="Party A", list_position=5),

        Candidate(name="Frank", party="Party B", list_position=1),
        Candidate(name="Grace", party="Party B", list_position=2),
        Candidate(name="Henry", party="Party B", list_position=3),
        Candidate(name="Iris", party="Party B", list_position=4),

        Candidate(name="Jack", party="Party C", list_position=1),
        Candidate(name="Kate", party="Party C", list_position=2),
        Candidate(name="Leo", party="Party C", list_position=3),
    ]

    party_votes = {
        'Party A': 100000,
        'Party B': 80000,
        'Party C': 30000,
    }

    candidate_votes = {
        "Alice": 8000, "Bob": 35000, "Carol": 28000, "David": 15000, "Eve": 10000,
        "Frank": 25000, "Grace": 30000, "Henry": 15000, "Iris": 8000,
        "Jack": 5000, "Kate": 20000, "Leo": 3000,
    }

    # Run election
    election = OpenListPR(
        parties=['Party A', 'Party B', 'Party C'],
        candidates=candidates,
        party_votes=party_votes,
        candidate_votes=candidate_votes,
        total_seats=10,
        method='dhondt',
        ranking_variant='pure'
    )

    results = election.run_election()

    print("\n1. Creating party allocation chart...")
    fig1 = create_party_allocation_chart(party_votes, results['party_seats'], 10)
    fig1.savefig('party_allocation.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: party_allocation.png")

    print("\n2. Creating candidate jump visualizations...")
    for party in ['Party A', 'Party B', 'Party C']:
        fig = create_candidate_jump_visualization(candidates, candidate_votes, party)
        filename = f'candidate_jumps_{party.replace(" ", "_").lower()}.png'
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"   ✓ Saved: {filename}")

    print("\n3. Creating preference votes chart...")
    fig4 = create_preference_votes_chart(candidates, candidate_votes)
    fig4.savefig('preference_votes.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: preference_votes.png")

    print("\n" + "=" * 80)
    print("VISUALIZATION COMPLETE!")
    print("=" * 80)
    print("\nGenerated files:")
    print("  • party_allocation.png - Vote % vs Seat % comparison")
    print("  • candidate_jumps_party_a.png - Party A ranking changes")
    print("  • candidate_jumps_party_b.png - Party B ranking changes")
    print("  • candidate_jumps_party_c.png - Party C ranking changes")
    print("  • preference_votes.png - Preference vote distribution")
    print("\nThese visualizations show:")
    print("  ⬆️ Position jumps with arrows and indicators")
    print("  ✓ Elected candidates highlighted in green")
    print("  📊 Vote percentages vs seat percentages")
    print("=" * 80)

    # Note: plt.show() commented out - to view charts, open the PNG files
    # Uncomment the line below if you want interactive display:
    # plt.show()


if __name__ == '__main__':
    main()

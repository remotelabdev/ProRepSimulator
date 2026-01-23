"""
Proportional Representation Seat Allocation Simulator

This module implements two electoral seat allocation methods:
- D'Hondt method (favors larger parties)
- Sainte-Laguë method (more proportional, favors smaller parties)

Author: Neo
"""


class DHondt:
    """
    Implements the D'Hondt method for proportional seat allocation.

    The D'Hondt method divides each party's votes by (seats_allocated + 1)
    and awards seats sequentially to the party with the highest quotient.
    """

    def __init__(self, parties=None, votes=None, total_seats=None):
        """
        Initialize D'Hondt calculator.

        Args:
            parties: List of party names
            votes: Dictionary mapping party names to vote counts
            total_seats: Total number of seats to allocate
        """
        if parties:
            self._parties = parties
        if votes:
            self._votes = votes
        self._seat_allocation = {party: 0 for party in self._parties}
        if total_seats:
            self._total_seats = total_seats

    def sanity_check(self):
        """Validate that parties and votes data are consistent."""
        if len(self._parties) != len(self._votes):
            raise ValueError("the length of party list and vote dictionary mismatch")
        for party in self._parties:
            if party not in self._votes.keys():
                raise ValueError(f"{party} not having a vote")

    def _seat_allocating_helper(self, seat_allocation=None, total_seats=None):
        """
        Allocate a single seat using the D'Hondt quotient formula.

        Formula: quotient = votes / (seats_allocated + 1)
        Awards seat to party with highest quotient.
        """
        if total_seats is None:
            total_seats = self._total_seats
        if not seat_allocation:
            seat_allocation = self._seat_allocation

        # Calculate D'Hondt quotients for each party
        dhondt_vals = {}
        for party, seat_allocated in seat_allocation.items():
            vote_count = self._votes[party]
            quotient = vote_count / (seat_allocated + 1)
            dhondt_vals[party] = quotient

        # Find party with highest quotient
        sorted_dhondt_vals = sorted(dhondt_vals.items(), key=lambda item: item[1], reverse=True)
        winner_this_round = sorted_dhondt_vals[0][0]

        # Award seat to winner
        seat_allocation[winner_this_round] += 1

    def dhondt(self):
        """
        Execute the D'Hondt allocation algorithm.

        Allocates all seats by repeatedly calling _seat_allocating_helper()
        which awards one seat per iteration to the party with highest quotient.
        """
        self.sanity_check()
        for _ in range(self._total_seats):
            self._seat_allocating_helper()


class SatineLague:
    """
    Implements the Sainte-Laguë method for proportional seat allocation.

    The Sainte-Laguë method divides each party's votes by (2 * seats_allocated + 1)
    and awards seats sequentially to the party with the highest quotient.
    More proportional than D'Hondt, slightly favors smaller parties.
    """

    def __init__(self, parties=None, votes=None, total_seats=None):
        """
        Initialize Sainte-Laguë calculator.

        Args:
            parties: List of party names
            votes: Dictionary mapping party names to vote counts
            total_seats: Total number of seats to allocate
        """
        if parties:
            self._parties = parties
        if votes:
            self._votes = votes
        self._seat_allocation = {party: 0 for party in self._parties}
        if total_seats:
            self._total_seats = total_seats

    def sanity_check(self):
        """Validate that parties and votes data are consistent."""
        if len(self._parties) != len(self._votes):
            raise ValueError("the length of party list and vote dictionary mismatch")
        for party in self._parties:
            if party not in self._votes.keys():
                raise ValueError(f"{party} not having a vote")

    def _seat_allocating_helper(self, seat_allocation=None, total_seats=None):
        """
        Allocate a single seat using the Sainte-Laguë quotient formula.

        Formula: quotient = votes / (2 * seats_allocated + 1)
        Awards seat to party with highest quotient.
        """
        if total_seats is None:
            total_seats = self._total_seats
        if not seat_allocation:
            seat_allocation = self._seat_allocation

        # Calculate Sainte-Laguë quotients for each party
        satinelague_vals = {}
        for party, seat_allocated in seat_allocation.items():
            vote_count = self._votes[party]
            quotient = vote_count / (2 * seat_allocated + 1)
            satinelague_vals[party] = quotient

        # Find party with highest quotient
        sorted_satinelague_vals = sorted(satinelague_vals.items(), key=lambda item: item[1], reverse=True)
        winner_this_round = sorted_satinelague_vals[0][0]

        # Award seat to winner
        seat_allocation[winner_this_round] += 1

    def satinelague(self):
        """
        Execute the Sainte-Laguë allocation algorithm.

        Allocates all seats by repeatedly calling _seat_allocating_helper()
        which awards one seat per iteration to the party with highest quotient.
        """
        self.sanity_check()
        for _ in range(self._total_seats):
            self._seat_allocating_helper()


class CompareSeatAllocation:
    """
    Compare seat allocation results between different electoral methods.

    Runs both D'Hondt and Sainte-Laguë methods on the same election data
    and provides comparison analysis showing differences in seat allocation.
    """

    def __init__(self, method_label1='dhondt', method_label2='satinelague', params=None):
        """
        Initialize comparison framework.

        Args:
            method_label1: First method to compare (default: 'dhondt')
            method_label2: Second method to compare (default: 'satinelague')
            params: Election parameters (parties, votes, total_seats)
        """
        self._method_label1 = method_label1
        self._method_label2 = method_label2
        self._method_labels = {self._method_label1, self._method_label2}
        if params:
            self._params = params
        self._method_and_allocation = {}

    def run_calculations(self):
        """
        Run both allocation methods and store results.

        Returns:
            Dictionary mapping method names to their seat allocation results
        """
        method_and_allocation = {}
        if self._method_and_allocation:
            method_and_allocation = self._method_and_allocation

        for method_label in self._method_labels:
            if method_label == 'dhondt':
                dhondt = DHondt(**self._params)
                dhondt.dhondt()
                method_and_allocation['dhondt'] = dhondt._seat_allocation
            elif method_label == 'satine_lague':
                satinelague = SatineLague(**self._params)
                satinelague.satinelague()
                method_and_allocation['satine_lague'] = satinelague._seat_allocation

        self._method_and_allocation = method_and_allocation
        return method_and_allocation

    def get_comparison_results(self):
        """
        Transpose and compare results from both methods.

        Transforms data structure from:
            {'dhondt': {'Party A': 48, 'Party B': 38}, 'satine_lague': {...}}
        To:
            {'Party A': {'dhondt': 48, 'satine_lague': 47}, 'Party B': {...}}

        Returns:
            tuple: (party_and_allocation dict, diff_dict showing differences)
        """
        party_and_allocation = {}
        diff_dict = {}

        # Transpose: method->party->seats to party->method->seats
        for method, allocation in self._method_and_allocation.items():
            for party, seat in allocation.items():
                if party not in party_and_allocation:
                    party_and_allocation[party] = {}
                party_and_allocation[party][method] = seat

        # Compare seat allocations between methods
        for party, methods_seats in party_and_allocation.items():
            method_labels = list(methods_seats.keys())
            if len(method_labels) >= 2:
                seats1 = methods_seats[method_labels[0]]
                seats2 = methods_seats[method_labels[1]]
                if seats1 == seats2:
                    diff_dict[party] = 'not diff'
                else:
                    diff_dict[party] = f'diff: {method_labels[0]}={seats1}, {method_labels[1]}={seats2}'

        return party_and_allocation, diff_dict


# Example usage
if __name__ == '__main__':
    # Define election parameters
    params = {'parties': ['Party A', 'Party B', 'Party C'],
        'votes': {'Party A': 100000, 'Party B': 80000, 'Party C': 30000},
        'total_seats': 5,
    }

    # Override total_seats for larger election
    params_100 = {**params, 'total_seats': 100}

    # Run D'Hondt method
    dhondt = DHondt(**params_100)
    dhondt.dhondt()
    print("D'Hondt allocation:", dhondt._seat_allocation)

    # Run Sainte-Laguë method
    satinelague = SatineLague(**params_100)
    satinelague.satinelague()
    print("Sainte-Laguë allocation:", satinelague._seat_allocation)

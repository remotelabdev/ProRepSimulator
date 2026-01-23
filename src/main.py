# Removed 'import typing' - was unused throughout the code
class DHondt:
    def __init__(self, parties=None, votes=None, total_seats=None):  # Fixed: Added spaces after commas (PEP 8)
        # added optional total seats and initializing self._total_seats to fix bug 4 accordingly
        if parties:
            self._parties = parties
        if votes:
            self._votes = votes
        self._seat_allocation = {party: 0 for party in self._parties}  # Fixed: Added space after colon in dict comprehension
        if total_seats:
            self._total_seats = total_seats
    def sanity_check(self):
        if len(self._parties) != len(self._votes):
            raise ValueError("the length of party list and vote dictionary mismatch")
        for party in self._parties:
            if party not in self._votes.keys():
                raise ValueError(f"{party} not having a vote")
    def _seat_allocating_helper(self, seat_allocation=None, total_seats=None):  # Fixed: Added spaces after commas
        # BUG #4 (MAJOR): total_seats parameter is defined but never used!
        # TECHNICAL: The function allocates exactly one seat per invocation. Without iterating
        #            total_seats times, only one seat will ever be allocated.
        # VIVID: Imagine a chef who can only cook one dish at a time, but you never tell them
        #        how many dishes to cook. They make one and stop. That's this function!
        # FIX: Add a loop in the caller: for i in range(total_seats): self._seat_allocating_helper(...)
        if total_seats is None:
            total_seats = self._total_seats  # add them just to prepare future potential usage
        if not seat_allocation:
            seat_allocation = self._seat_allocation
        dhondt_vals = {}  # Renamed from dhondt_vals for clarity: stores quotient values for each party
        for party, seat_allocated in seat_allocation.items():  # Fixed: Added space after comma
            vote_count = self._votes[party]  # Renamed: vote_prop → vote_count (more accurate, it's total votes not proportion)
            # Why +1 in the denominator? Because we don't like to divide by zero,
            # and we guess you wouldn't either! 😉
            # (Seriously: it's dividing by "seats they'd have AFTER getting this one")
            quotient = vote_count / (seat_allocated + 1)  # Renamed: dhondt_val → quotient (standard terminology). Fixed: spaces around operators
            dhondt_vals[party] = quotient

        # BUG #2 (CRITICAL): Sorting in ascending order when we need descending!
        # TECHNICAL: D'Hondt method awards seats to the party with the HIGHEST quotient.
        #            sorted() defaults to ascending order (smallest first), so sorted_dhondt_vals[0]
        #            gives us the LOSER, not the winner.
        # VIVID: It's like running a race backwards - you're crowning the slowest runner!
        # FIX: sorted(..., reverse=True) to get highest values first
        # sorted_dhondt_vals = sorted(dhondt_vals.items(), key=lambda item: item[1])
        sorted_dhondt_vals = sorted(dhondt_vals.items(), key=lambda item: item[1], reverse=True)  # Fixed: Added spaces after commas

        # BUG #1 (CRITICAL): Can't call .keys() on a list!
        # TECHNICAL: sorted() returns List[Tuple[str, float]], not Dict. Attempting .keys()
        #            raises AttributeError at runtime.
        # VIVID: You ordered a sandwich (list of tuples) but you're trying to use it like
        #        a filing cabinet (dict). The sandwich doesn't have drawers!
        # FIX: sorted_dhondt_vals[0][0] to access first tuple's first element (the party name)
        # winner_this_round = sorted_dhondt_vals.keys()[0]
        winner_this_round = sorted_dhondt_vals[0][0]  # my fix for bug #1

        seat_allocation[winner_this_round] += 1

        # BUG #3 (CRITICAL): Double increment - awarding 2 seats instead of 1!
        # TECHNICAL: Line 25 already incremented seat_allocation[winner]. This conditional
        #            (which always evaluates True since self._seat_allocation is a non-empty dict)
        #            increments AGAIN, giving 2 seats per allocation round.
        # VIVID: You're giving the winner their trophy (line 25), then saying "oh wait, here's
        #        ANOTHER trophy!" (line 27). They end up with double the prize!
        # FIX: Delete these two lines entirely
        # if self._seat_allocation:
            # seat_allocation[winner_this_round] += 1  # my fix for bug #3, but I wrote the buggy line because of confusion between tracking of two instances self._seat_allocation and seat_allocation




    def dhondt(self):
        self.sanity_check()
        # Removed: sorted_votes was calculated but never used in the algorithm

        # BUG #5 (CRITICAL): Same .keys() mistake as Bug #1, plus empty loop body!
        # TECHNICAL: sorted() returns List[Tuple[str, int]], not Dict. Cannot call .keys().
        #            Additionally, loop body contains only 'pass' - no actual logic implemented.
        # VIVID: You've built a merry-go-round (the loop), but:
        #        1) You're trying to read the instruction manual from a sandwich (wrong type)
        #        2) Even if it worked, the ride does nothing - no horses, no music!
        # FIX: Two options:
        #      Option A: for party, votes in sorted_votes:  (if you need to iterate)
        #      Option B: Delete this loop entirely and call _seat_allocating_helper() instead
        #      Note: The D'Hondt algorithm doesn't actually need pre-sorted votes for the main loop!
        # for party in sorted_votes.keys():
            # pass
        for _ in range(self._total_seats):  # oh, I get it when fixing bug #4, I would like iterate by the total seats
            self._seat_allocating_helper()  # my fix for bug #5, but how to call the helper properly?

class SatineLague:
    def __init__(self, parties=None, votes=None, total_seats=None):  # Fixed: Added spaces after commas
        # added optional total seats and initializing self._total_seats to fix bug 4 accordingly
        if parties:
            self._parties = parties
            # Removed debug print: print(f'parties = {parties}')
        if votes:
            self._votes = votes
            # Removed debug print: print(f'votes = {votes}')
        self._seat_allocation = {party: 0 for party in self._parties}  # Fixed: Added space after colon in dict comprehension
        # Removed debug print: print(f'self._seat_allocation = {self._seat_allocation}')  # Also fixed typo in comment: allcoation → allocation
        if total_seats:
            self._total_seats = total_seats
            # Removed debug print: print(f'total_seats={total_seats}')
    def sanity_check(self):
        # Removed debug print: print('sanity check start')
        if len(self._parties) != len(self._votes):
            raise ValueError("the length of party list and vote dictionary mismatch")
        for party in self._parties:
            if party not in self._votes.keys():
                raise ValueError(f"{party} not having a vote")
    def _seat_allocating_helper(self, seat_allocation=None, total_seats=None):  # Fixed: Added spaces after commas
        # Removed debug print: print('self._seat_allocating_helper working')
        if total_seats is None:
            total_seats = self._total_seats
        if not seat_allocation:
            seat_allocation = self._seat_allocation
        satinelague_vals = {}
        for party, seat_allocated in seat_allocation.items():  # Fixed: Added space after comma
            # Removed debug print: print('allocation loop starts')
            vote_count = self._votes[party]  # Renamed: vote_prop → vote_count (consistent with DHondt class)
            # Why +1 in the denominator? Because we don't like to divide by zero,
            # and we guess you wouldn't either! 😉
            # (Seriously: it's dividing by "seats they'd have AFTER getting this one")
            quotient = vote_count / (2 * seat_allocated + 1)  # Renamed: satinelague_val → quotient. Fixed: spaces around operators
            satinelague_vals[party] = quotient

        sorted_satinelague_vals = sorted(satinelague_vals.items(), key=lambda item: item[1], reverse=True)  # Fixed: Added spaces after commas

        winner_this_round = sorted_satinelague_vals[0][0]

        seat_allocation[winner_this_round] += 1

    def satinelague(self):
        self.sanity_check()
        # Removed: sorted_votes was calculated but never used in the algorithm

        for _ in range(self._total_seats):
            self._seat_allocating_helper()
class CompareSeatAllocation:
    def __init__(self, method_label1='dhondt', method_label2='satinelague', params=None):  # Fixed: Added spaces after commas and around =
        self._method_label1 = method_label1  # Fixed: Added spaces around =
        self._method_label2 = method_label2  # Fixed: Added spaces around =
        self._method_labels = {self._method_label1, self._method_label2}  # Fixed: Added space after comma
        if params:
            self._params = params
        self._method_and_allocation = {}
    def run_calculations(self):  # Renamed: call() → run_calculations() (more descriptive of what it does)
        # Refactored: Use **self._params to unpack parameters for both methods
        # This makes the comparison flexible and reusable with any election scenario
        # Previously hardcoded params for prototype, now properly using **self._params
        method_and_allocation = {}
        if self._method_and_allocation:
            method_and_allocation = self._method_and_allocation

        for method_label in self._method_labels:
            if method_label == 'dhondt':
                dhondt = DHondt(**self._params)  # Now uses **self._params instead of hardcoded values
                dhondt.dhondt()
                method_and_allocation['dhondt'] = dhondt._seat_allocation
            elif method_label == 'satine_lague':
                # BUG #6 (CRITICAL): Indentation error - lines below are outside elif block!
                # TECHNICAL: Lines 174-175 are not indented under the elif, so they execute
                #            regardless of which method_label is being processed. This causes
                #            NameError when method_label == 'dhondt' (satinelague not defined).
                # VIVID: It's like having a recipe that says "if making pasta, boil water"
                #        but then "drain the noodles" is written at the margin, so you try to
                #        drain noodles even when making a salad! Indentation = scope!
                # FIX: Indent lines 174-175 to match the dhondt block above (4 extra spaces)
                satinelague = SatineLague(**self._params)  # my fix of bug #6 indentation problem, now also uses **self._params
                satinelague.satinelague()
                method_and_allocation['satine_lague'] = satinelague._seat_allocation  # my fix for bug #8, changed 'satinelague' to satine_lague for consistency

        # BUG #7 (MAJOR): call() doesn't save or return results!
        # TECHNICAL: method_and_allocation is a local variable that gets discarded when the
        #            function ends. self._method_and_allocation remains empty, so compare()
        #            will have no data to work with.
        # VIVID: You're cooking a big meal, plating it beautifully... then throwing it away
        #        before anyone can eat it! All that work, but nothing saved.
        # FIX: Add these lines before the function ends:
        #      self._method_and_allocation = method_and_allocation
        #      return method_and_allocation
        self._method_and_allocation = method_and_allocation
        return method_and_allocation  # my fix of bug #7, added saved local method_and_allocation to self._method_and_allocation instance properly and returns it
        # BUG #8 (MINOR): String inconsistency 'satine_lague' vs 'satinelague'
        # TECHNICAL: Line 168 checks for 'satine_lague' (with underscore) but line 175 uses
        #            'satinelague' (no underscore) as the dict key. The elif will never match.
        # VIVID: You're checking if someone's name is "John-Smith" but then calling them
        #        "JohnSmith" - they won't respond! Pick one spelling and stick with it.
        # FIX: Use consistent spelling throughout (recommend 'satinelague' or 'sainte_lague')

    def get_comparison_results(self):  # Renamed: compare() → get_comparison_results() (clearer about return value)
        # GOAL: Transpose/pivot the data structure from method->party->seats to party->method->seats
        # Current structure: {'dhondt': {'Party A': 48, 'Party B': 38}, 'satinelague': {...}}
        # Desired structure: {'Party A': {'dhondt': 48, 'satinelague': 47}, 'Party B': {...}}
        # This is like swapping rows and columns in a matrix!

        party_and_allocation = {}
        diff_dict = {}

        # BUG #9 (CRITICAL): Missing parentheses on .items()
        # TECHNICAL: .items is a method reference, not the actual items. You need .items()
        #            to call it and get the key-value pairs. Without (), you get a TypeError.
        # VIVID: It's like asking for someone's phone number but getting their phone book
        #        instead of actually opening it. You need the () to "open" the method!
        # FIX: Change to self._method_and_allocation.items()
        for method, allocation in self._method_and_allocation.items():  # my fix on bug #9, added parentheses on .items(). Fixed: Added spaces after commas

            # BUG #10 (CRITICAL): Wrong unpacking - allocation is a dict, not a list!
            # TECHNICAL: allocation = {'Party A': 48, 'Party B': 38, ...} (a dict)
            #            You can't do allocation[0] or allocation[1] on a dict - those are
            #            list/tuple operations. You need to iterate: for party, seat in allocation.items()
            # VIVID: You're trying to get the "first" item from a bag of labeled marbles.
            #        Dicts don't have "first" or "second" - they have keys! You need to ask
            #        "which marble label?" not "which position?"
            # FIX: This whole loop should be:
            #      for method, allocation in self._method_and_allocation.items():
            #          for party, seat in allocation.items():
            #              if party not in party_and_allocation:
            #                  party_and_allocation[party] = {}
            #              party_and_allocation[party][method] = seat
            # party, seat = allocation[0], allocation[1]
            for method, allocation in self._method_and_allocation.items():  # Fixed: Added spaces after commas
                for party, seat in allocation.items():  # Fixed: Added spaces after commas
                    if party not in party_and_allocation:
                        party_and_allocation[party] = {}
                    party_and_allocation[party][method] = seat  # my fix on bug #10, I noticed I need something like transposing in matrices for the dicts, but initially struggled with syntax, current worked

        # BUG #13 (CRITICAL): Leftover tuple-based comparison logic after transpose
        # TECHNICAL: Lines 234-238 successfully create party_and_allocation as:
        #            {'Party A': {'dhondt': 48, 'satine_lague': 95}, ...}
        #            But this comparison code expects the OLD tuple structure:
        #            {'Party A': (48, 'dhondt'), ...}
        #            Trying to use [0] indexing on a dict causes KeyError.
        # VIVID: You successfully renovated your filing cabinet to use labeled folders (dict),
        #        but this code still tries to grab "the first item" as if they were stacks
        #        of papers (tuple). You're asking "give me drawer [0]" when drawers have
        #        names like 'dhondt', not positions!
        # FIX: Rewrite to compare the two methods' seat counts within the dict structure
        for party, methods_seats in party_and_allocation.items():
            # methods_seats is now {'dhondt': 48, 'satine_lague': 95}
            # We need to compare the two method results
            method_labels = list(methods_seats.keys())
            if len(method_labels) >= 2:
                seats1 = methods_seats[method_labels[0]]
                seats2 = methods_seats[method_labels[1]]
                if seats1 == seats2:
                    diff_dict[party] = 'not diff'
                else:
                    diff_dict[party] = f'diff: {method_labels[0]}={seats1}, {method_labels[1]}={seats2}'

        return party_and_allocation, diff_dict  # Fixed: Added space after comma


            

            

params = {'parties': ['Party A', 'Party B', 'Party C'],  # Fixed: Added spaces after colons and commas
    'votes': {'Party A': 100000, 'Party B': 80000, 'Party C': 30000},  # Fixed: Added spaces after colons and commas
    'total_seats': 5,  # Fixed: Added space after colon

}

# BUG #12 (MINOR): **params unpacking attempts but params has wrong total_seats!
# TECHNICAL: The **params syntax DOES work, but params defines total_seats=5 while
#            you want 100 seats. When you tried **params, it gave you 5 seats instead of 100,
#            so you commented it out and went back to explicit parameters.
# VIVID: You prepared a recipe card (params) with "bake for 5 minutes" but you actually
#        want to bake for 100 minutes. The ** spreading works fine, but the recipe is wrong!
# FIX: Either update params to total_seats=100, OR create a separate variable:
#      params_100 = {**params, 'total_seats': 100}  # Copy params but override total_seats
# NOTE: **params unpacking syntax is CORRECT and works perfectly! Example below:

# Using **params (this works! Just uses total_seats=5 from params dict):
# dhondt = DHondt(**params)

# If you want 100 seats, update the dict first:
params_100 = {**params, 'total_seats': 100}  # Override total_seats
# bug #12 fixed, the unpacking and overriding is like having a ready to modify boilerplate, it makes work lighter.

dhondt = DHondt(**params_100)  # Now this uses total_seats=100!
dhondt.dhondt()
print(dhondt._seat_allocation)

satinelague = SatineLague(**params_100)  # Same params, reused!
satinelague.satinelague()
print(satinelague._seat_allocation)

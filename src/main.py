import typing
class DHondt:
    def __init__(self,parties=None,votes=None,total_seats=None):
        #added optional total seats and initialzing self._total_seats to fix bug 4 accordingly
        if parties:
            self._parties = parties
        if votes:
            self._votes = votes
        self._seat_allocation = {party:0 for party in self._parties}
        if total_seats:
            self._total_seats = total_seats
    def sanity_check(self):
        if len(self._parties) != len(self._votes):
            raise ValueError("the length of party list and vote dictionary mismatch")
        for party in self._parties:
            if party not in self._votes.keys():
                raise ValueError(f"{party} not having a vote")
    def _seat_allocating_helper(self,seat_allocation=None,total_seats=None):
        # BUG #4 (MAJOR): total_seats parameter is defined but never used!
        # TECHNICAL: The function allocates exactly one seat per invocation. Without iterating
        #            total_seats times, only one seat will ever be allocated.
        # VIVID: Imagine a chef who can only cook one dish at a time, but you never tell them
        #        how many dishes to cook. They make one and stop. That's this function!
        # FIX: Add a loop in the caller: for i in range(total_seats): self._seat_allocating_helper(...)
        if total_seats is None:
            total_seats = self._total_seats#add them just to prepare future potential usage
        if not seat_allocation:
            seat_allocation = self._seat_allocation
        dhondt_vals = {}
        for party,seat_allocated in seat_allocation.items():
            vote_prop = self._votes[party]
            # Why +1 in the denominator? Because we don't like to divide by zero,
            # and we guess you wouldn't either! 😉
            # (Seriously: it's dividing by "seats they'd have AFTER getting this one")
            dhondt_val = vote_prop /( seat_allocated + 1 )
            dhondt_vals[party] = dhondt_val

        # BUG #2 (CRITICAL): Sorting in ascending order when we need descending!
        # TECHNICAL: D'Hondt method awards seats to the party with the HIGHEST quotient.
        #            sorted() defaults to ascending order (smallest first), so sorted_dhondt_vals[0]
        #            gives us the LOSER, not the winner.
        # VIVID: It's like running a race backwards - you're crowning the slowest runner!
        # FIX: sorted(..., reverse=True) to get highest values first
        #sorted_dhondt_vals = sorted(dhondt_vals.items(),key=lambda item: item[1])
        sorted_dhondt_vals = sorted(dhondt_vals.items(),key=lambda item: item[1],reverse=True)

        # BUG #1 (CRITICAL): Can't call .keys() on a list!
        # TECHNICAL: sorted() returns List[Tuple[str, float]], not Dict. Attempting .keys()
        #            raises AttributeError at runtime.
        # VIVID: You ordered a sandwich (list of tuples) but you're trying to use it like
        #        a filing cabinet (dict). The sandwich doesn't have drawers!
        # FIX: sorted_dhondt_vals[0][0] to access first tuple's first element (the party name)
        #winner_this_round = sorted_dhondt_vals.keys()[0]
        winner_this_round = sorted_dhondt_vals[0][0]#my fix for bug #1

        seat_allocation[winner_this_round] += 1

        # BUG #3 (CRITICAL): Double increment - awarding 2 seats instead of 1!
        # TECHNICAL: Line 25 already incremented seat_allocation[winner]. This conditional
        #            (which always evaluates True since self._seat_allocation is a non-empty dict)
        #            increments AGAIN, giving 2 seats per allocation round.
        # VIVID: You're giving the winner their trophy (line 25), then saying "oh wait, here's
        #        ANOTHER trophy!" (line 27). They end up with double the prize!
        # FIX: Delete these two lines entirely
        #if self._seat_allocation:
            #seat_allocation[winner_this_round] += 1 #my fix for bug #3,but I wrote the buggy line because of confusion between tracking of  two instances self._seat_allocation and sear_allocation



                
    def dhondt(self):
        self.sanity_check()
        sorted_votes = sorted(self._votes.items(),key=lambda item:item[1])

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
        #for party in sorted_votes.keys():
            #pass 
        for _ in range(self._total_seats):#oh,I get it when fixing bug #4,I would like iterate by the total seats
            self._seat_allocating_helper()#my fix for bug#5,but how to call the helper properly?

    
            
dhondt = DHondt(
    parties=['Party A','Party B','Party C'],
    votes={'Party A':100000,'Party B':80000,'Party C':30000},
    total_seats=100,
)
dhondt.dhondt()
print(dhondt._seat_allocation)
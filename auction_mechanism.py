#!/usr/bin/env python3
"""VCG auction — truthful mechanism for combinatorial auctions."""
from itertools import combinations

def vcg_auction(n_items, bids):
    """bids = {bidder: {frozenset(items): value}}. Returns allocation + payments."""
    bidders = list(bids.keys())
    items = list(range(n_items))
    # Find optimal allocation
    def optimal(exclude=None):
        best_val = 0; best_alloc = {}
        # Enumerate all partitions (simplified for small instances)
        active = [b for b in bidders if b != exclude]
        def search(remaining, alloc, val):
            nonlocal best_val, best_alloc
            if val > best_val: best_val = val; best_alloc = dict(alloc)
            for b in active:
                if b in alloc: continue
                for bundle, v in bids[b].items():
                    if bundle.issubset(remaining):
                        alloc[b] = bundle
                        search(remaining - bundle, alloc, val + v)
                        del alloc[b]
        search(frozenset(items), {}, 0)
        return best_val, best_alloc
    total_val, allocation = optimal()
    payments = {}
    for b in bidders:
        if b in allocation:
            val_without = optimal(exclude=b)[0]
            others_with = total_val - bids[b].get(allocation[b], 0)
            payments[b] = val_without - others_with
        else: payments[b] = 0
    return allocation, payments

def main():
    bids = {"A": {frozenset([0]): 5, frozenset([1]): 3},
            "B": {frozenset([0]): 3, frozenset([1]): 4},
            "C": {frozenset([0,1]): 7}}
    alloc, pay = vcg_auction(2, bids)
    print(f"Allocation: {alloc}")
    print(f"Payments: {pay}")

if __name__ == "__main__": main()

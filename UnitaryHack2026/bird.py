"""
bird.py
-------
Defines the Bird class: the game piece for Cluck & Crow.

Each Bird has three "feather genes" (a, b, c), each of which can be:
    True   -> Hen-feather   (golden/cream)
    False  -> Crow-feather  (deep indigo)
    None   -> unexpressed (not yet determined)

A bird's overall species (hen or crow) is decided by majority vote of its
expressed genes. Ties are broken randomly. This mirrors the original
cow-breeding game's logic, just re-themed and cleaned up.
"""

import itertools
from random import choice


class Bird:
    """A single hen or crow on the farm, with three feather genes."""

    _id_counter = itertools.count()

    def __init__(self, species: bool, a=None, b=None, c=None):
        """
        species: True  = Hen (player's side)
                  False = Crow (Quantum AI's side)
        a, b, c: feather genes, each True/False/None
        """
        self.species = species          # which team this bird ultimately is
        self.side = species             # which COOP (field half) it currently stands on
        self.genes = {"a": a, "b": b, "c": c}
        self.id = next(Bird._id_counter)
        self.age = 0

    def breed(self, other: "Bird") -> "Bird":
        """
        Combine this bird's genes with another's to create a chick.
        For each gene slot: if only one parent has it expressed, the chick
        inherits it. If both have it expressed, the chick randomly inherits
        one parent's version. If neither has it, it stays unexpressed.
        """
        chick = Bird(self.species)
        for gene in self.genes:
            mine, theirs = self.genes[gene], other.genes[gene]
            if mine is not None and theirs is None:
                chick.genes[gene] = mine
            elif mine is None and theirs is not None:
                chick.genes[gene] = theirs
            elif mine is not None and theirs is not None:
                chick.genes[gene] = choice([mine, theirs])
            # else both None -> stays None

        # Majority vote on expressed genes decides species; ties favor self's species
        tally = {True: 0, False: 0}
        for value in chick.genes.values():
            if value is not None:
                tally[value] += 1
        chick.species = self.species if tally[True] == tally[False] else (tally[True] > tally[False])
        chick.side = self.side
        return chick

    def move(self):
        """Cross to the opposite side of the farm."""
        self.side = not self.side

    def describe(self) -> str:
        species_name = "Hen" if self.species else "Crow"
        gene_str = "".join(
            "H" if v is True else "C" if v is False else "_" for v in self.genes.values()
        )
        return f"Bird#{self.id} [{species_name}] genes={gene_str} side={'Hen-coop' if self.side else 'Crow-coop'} age={self.age}"

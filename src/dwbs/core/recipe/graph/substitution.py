from typing import Dict, List, Tuple, Set, Optional
from ...contracts.inventory import ItemIdentity

class SubstitutionGraph:
    """
    D2.1 Ingredient Substitution Graph
    Manages a directed graph where edges represent valid substitutions.
    Edge (A -> B) means "If you need A, you can use B".
    """
    def __init__(self):
        # Adjacency list: Item -> List of (Substitute, Penalty)
        self._adj: Dict[ItemIdentity, List[Tuple[ItemIdentity, float]]] = {}

    def add_substitution(self, original: ItemIdentity, substitute: ItemIdentity, penalty: float):
        """
        Adds a substitution rule.
        :param original: The item called for in the recipe.
        :param substitute: The item that can be used instead.
        :param penalty: The cost/penalty of this substitution (must be non-negative).
        """
        if penalty < 0:
            raise ValueError("Penalty cannot be negative")

        if original == substitute:
            return # No-op

        # Cycle detection: Check if adding Original -> Substitute creates a cycle
        # A cycle exists if there is already a path from Substitute -> Original
        if self._path_exists(substitute, original):
             raise ValueError(f"Cycle detected: {substitute.full_name()} already leads to {original.full_name()}")

        if original not in self._adj:
            self._adj[original] = []

        # Check if already exists to update penalty? Or allow multiples?
        # We'll just append for now, simpler. Or overwrite if exact match.
        for i, (existing_sub, _) in enumerate(self._adj[original]):
            if existing_sub == substitute:
                # Update penalty
                self._adj[original][i] = (substitute, penalty)
                return

        self._adj[original].append((substitute, penalty))

    def get_substitutes(self, item: ItemIdentity) -> List[Tuple[ItemIdentity, float]]:
        """
        Returns all valid substitutes for the given item, including transitive ones.
        Returns list of (SubstituteItem, TotalPenalty).
        """
        substitutes = []
        # Use Dijkstra-like approach to find shortest paths (min penalty)
        import heapq

        # Priority queue: (penalty, item_wrapper)
        # We need a wrapper because ItemIdentity comparison in tuple might fail if penalties equal?
        # Actually Pydantic models are comparable.

        # We use a simple counter to break ties to avoid comparing items
        import itertools
        counter = itertools.count()

        pq = [(0.0, next(counter), item)]
        min_penalties: Dict[ItemIdentity, float] = {item: 0.0}

        while pq:
            current_penalty, _, current_item = heapq.heappop(pq)

            if current_penalty > min_penalties.get(current_item, float('inf')):
                continue

            if current_item != item:
                substitutes.append((current_item, current_penalty))

            for neighbor, weight in self._adj.get(current_item, []):
                new_penalty = current_penalty + weight
                if new_penalty < min_penalties.get(neighbor, float('inf')):
                    min_penalties[neighbor] = new_penalty
                    heapq.heappush(pq, (new_penalty, next(counter), neighbor))

        return substitutes

    def _path_exists(self, start: ItemIdentity, end: ItemIdentity) -> bool:
        visited = set()
        stack = [start]
        while stack:
            curr = stack.pop()
            if curr == end:
                return True
            if curr in visited:
                continue
            visited.add(curr)
            for neighbor, _ in self._adj.get(curr, []):
                stack.append(neighbor)
        return False

import pytest
from datetime import date, timedelta
from dwbs.core.recipe.domain.feasibility import FeasibilityChecker
from dwbs.core.recipe.domain.recipe import Recipe
from dwbs.core.recipe.domain.ingredient import IngredientRef
from dwbs.core.recipe.graph.substitution import SubstitutionGraph
from dwbs.core.contracts.inventory import InventoryState, InventoryItem, ItemIdentity, Quantity, Unit, StockStatus

# Helpers
def make_item(name, qty_val, unit=Unit.GRAM, expiry_date=None, status=StockStatus.IN_STOCK):
    return InventoryItem(
        item=ItemIdentity(name=name),
        quantity=Quantity(value=qty_val, unit=unit),
        expiry_date=expiry_date,
        status=status
    )

def make_recipe(ingredients):
    return Recipe(
        id="r1",
        name="Test Recipe",
        ingredients=ingredients,
        instructions=[]
    )

def test_exact_match():
    # Recipe needs 100g Tomato
    tomato = ItemIdentity(name="Tomato")
    req = IngredientRef(item=tomato, quantity=Quantity(value=100, unit=Unit.GRAM))
    recipe = make_recipe([req])

    # Inventory has 150g Tomato
    inv_item = make_item("Tomato", 150)
    inventory = InventoryState(items=[inv_item])

    checker = FeasibilityChecker()
    assert checker.can_cook(recipe, inventory) is True

def test_insufficient_quantity():
    # Recipe needs 100g Tomato
    tomato = ItemIdentity(name="Tomato")
    req = IngredientRef(item=tomato, quantity=Quantity(value=100, unit=Unit.GRAM))
    recipe = make_recipe([req])

    # Inventory has 50g Tomato
    inv_item = make_item("Tomato", 50)
    inventory = InventoryState(items=[inv_item])

    checker = FeasibilityChecker()
    assert checker.can_cook(recipe, inventory) is False

def test_missing_item():
    tomato = ItemIdentity(name="Tomato")
    req = IngredientRef(item=tomato, quantity=Quantity(value=100, unit=Unit.GRAM))
    recipe = make_recipe([req])

    # Inventory has Onion
    inv_item = make_item("Onion", 500)
    inventory = InventoryState(items=[inv_item])

    checker = FeasibilityChecker()
    assert checker.can_cook(recipe, inventory) is False

def test_substitution():
    # Recipe needs 100g Sour Cream
    sour_cream = ItemIdentity(name="Sour Cream")
    req = IngredientRef(item=sour_cream, quantity=Quantity(value=100, unit=Unit.GRAM))
    recipe = make_recipe([req])

    # Inventory has 200g Greek Yogurt
    yogurt_id = ItemIdentity(name="Greek Yogurt")
    inv_item = InventoryItem(item=yogurt_id, quantity=Quantity(value=200, unit=Unit.GRAM), status=StockStatus.IN_STOCK)
    inventory = InventoryState(items=[inv_item])

    # Graph: Greek Yogurt replaces Sour Cream
    graph = SubstitutionGraph()
    # Need Sour Cream -> Use Greek Yogurt
    graph.add_substitution(sour_cream, yogurt_id, 0.5)

    checker = FeasibilityChecker(substitution_graph=graph)
    assert checker.can_cook(recipe, inventory) is True

def test_expired_item_ignored():
    tomato = ItemIdentity(name="Tomato")
    req = IngredientRef(item=tomato, quantity=Quantity(value=100, unit=Unit.GRAM))
    recipe = make_recipe([req])

    # Inventory has 200g Tomato but EXPIRED
    inv_item = make_item("Tomato", 200, expiry_date=date.today() - timedelta(days=1))

    inventory = InventoryState(items=[inv_item])

    checker = FeasibilityChecker()
    assert checker.can_cook(recipe, inventory) is False

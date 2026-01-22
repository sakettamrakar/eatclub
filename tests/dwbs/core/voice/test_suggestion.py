import pytest
from src.dwbs.core.recipe.domain.recipe import Recipe
from src.dwbs.core.voice.generation.suggestion_formatter import SpokenSuggestionFormatter

class TestSpokenSuggestionFormatter:
    def setup_method(self):
        self.formatter = SpokenSuggestionFormatter()

    def create_recipe(self, name: str) -> Recipe:
        return Recipe(id="1", name=name, ingredients=[], instructions=[])

    def test_no_suggestions(self):
        text = self.formatter.format_suggestions([])
        assert text == "I don't have any recipe suggestions right now."

    def test_one_suggestion(self):
        recipes = [self.create_recipe("Pizza")]
        text = self.formatter.format_suggestions(recipes)
        assert text == "You could cook Pizza."

    def test_two_suggestions(self):
        recipes = [self.create_recipe("Pizza"), self.create_recipe("Soup")]
        text = self.formatter.format_suggestions(recipes)
        assert text == "You could cook Pizza or Soup."

    def test_three_suggestions(self):
        recipes = [
            self.create_recipe("Pizza"),
            self.create_recipe("Soup"),
            self.create_recipe("Salad")
        ]
        text = self.formatter.format_suggestions(recipes)
        assert text == "You could cook Pizza, Soup, or Salad."

    def test_more_than_three_suggestions(self):
        recipes = [
            self.create_recipe("Pizza"),
            self.create_recipe("Soup"),
            self.create_recipe("Salad"),
            self.create_recipe("Cake")
        ]
        text = self.formatter.format_suggestions(recipes)
        assert "Cake" not in text
        assert "Pizza, Soup, or Salad" in text

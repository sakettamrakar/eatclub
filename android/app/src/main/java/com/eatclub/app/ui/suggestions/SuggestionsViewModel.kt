package com.eatclub.app.ui.suggestions

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.eatclub.app.core.decision.RecipeScorer
import com.eatclub.app.core.domain.Recipe
import com.eatclub.app.core.ledger.InventoryRepository
import kotlinx.coroutines.launch

class SuggestionsViewModel(
    private val repository: InventoryRepository,
    private val scorer: RecipeScorer = RecipeScorer()
) : ViewModel() {

    private val _suggestions = MutableLiveData<List<Pair<Recipe, Double>>>()
    val suggestions: LiveData<List<Pair<Recipe, Double>>> = _suggestions

    // Mock Recipe Database for Phase 1
    private val allRecipes = listOf(
        Recipe("1", "Tomato Soup", "Delicious soup", emptyList(), 10, 20),
        Recipe("2", "Salad", "Healthy salad", emptyList(), 5, 0)
    )

    fun refreshSuggestions() {
        viewModelScope.launch {
            val inventory = repository.getInventoryState()
            val scored = allRecipes.map { recipe ->
                recipe to scorer.score(recipe, inventory)
            }.sortedByDescending { it.second }
            
            _suggestions.postValue(scored)
        }
    }
}

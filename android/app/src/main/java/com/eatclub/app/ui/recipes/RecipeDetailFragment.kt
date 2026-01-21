package com.eatclub.app.ui.recipes

import android.os.Bundle
import android.view.View
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import com.eatclub.app.R
import com.eatclub.app.core.domain.Recipe
import com.eatclub.app.databinding.FragmentRecipeDetailBinding

class RecipeDetailFragment : Fragment(R.layout.fragment_recipe_detail) {
    
    // In a real app, args would pass the Recipe ID, and ViewModel retrieves it
    // For Phase 1 demo, we might mock or look it up from static list
    private var _binding: FragmentRecipeDetailBinding? = null
    private val binding get() = _binding!!

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentRecipeDetailBinding.bind(view)
        
        // Mock data binding
        val mockRecipe = Recipe("1", "Tomato Soup", "Delicious soup", emptyList(), 10, 20)
        bindRecipe(mockRecipe)
    }
    
    private fun bindRecipe(recipe: Recipe) {
        binding.recipeTitle.text = recipe.title
        binding.recipeDescription.text = recipe.description
        binding.prepTime.text = "${recipe.prepTimeMinutes} min prep"
        binding.cookTime.text = "${recipe.cookTimeMinutes} min cook"
        
        // Ingredients logic would go here: iterate and add Views
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

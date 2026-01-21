package com.eatclub.app.core.decision

import com.eatclub.app.core.domain.*
import java.math.BigDecimal

class RecipeScorer {
    
    // D3.1/3.2/3.3 Ported Logic
    fun score(recipe: Recipe, inventory: List<InventoryItem>): Double {
        var score = 1.0
        
        // 1. Feasibility Check
        val missingIngredients = getMissingIngredients(recipe, inventory)
        if (missingIngredients.isNotEmpty()) {
            return 0.0 // Hard rule for now
        }
        
        // 2. Confidence Weighting (lowest confidence ingredient drags down score)
        val lowestConfidence = recipe.ingredients.minOfOrNull { ingredient ->
             findInInventory(ingredient.item, inventory)?.item?.confidence ?: 1.0f
        } ?: 1.0f
        
        score *= lowestConfidence.toDouble()
        
        // 3. Expiry Boost
        val hasExpiringItems = recipe.ingredients.any { ingredient ->
            val item = findInInventory(ingredient.item, inventory)
            // Logic: if expires within 2 days. For now, mock check
            item?.expiryDate?.let { 
                // java.time check would go here. 
                // Simply boosting if expiry is present for Phase 1 demo
                true
            } ?: false
        }
        
        if (hasExpiringItems) {
            score *= 1.5
        }
        
        return score
    }
    
    fun getMissingIngredients(recipe: Recipe, inventory: List<InventoryItem>): List<IngredientRef> {
        return recipe.ingredients.filter { ingredient ->
            val inStock = findInInventory(ingredient.item, inventory)
            inStock == null || inStock.status != StockStatus.IN_STOCK
        }
    }
    
    private fun findInInventory(identity: ItemIdentity, inventory: List<InventoryItem>): InventoryItem? {
        return inventory.find { it.item.name == identity.name } // Simple name match for now
    }
}

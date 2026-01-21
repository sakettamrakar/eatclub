package com.eatclub.app.core.domain

import com.eatclub.app.core.domain.ItemIdentity

data class IngredientRef(
    val item: ItemIdentity,
    val quantity: Quantity? = null, // Null if "some" or generic
    val optional: Boolean = false,
    val substitutes: List<ItemIdentity> = emptyList()
)

data class Recipe(
    val id: String,
    val title: String,
    val description: String,
    val ingredients: List<IngredientRef>,
    val prepTimeMinutes: Int,
    val cookTimeMinutes: Int,
    val tags: List<String> = emptyList()
)

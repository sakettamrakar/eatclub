package com.eatclub.app.core.domain

import java.math.BigDecimal

enum class Unit(val symbol: String) {
    GRAM("G"),
    KILOGRAM("KG"),
    MILLILITER("ML"),
    LITER("L"),
    PIECE("PCS"),
    BUNCH("BUNCH"),
    PINCH("PINCH"),
    PACKET("PACKET")
}

enum class StockStatus {
    IN_STOCK,
    LOW_STOCK,
    OUT_OF_STOCK,
    EXPIRED,
    UNKNOWN
}

data class Quantity(
    val value: BigDecimal,
    val unit: Unit,
    val approx: Boolean = false
) {
    init {
        require(value >= BigDecimal.ZERO) { "Quantity value must be non-negative" }
    }
}

data class ItemIdentity(
    val name: String,
    val variant: String? = null,
    val brand: String? = null,
    val confidence: Float = 1.0f
) {
    fun fullName(): String {
        val parts = mutableListOf(name)
        variant?.let { parts.add("($it)") }
        brand?.let { parts.add("[$it]") }
        return parts.joinToString(" ")
    }
}

data class InventoryItem(
    val item: ItemIdentity,
    val quantity: Quantity,
    val expiryDate: java.time.LocalDate? = null,
    val status: StockStatus = StockStatus.IN_STOCK
)

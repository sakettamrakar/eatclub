package com.eatclub.app.core.ingestion

import com.eatclub.app.core.domain.*
import java.util.UUID

data class DraftItem(
    val id: String = UUID.randomUUID().toString(),
    val item: ItemIdentity,
    val quantity: Quantity,
    val confidence: Float = 0.4f // Unverified
)

class IngestionService {
    
    // D4.1/4.2 Draft Flow Logic
    fun createDraft(items: List<DraftItem>): List<DraftItem> {
        // Logic to store drafts or return them for review
        return items
    }
    
    fun confirmDrafts(drafts: List<DraftItem>): List<InventoryItem> {
        // Convert drafts to final Items (mocking Ledger commit here)
        return drafts.map { draft ->
            InventoryItem(
                item = draft.item.copy(confidence = 1.0f), // Confirmed = 1.0
                quantity = draft.quantity
            )
        }
    }
    
    fun manualEntry(item: ItemIdentity, quantity: Quantity): InventoryItem {
        // Direct to Ledger (confidence 1.0)
        return InventoryItem(
            item = item.copy(confidence = 1.0f),
            quantity = quantity
        )
    }
}

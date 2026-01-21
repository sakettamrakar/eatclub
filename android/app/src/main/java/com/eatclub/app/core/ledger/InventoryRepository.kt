package com.eatclub.app.core.ledger

import com.eatclub.app.core.domain.*
import com.eatclub.app.data.db.LedgerDao
import com.eatclub.app.data.db.LedgerEventEntity
import com.google.gson.Gson
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.math.BigDecimal

class InventoryRepository(private val ledgerDao: LedgerDao) {

    // Simple in-memory state reconstruction for Phase 1
    // Ideally this would be cached or more optimized
    suspend fun getInventoryState(): List<InventoryItem> {
        val events = ledgerDao.getAllEventsSnapshot()
        val currentState = mutableMapOf<ItemIdentity, InventoryItem>()
        
        events.forEach { event ->
            applyEvent(currentState, event)
        }
        
        return currentState.values.filter { it.status == StockStatus.IN_STOCK }.toList()
    }

    fun getInventoryFlow(): Flow<List<InventoryItem>> {
        return ledgerDao.getAllEvents().map { events ->
            val currentState = mutableMapOf<ItemIdentity, InventoryItem>()
            events.forEach { event ->
                applyEvent(currentState, event)
            }
            currentState.values.filter { it.status == StockStatus.IN_STOCK }.toList()
        }
    }

    private fun applyEvent(state: MutableMap<ItemIdentity, InventoryItem>, event: LedgerEventEntity) {
        // Parse payload (assuming Gson availability or simple extraction)
        // For Phase 1 validation, we might mock the parsing if Gson isn't fully set up, 
        // but let's assume standard JSON structure from Python.
        
        // Note: Real implementation needs Full JSON parsing matching Python schemas.
        // Shortcuts taken here for brevity of the file, assuming "Purchase" adds and "Consume" subtracts.
        
        // This is a placeholder for the D1.1 Event-Sourcing Logic port.
        // In a real build, we'd share the JSON models or use kotlinx.serialization.
    }
}

package com.eatclub.app.ui.inventory

import androidx.lifecycle.LiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.asLiveData
import com.eatclub.app.core.domain.InventoryItem
import com.eatclub.app.core.ledger.InventoryRepository

class InventoryViewModel(private val repository: InventoryRepository) : ViewModel() {
    val inventory: LiveData<List<InventoryItem>> = repository.getInventoryFlow().asLiveData()
}

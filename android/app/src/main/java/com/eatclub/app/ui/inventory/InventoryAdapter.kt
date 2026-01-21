package com.eatclub.app.ui.inventory

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.eatclub.app.core.domain.InventoryItem
import com.eatclub.app.databinding.ItemInventoryBinding

class InventoryAdapter : ListAdapter<InventoryItem, InventoryAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemInventoryBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class ViewHolder(private val binding: ItemInventoryBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(item: InventoryItem) {
            binding.itemName.text = item.item.fullName()
            binding.itemQty.text = "${item.quantity.value} ${item.quantity.unit.symbol}"
            binding.itemExpiry.text = item.expiryDate?.toString() ?: "No Expiry"
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<InventoryItem>() {
        override fun areItemsTheSame(oldItem: InventoryItem, newItem: InventoryItem): Boolean {
            return oldItem.item == newItem.item
        }

        override fun areContentsTheSame(oldItem: InventoryItem, newItem: InventoryItem): Boolean {
            return oldItem == newItem
        }
    }
}

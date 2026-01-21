package com.eatclub.app.ui.inventory

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import com.eatclub.app.R
import com.eatclub.app.databinding.FragmentInventoryBinding

class InventoryFragment : Fragment(R.layout.fragment_inventory) {
    
    // Note: Manual dependency injection for Phase 1 (no Hilt yet)
    // In real app, use Hilt/Koin. Here assume ViewModelFactory handles it.
    private val viewModel: InventoryViewModel by viewModels() 
    private var _binding: FragmentInventoryBinding? = null
    private val binding get() = _binding!!

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentInventoryBinding.bind(view)
        
        val adapter = InventoryAdapter()
        binding.recyclerView.layoutManager = LinearLayoutManager(context)
        binding.recyclerView.adapter = adapter
        
        viewModel.inventory.observe(viewLifecycleOwner) { items ->
            adapter.submitList(items)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

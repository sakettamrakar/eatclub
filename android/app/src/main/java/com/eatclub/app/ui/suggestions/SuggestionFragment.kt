package com.eatclub.app.ui.suggestions

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import com.eatclub.app.R
import com.eatclub.app.databinding.FragmentSuggestionsBinding

class SuggestionFragment : Fragment(R.layout.fragment_suggestions) {
    
    private val viewModel: SuggestionsViewModel by viewModels()
    private var _binding: FragmentSuggestionsBinding? = null
    private val binding get() = _binding!!

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentSuggestionsBinding.bind(view)
        
        viewModel.suggestions.observe(viewLifecycleOwner) { suggestions ->
            // Update UI (Adapter logic similar to Inventory, simplified here)
            if (suggestions.isNotEmpty()) {
                binding.emptyStateText.visibility = View.GONE
                // binding.recyclerView.adapter.submitList(suggestions)
            } else {
                binding.emptyStateText.visibility = View.VISIBLE
            }
        }
        
        viewModel.refreshSuggestions()
    }
}

package com.eatclub.app.ui.ingest

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.eatclub.app.R
import com.eatclub.app.core.domain.*
import com.eatclub.app.core.ingestion.IngestionService
import com.eatclub.app.databinding.FragmentManualEntryBinding
import java.math.BigDecimal

class ManualEntryFragment : Fragment(R.layout.fragment_manual_entry) {

    private var _binding: FragmentManualEntryBinding? = null
    private val binding get() = _binding!!
    private val service = IngestionService() // Injected in real app

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentManualEntryBinding.bind(view)
        
        binding.submitButton.setOnClickListener {
            val name = binding.nameInput.text.toString()
            val qtyStr = binding.qtyInput.text.toString()
            
            if (name.isNotBlank() && qtyStr.isNotBlank()) {
                val item = service.manualEntry(
                    ItemIdentity(name),
                    Quantity(BigDecimal(qtyStr), Unit.PIECE) // Default unit for now
                )
                Toast.makeText(context, "Added ${item.item.name}", Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

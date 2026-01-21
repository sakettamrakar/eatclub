package com.eatclub.app.ui.ingest.passive;

import android.app.Activity;
import android.os.Bundle;
import java.util.List;

/**
 * D7.5 User approval UI
 * UI to list "Pending Invoices".
 */
public class PendingInvoicesActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // setContentView(R.layout.activity_pending_invoices);
        loadPendingInvoices();
    }

    private void loadPendingInvoices() {
        // Simulate fetching drafts
        // List<DraftSession> drafts = passiveIngestionService.getPendingDrafts();
        // display(drafts);
    }

    public void onImportClicked(String sessionId) {
        // Navigate to detail view for confirmation
        // Intent intent = new Intent(this, InvoiceDetailActivity.class);
        // intent.putExtra("SESSION_ID", sessionId);
        // startActivity(intent);
    }
}

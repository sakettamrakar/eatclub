package com.eatclub.app.core.logging

import java.io.File
import java.time.LocalDateTime

class SessionLogger(private val logFile: File) {

    fun logSessionStart() {
         appendLog("SESSION_START", "User opened app")
    }

    fun logSessionEnd() {
         appendLog("SESSION_END", "User closed app (inferred)")
    }
    
    fun logAction(action: String, details: String) {
        appendLog("ACTION", "$action: $details")
    }

    private fun appendLog(type: String, message: String) {
        val timestamp = LocalDateTime.now()
        val entry = "[$timestamp] [$type] $message\n"
        // In real Android, handle IO execution on background thread
        try {
            logFile.appendText(entry)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}

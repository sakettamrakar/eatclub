package com.eatclub.app.data.db

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.TypeConverter
import androidx.room.TypeConverters
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import java.time.Instant
import java.util.UUID

@Entity(tableName = "ledger_events")
data class LedgerEventEntity(
    @PrimaryKey val eventId: String,
    val timestamp: Long,
    val actor: String,
    val mutationType: String,
    val payloadJson: String
)

class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): Instant? {
        return value?.let { Instant.ofEpochMilli(it) }
    }

    @TypeConverter
    fun dateToTimestamp(date: Instant?): Long? {
        return date?.toEpochMilli()
    }
}

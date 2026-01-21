package com.eatclub.app.data.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface LedgerDao {
    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insert(event: LedgerEventEntity)

    @Query("SELECT * FROM ledger_events ORDER BY timestamp ASC")
    fun getAllEvents(): Flow<List<LedgerEventEntity>>

    @Query("SELECT * FROM ledger_events ORDER BY timestamp ASC")
    suspend fun getAllEventsSnapshot(): List<LedgerEventEntity>
}

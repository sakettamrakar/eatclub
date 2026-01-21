package com.eatclub.app.data.db

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters

@Database(entities = [LedgerEventEntity::class], version = 1)
@TypeConverters(Converters::class)
abstract class InventoryDatabase : RoomDatabase() {
    abstract fun ledgerDao(): LedgerDao
}

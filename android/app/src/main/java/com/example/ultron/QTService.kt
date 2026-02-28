package com.example.ultron

import android.content.Context
import android.service.quicksettings.Tile
import android.service.quicksettings.TileService
import android.util.Log
import com.example.ultron.elements.makeRequest

class QTService : TileService() {

    override fun onStartListening() {
        super.onStartListening()
    }

    override fun onClick() {
        super.onClick()


        val tile = qsTile
        val newState = if (tile.state == Tile.STATE_ACTIVE) {
            Tile.STATE_INACTIVE
        } else {
            Tile.STATE_ACTIVE
        }

        val value = if (newState == Tile.STATE_ACTIVE) "F" else "B"

        val prefs = getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)

        val serverUrl = prefs.all.filterKeys { it=="serverUrl" }
        makeRequest(serverUrl["serverUrl"].toString() + "door?value=$value")


        tile.state = newState
        tile.updateTile()
    }
}
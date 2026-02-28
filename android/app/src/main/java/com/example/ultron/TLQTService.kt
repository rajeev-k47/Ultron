package com.example.ultron

import android.content.Context
import android.service.quicksettings.Tile
import android.service.quicksettings.TileService
import com.example.ultron.elements.makeRequest

class TLQTService : TileService() {

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

        val prefs = getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)

        val serverUrl = prefs.all.filterKeys { it=="serverUrl" }
        makeRequest(serverUrl["serverUrl"].toString() + "tubelight")


        tile.state = newState
        tile.updateTile()
    }
}
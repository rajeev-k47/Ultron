package com.example.ultron.elements

import android.util.Log
import kotlinx.coroutines.*
import okhttp3.OkHttpClient
import okhttp3.Request

val client = OkHttpClient()

fun makeRequest(url: String) {
    CoroutineScope(Dispatchers.IO).launch {
        val request = Request.Builder()
            .url(url)
            .build()

        client.newCall(request).execute().use { response ->
            val body = response.body?.string()
            Log.d("match", response.body.toString())
            withContext(Dispatchers.Main) {
                println(body)
            }
        }
    }
}

package com.example.ultron.elements

import android.util.Log
import kotlinx.coroutines.*
import okhttp3.OkHttpClient
import okhttp3.Request
import okio.IOException

val client = OkHttpClient()

fun makeRequest(url: String) {
    CoroutineScope(Dispatchers.IO).launch {
        val request = Request.Builder()
            .url(url)
            .build()

        try {
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    return@launch
                }
            }
        } catch (e: IOException) {
            withContext(Dispatchers.Main) {
                println("Network Error: ${e.message}")
            }
        } catch (e: Exception) {
            withContext(Dispatchers.Main) {
                println("An unexpected error occurred: ${e.message}")
            }
        }
    }
}
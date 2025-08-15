package com.example.ultron.elements

import android.util.Log
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardColors
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldColors
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ultron.R
import com.example.ultron.ui.theme.BackgroundColor
import com.example.ultron.ui.theme.OverBackground

@Composable
fun MainFragment(preferencesManager: PreferencesManager, url: Map<String,*>){

    var serverUrl by rememberSaveable { mutableStateOf(preferencesManager.getData("serverUrl","")) }
    var bottomSettings by rememberSaveable { mutableStateOf(false) }
    var bottomAdd by rememberSaveable { mutableStateOf(false) }
    var urls by rememberSaveable { mutableStateOf(url) }

    Column(
        modifier = Modifier.fillMaxSize().background(BackgroundColor).windowInsetsPadding(WindowInsets.statusBars)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                "Ultron",
                modifier = Modifier.padding(horizontal = 10.dp, vertical = 10.dp),
                fontSize = 30.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Red
            )
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    painter = painterResource(id = R.drawable.more),
                    tint = Color.Red,
                    contentDescription = "Add",
                    modifier = Modifier.padding(end = 20.dp).size(28.dp).clickable {
                        bottomAdd=true
                    }
                )

                Icon(
                    painter = painterResource(id = R.drawable.setting),
                    tint = Color.Red,
                    contentDescription = "Settings",
                    modifier = Modifier.padding(end = 10.dp).size(30.dp).clickable {
                        bottomSettings=true
                    }
                )
            }
        }

        TextField(
            value = serverUrl,
            onValueChange = {},
            readOnly = true,
            prefix = { Text("Server URL : ") },
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp)
                .border(2.dp, Color.Gray, RoundedCornerShape(16.dp)), // Add border here
            colors = TextFieldDefaults.colors(
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = BackgroundColor,
                disabledContainerColor = Color.Transparent,
                errorContainerColor = Color.Transparent,
                unfocusedIndicatorColor = Color.Transparent,
                focusedIndicatorColor = Color.Transparent
            ),
        )
        Spacer(modifier = Modifier.height(5.dp))


        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            modifier = Modifier.fillMaxSize()
        ) {
            items(urls.keys.size) { item ->
                Card (
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(10.dp),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardColors(
                        containerColor = OverBackground.copy(alpha = 0.13f),
                        contentColor = Color.White,
                        disabledContainerColor = OverBackground.copy(alpha = 0.09f),
                        disabledContentColor = Color.White
                    )
                ){
                    Column (
                        Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    ){
                        Box (
                            modifier = Modifier
                                .fillMaxWidth(),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = urls.keys.elementAt(item),
                                fontSize = 22.sp,
                                fontWeight = FontWeight.Bold,
                                style = MaterialTheme.typography.headlineMedium,
                                color = OverBackground,
                                modifier = Modifier
                                    .padding(horizontal = 30.dp)
                                    .align(Alignment.Center),
                                overflow = TextOverflow.Ellipsis,
                                maxLines = 1,
                            )
                        }
                        Button(onClick ={
                                makeRequest(serverUrl+urls.values.elementAt(item))
                        },
                            modifier = Modifier
                                .padding(start = 10.dp),
                            shape = RoundedCornerShape(10.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = OverBackground.copy(alpha = 0.1f)),
                        ) {
                            Icon(painter = painterResource(id = R.drawable.send), contentDescription = "send", tint = OverBackground, modifier = Modifier.size(25.dp))
                        }
                        Spacer(Modifier.height(10.dp))

                    }
                }
            }
        }
    }

    if(bottomAdd){
        BottomAddSheet(onSubmit = {key,value->
            preferencesManager.saveData(key,value)
            urls = urls.toMutableMap().apply { put(key, value) }
        })
        {value->bottomAdd=value }
    }
    if(bottomSettings){
        BottomSettingsSheet(onSubmit = {
            serverUrl=it
            preferencesManager.saveData("serverUrl", it)
        }){ value-> bottomSettings = value }
    }

}
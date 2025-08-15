package com.example.ultron.elements

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonColors
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.example.ultron.ui.theme.BackgroundColor
import com.example.ultron.ui.theme.OverBackground

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BottomSettingsSheet(onSubmit:(String)->Unit, onSwitch:(Boolean)->Unit){
    val sheetState = rememberModalBottomSheetState()
    var serverUrl by rememberSaveable { mutableStateOf("") }
    ModalBottomSheet(
        onDismissRequest = { onSwitch(false) },
        sheetState = sheetState,
        containerColor = BackgroundColor
    ) {
        TextField(
            value = serverUrl,
            onValueChange = {serverUrl = it},
            placeholder = { Text("Enter new server url") },
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
        Spacer(modifier = Modifier.height(10.dp))

        Button(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 10.dp),
            onClick = {
                onSubmit(serverUrl)
                onSwitch(false)
            },
            colors = ButtonColors(
                contentColor = Color.Red,
                containerColor = OverBackground.copy(alpha = 0.1f),
                disabledContainerColor = Color.Transparent,
                disabledContentColor = Color.Transparent
            ),
            shape = RoundedCornerShape(16.dp)
        ) {
            Text("Submit")
        }
        Spacer(modifier = Modifier.height(10.dp))
    }
}
package com.example.ultron.widgets

import androidx.glance.appwidget.GlanceAppWidget
import androidx.glance.appwidget.GlanceAppWidgetReceiver

class AppWidgets : GlanceAppWidgetReceiver() {
    override val glanceAppWidget: GlanceAppWidget = RequestWidget()
}

<div align="center">
  <img src="assets/logo.png" alt="Logo" width="150" height="200">
  <h1><b>Ultron</b></h1>
</div>

Ultron is a custom modular Raspberry Pi system built to connect hardware control, messaging, and AI. Capable of computing and broadcasting of data and allows controlling hardware remotely. Integrated with multiple sensors to provide real time data for different purposes.

---

## System Architecture Overview

Ultron have multiple modules for multiple functionalities.

- Each capability lives in its own module
- Modules are loosely coupled
- A shared system/state layer coordinates execution
- Hardware interaction and higher-level logic are cleanly separated


## Hardware

- **Raspberry Pi 4** - Primary node which runs the core Ultron and its services.
- **Raspberry Pi 5** - Secondarily for computing and visualizing the real time data over the display.
- **ESP32-C6** - Microcontroller for low-level hardware control and wireless communication
- **Arduino Mega** - Handles extensive GPIO, sensors, and actuator control  
- **TFT Display (Raspberry Pi 5)** - Local screen for system status and sensor outputs  
- **LED Matrix** - Low-resolution visual output for symbols, messages, and state indication

## Core Modules

### `android/`
- Android app that allows controlling hardware over the system network wirelessly.
- Built for structured api calls with **Jetpack Compose x Kotlin**.

### `audio/`

Handles all sound-related capabilities.

Responsibilities:
- Controls buzzer for signal outputs.
- Speaker playback.
- StreamPlayer to play any songs abstracted using `yt-dlp`

### `video/`

Manages camera and visual input.

Responsibilities:
- Camera initialization
- Frame capture
- Video stream handling

Designed to support future computer vision, monitoring.

### `lights/`

Controls physical lighting components.

Responsibilities:
- Handles high voltage electrical appliances using relay.
- Handles the monitoring of day/night cycles using `LDR`.
- Operates WS2811B Addressable Pixel LED Strip amanaged by high privileged `./extstrip.py`.

This module translates logical states into physical light behavior.

### `matrix/`

Dedicated to LED matrix display.

Responsibilities:
- Operates the matrix using serialcomm. over Arduino Mega.
- Pixel or character rendering.
- Switch animations and static signals.

Acts as a **visual output surface** for system feedback, expressions, or diagnostics.

### `mqtts/`

Implements MQTT-based messaging.

Responsibilities:
- MQTT client setup
- Publish sensors data over mqtts and accessed over RPI5.
  
This is the primary **external communication layer**, enabling Ultron to share real-time data over internet.

### `gen_ai/`

Integrates generative AI capabilities.

Responsibilities:
- Speech-to-Text (STT)
- Text-to-Speech (TTS)
- LLM Output Generation (Groq)
  - Uses Groq-hosted large language models for response generation

This module does not control hardware directly. It influences system behavior via state and messaging.

### `state/`

Centralized state management.

Responsibilities:
- Maintain hardware system state
- Share context between modules
- Enable coordinated behavior for harware after rebooting of system.

### `main.py`

Acts as the **orchestrator**.

Responsibilities:
- Bootstraps the system
- Initializes modules
- Establishes the GPIO handlers for each functionality.
- Coordinates lifecycle management
- Exposes apis for hardware controls over network with FastAPI.

All high-level behavior flows through this file.

---

## Intended Use

- Embedded AI systems, AI controlling hardware
- Smart environment controllers
- Multiple hardwares for specific use cases.
- Can be used for Homelab.

---

## Installation

- Build for Raspberry Pi
```bash
git clone https://github.com/rajeev-k47/Ultron.git
cd Ultron
chmod +x ./install.sh
./install.sh
```

## Status

Active development. Modules may evolve independently.


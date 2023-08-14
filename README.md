# Reactive LEDs

**WORK IN PROGRESS**

This is a personal project in which I try to create an audio reactive led strip.

With as bigger goal to make a generic realtime audio detection software for helping generate visual art.


## Installation

**Led Controller**

Install `led_controller/led_controller.ino` using https://support.arduino.cc/hc/en-us/articles/4733418441116-Upload-a-sketch-in-Arduino-IDE

**Reactive Led**

```
poetry install
```

## Usage

With the led controller connected via usb run

```
poetry run src/main.py
```

## Architecture

```
Led Controller (arduino) ---usb--- Reactive Led Software (python)
```

## Bugs
- Threading: handle failing devices and wait for failing devices 
  - When power from led wait until serial device is back
- Audio: Find default output device

## Roadmap
- Moving average sampling 
- Bpm detection
  - transition based on bpm
- Audio metadata
  - Title, artist, genre enc.
- Frequency analysis
  - Emotion based colors and patterns
  - Fourier transform: Get notes played in a song and link them to an emotion
- Smooth transitions between patterns
- Web interface
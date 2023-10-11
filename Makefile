BAUD_RATE=250000
PORT=/dev/$(shell ls /dev/ | grep USB | head -n 1)
ARDUINO_OPTIONS = -b arduino:avr:nano:cpu=atmega328old -p ${PORT} -v 
ESP_OPTIONS = -b esp32:esp32:esp32:JTAGAdapter=default,PSRAM=disabled,PartitionScheme=default,CPUFreq=240,FlashMode=qio,FlashFreq=80,FlashSize=4M,UploadSpeed=921600,LoopCore=1,EventsCore=1,DebugLevel=none,EraseFlash=none -p ${PORT} -v

.DEFAULT_GOAL := debug

.PHONY: all debug firmware clean

all: firmware debug
	
debug:
	poetry run src/main.py

arduino:
	arduino-cli ${ARDUINO_OPTIONS} compile firmware
	arduino-cli ${ARDUINO_OPTIONS} upload firmware

esp:
	arduino-cli ${ESP_OPTIONS} compile firmware
	arduino-cli ${ESP_OPTIONS} upload firmware

serial:
	screen ${PORT} ${BAUD_RATE}

clean:
	rm -rf .venv
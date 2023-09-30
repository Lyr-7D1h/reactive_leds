ARDUINO_OPTIONS = -b arduino:avr:nano:cpu=atmega328old -p /dev/ttyUSB0 -v 

.DEFAULT_GOAL := debug

.PHONY: all debug update_firmware clean

all: update_firmware debug

debug:
	poetry run src/main.py

update_firmware:
	arduino-cli ${ARDUINO_OPTIONS} compile firmware
	arduino-cli ${ARDUINO_OPTIONS} upload firmware

clean:
	rm -rf .venv
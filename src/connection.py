#!/usr/bin/env python

import serial


class Connection:
    def __init__(self, serial_path: str, led_amount: int) -> None:
        self.led_amount = led_amount
        try:
            print(
                f"Connecting to led strip with {led_amount} leds through {serial_path}"
            )
            self.serial = serial.Serial(serial_path, 9600)
        except Exception as e:
            print(f"Could not open {serial_path}")
            print(e)
            exit(1)
        if not self.serial.is_open:
            self.serial.open()

    def __del__(self):
        print("Closing connection")
        self.serial.close()

    def available(self) -> bool:
        return self.serial.is_open

    def set(self, start: int, end: int, rgb: tuple[int, int, int]):
        if start == 255:
            raise Exception("Index 255 is reserved for showing")
        if end == 255:
            raise Exception("Index 255 is reserved for showing")
        self.serial.write(
            bytearray(
                [
                    start,
                    end,
                    rgb[0],
                    rgb[1],
                    rgb[2],
                ]
            )
        )
        self.serial.flush()

    def show(self):
        self.serial.write(bytearray([255, 0, 0, 0, 0]))
        # probably don't need this
        self.serial.flush()

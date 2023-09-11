#!/usr/bin/env python

import serial


class Connection:
    def __init__(self, serial_path: str, led_amount: int) -> None:
        self.led_amount = led_amount
        try:
            print(
                f"Connecting to led strip with {led_amount} leds through {serial_path}"
            )
            self.serial = serial.Serial(
                serial_path,
                250000,
                timeout=1,
                dsrdtr=True,
                rtscts=True,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
            )
        except Exception as e:
            print(f"Could not open {serial_path}")
            print(e)
            raise e
        if not self.serial.is_open:
            self.serial.open()

    def __del__(self):
        print("Closing connection")
        self.serial.close()

    def clear(self):
        self.serial.write(bytearray([0] * self.led_amount * 3))
        self.serial.flush()

    def available(self) -> bool:
        return self.serial.is_open

    def write(self, data: list[int]):
        self.serial.write(bytearray(data))
        self.serial.flush()

    def send(self, data: list[tuple[int, int, int]]):
        byte_data = bytearray([color for rgb in data for color in rgb])
        self.serial.write(byte_data)
        self.serial.flush()

    def fill(self, rgb: tuple[int, int, int]):
        data = [color for color in rgb for _ in range(0, self.led_amount)]
        self.write(data)

    def set(self, start: int, end: int, rgb: tuple[int, int, int]):
        data = [color for color in rgb for _ in range(start, end)]
        self.write(data)

    # def show(self):
    #     self.serial.write(bytearray([255, 0, 0, 0, 0]))
    #     # probably don't need this
    #     self.serial.flush()

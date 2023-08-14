#!/usr/bin/env python

import time
import serial


class Connection:
    def __init__(self, serial_path: str, led_amount: int) -> None:
        self.led_amount = led_amount
        try:
            self.serial = serial.Serial(serial_path, 9600)
        except Exception as e:
            print(f"Could not open {serial_path}")
            print(e)
            exit(1)
        if not self.serial.is_open:
            self.serial.open()

    def __del__(self):
        self.serial.close()

    # def all(self, rgb: tuple[int, int, int]):
    #     for i in range(0, self.led_amount):
    #         self.set(i, rgb)
    #     self.show()

    # def reset(
    #     self,
    # ):
    #     for i in range(0, 60):
    #         self.set(i, (10, 10, 10))
    #     self.show()

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


# connection = Connection()

# connection.reset()

# n = 60
# # i = 0
# for i in range(0, 60):
#     if i % 2 == 0:
#         connection.set(i, (200, 0, 0))
#     else:
#         connection.set(i, (0, 0, 200))
#     i += 1
#     i = i % n

# connection.show()
# connection.serial.flush()

# time.sleep(1)

from typing import Any
from unittest import mock

import minimalmodbus


def create_fake_modbus() -> minimalmodbus.Instrument:
    # Each register is 16 bits
    # One hex digit is 4 bits
    # 0x0000 == 16 bits (one register)
    data = {
        0x000A: 0x3014,
        0x000B: 0x2800,
        0x000C: "  RNG-CTRL-RVR40",
        0x0014: [0x0010, 0x2234],
        0x0016: [0x0011, 0x3422],
        0x0018: [0x1234, 0x5678],
        0x001A: 0x1234,
        0x0100: 98,
        0x0101: 124,
        0x0102: 3112,
        0x0103: 0x8514,
        0x0104: 145,
        0x0105: 3211,
        0x0106: 460,
        0x0107: 125,
        0x0108: 2440,
        0x0109: 305,
        0x010B: 128,
        0x010C: 55,
        0x010D: 3011,
        0x010E: 205,
        0x010F: 385,
        0x0110: 105,
        0x0111: 170,
        0x0112: 12,
        0x0113: 13450,
        0x0114: 123,
        0x0115: 180,
        0x0116: 5,
        0x0117: 123,
        0x0118: [0x0053, 0x0101],
        0x011A: [0x0105, 0x0202],
        0x011C: [0x0106, 0x0203],
        0x011E: [0x0205, 0x0104],
        0x0120: 0xBE02,
        0x0121: [0x0101, 0x0202],
        0xE002: 0xC8,
        0xE003: 0xC0C,
        0xE004: 0x0002,
        0xE005: 0xA0,
        0xE006: 0x9B,
        0xE007: 0x90,
        0xE008: 0x90,
        0xE009: 0x90,
        0xE00A: 0x84,
        0xE00B: 0x7E,
        0xE00C: 0x78,
        0xE00D: 0x6F,
        0xE00E: 0x6A,
        0xE00F: 0x6432,
        0xE010: 0x5,
        0xE011: 0x0,
        0xE012: 0x0,
        0xE013: 0x0,
        0xE014: 0x0,
        0xE015: 0x0,
        0xE016: 0x0,
        0xE017: 0x0,
        0xE018: 0x0,
        0xE019: 0x0,
        0xE01A: 0x0,
        0xE01B: 0x0,
        0xE01C: 0x0,
        0xE01D: 0x0,
        0xE01E: 0x5,
        0xE01F: 0xA,
        0xE020: 0x294,
        0xE021: 0x5,
    }

    fake_controller = mock.Mock(spec=minimalmodbus.Instrument)
    fake_controller.serial = mock.Mock()
    fake_controller.address = "/dev/ttyUSB0"
    fake_controller.port = 123

    fake_controller.read_register.side_effect = lambda x, *args, **kwargs: data.get(x)
    fake_controller.read_registers.side_effect = lambda x, *args, **kwargs: data.get(x)
    fake_controller.read_string.side_effect = lambda x, *args, **kwargs: data.get(x)

    def set_value(addr: int, value: Any) -> None:
        if addr in data:
            data[addr] = value
        else:
            raise ValueError(f"Address {addr} not found in fake modbus data")

    fake_controller.set_value = set_value

    return fake_controller

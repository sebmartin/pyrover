# pyrover

A Python client for communicating with the Renogy Rover MPPT solar charge controller over a wired
serial connection.

This utility is useful for connecting the Rover from a Raspberry Pi (or similar) to read
key statistics from the device. The modbus protocol has some support for writing to the device, but pyrover does
not (yet) support this.

There are several tutorials online describing how to make your own RS-485 to USB cable and there
might even be some available for purchase that are ready-to-use.

## Example

```python
>>> from pyrover.renogy_rover import RenogyRoverController
>>> rover = RenogyRoverController(port="/dev/ttyUSB0", address=1)
>>> rover.charging_state()
<ChargingState.MPPT: 2>
>>> rover.battery_percentage()
100
>>> rover.charging_current()
6.99
>>> [rover.solar_voltage(), rover.solar_current(), rover.charging_power()]
[33.1, 3.11, 103]
```

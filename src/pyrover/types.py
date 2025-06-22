from enum import IntFlag


class BatteryType(IntFlag):
    OPEN = 0x01
    SEALED = 0x02
    GEL = 0x03
    LITHIUM = 0x04
    SELF_CUSTOMIZED = 0x05

    def __str__(self) -> str:
        return {
            BatteryType.OPEN: "Open",
            BatteryType.SEALED: "Sealed",
            BatteryType.GEL: "Gel",
            BatteryType.LITHIUM: "Lithium",
            BatteryType.SELF_CUSTOMIZED: "Self-customized",
        }.get(self, "Unknown battery type")


class ProductType(IntFlag):
    CHARGE_CONTROLLER = 0x00
    INVERTER = 0x01

    def __str__(self) -> str:
        return {
            ProductType.CHARGE_CONTROLLER: "Charge controller",
            ProductType.INVERTER: "Inverter",
        }.get(self, "Unknown product type")


class Toggle(IntFlag):
    OFF = 0x00
    ON = 0x01

    def __str__(self) -> str:
        return {
            Toggle.OFF: "Off",
            Toggle.ON: "On",
        }.get(self, "Unknown on/off state")


class ChargingState(IntFlag):
    DEACTIVATED = 0x00
    ACTIVATED = 0x01
    MPPT = 0x02
    EQUALIZING = 0x03
    BOOST = 0x04
    FLOATING = 0x05
    CURRENT_LIMITING = 0x06

    def __str__(self) -> str:
        return {
            ChargingState.DEACTIVATED: "Charging deactivated",
            ChargingState.ACTIVATED: "Charging activated",
            ChargingState.MPPT: "MPPT charging mode",
            ChargingState.EQUALIZING: "Equalizing charging mode",
            ChargingState.BOOST: "Boost charging mode",
            ChargingState.FLOATING: "Floating charging mode",
            ChargingState.CURRENT_LIMITING: "Current limiting (overpower)",
        }.get(self, "Unknown charging state")


class Fault(IntFlag):
    # Lower bits 0-15 are reserved for future use
    BATTERY_OVER_DISCHARGE = 1 << 16
    BATTERY_OVER_VOLTAGE = 1 << 17
    BATTERY_UNDER_VOLTAGE = 1 << 18
    LOAD_SHORT_CIRCUIT = 1 << 19
    LOAD_OVER_CURRENT = 1 << 20
    CONTROL_TEMPERATURE_TOO_HIGH = 1 << 21
    AMBIENT_TEMPERATURE_TOO_HIGH = 1 << 22
    PHOTOVOLTAIC_OVER_POWER = 1 << 23
    PHOTOVOLTAIC_INPUT_SHORT_CIRCUIT = 1 << 24
    PHOTOVOLTAIC_INPUT_OVER_VOLTAGE = 1 << 25
    SOLAR_COUNTER_CURRENT = 1 << 26
    SOLAR_WORKING_POINT_OVER_VOLTAGE = 1 << 27
    SOLAR_REVERSELY_CONNECTED = 1 << 28
    ANTI_REVERSE_MOS_SHORT_CIRCUIT = 1 << 29
    CIRCUIT_CHARGE_MOS_SHORT_CIRCUIT = 1 << 30

    def __str__(self) -> str:
        return {
            Fault.BATTERY_OVER_DISCHARGE: "Battery over discharge",
            Fault.BATTERY_OVER_VOLTAGE: "Battery over voltage",
            Fault.BATTERY_UNDER_VOLTAGE: "Battery under voltage",
            Fault.LOAD_SHORT_CIRCUIT: "Load short circuit",
            Fault.LOAD_OVER_CURRENT: "Load over current",
            Fault.CONTROL_TEMPERATURE_TOO_HIGH: "Control temperature too high",
            Fault.AMBIENT_TEMPERATURE_TOO_HIGH: "Ambient temperature too high",
            Fault.PHOTOVOLTAIC_OVER_POWER: "Photovoltaic over power",
            Fault.PHOTOVOLTAIC_INPUT_SHORT_CIRCUIT: "Photovoltaic input short circuit",
            Fault.PHOTOVOLTAIC_INPUT_OVER_VOLTAGE: "Photovoltaic input over voltage",
            Fault.SOLAR_COUNTER_CURRENT: "Solar counter current",
            Fault.SOLAR_WORKING_POINT_OVER_VOLTAGE: "Solar working point over voltage",
            Fault.SOLAR_REVERSELY_CONNECTED: "Solar reversely connected",
            Fault.ANTI_REVERSE_MOS_SHORT_CIRCUIT: "Anti-reverse MOS short circuit",
            Fault.CIRCUIT_CHARGE_MOS_SHORT_CIRCUIT: "Circuit charge MOS short circuit",
        }.get(self, "Unknown fault")


class ChargingModeController(IntFlag):
    SOC = 0x00
    VOLTAGE = 0x01

    def __str__(self) -> str:
        return {
            ChargingModeController.SOC: "State of charge",
            ChargingModeController.VOLTAGE: "Voltage",
        }.get(self, "Unknown charging mode controller")


class ChargingMethod(IntFlag):
    DIRECT = 0x00
    PWM = 0x01

    def __str__(self) -> str:
        return {
            ChargingMethod.DIRECT: "Direct charging",
            ChargingMethod.PWM: "PWM",
        }.get(self, "Unknown charging method")


class LoadWorkingModes(IntFlag):
    SOLE_LIGHT_CONTROL = 0x00
    OFF_AFTER_1H = 0x01
    OFF_AFTER_2H = 0x02
    OFF_AFTER_3H = 0x03
    OFF_AFTER_4H = 0x04
    OFF_AFTER_5H = 0x05
    OFF_AFTER_6H = 0x06
    OFF_AFTER_7H = 0x07
    OFF_AFTER_8H = 0x08
    OFF_AFTER_9H = 0x09
    OFF_AFTER_10H = 0x0A
    OFF_AFTER_11H = 0x0B
    OFF_AFTER_12H = 0x0C
    OFF_AFTER_13H = 0x0D
    OFF_AFTER_14H = 0x0E
    MANUAL = 0x0F
    DEBUG = 0x10
    NORMAL_ON = 0x11

    def __str__(self) -> str:
        return {
            LoadWorkingModes.SOLE_LIGHT_CONTROL: "Sole light control over on/off of load",
            LoadWorkingModes.OFF_AFTER_1H: (
                "Load is turned on by light control, and goes off after a time delay of 1 hour"
            ),
            LoadWorkingModes.OFF_AFTER_2H: (
                "Load is turned on by light control, and goes off after a time delay of 2 hours"
            ),
            LoadWorkingModes.OFF_AFTER_3H: (
                "Load is turned on by light control, and goes off after a time delay of 3 hours"
            ),
            LoadWorkingModes.OFF_AFTER_4H: (
                "Load is turned on by light control, and goes off after a time delay of 4 hours"
            ),
            LoadWorkingModes.OFF_AFTER_5H: (
                "Load is turned on by light control, and goes off after a time delay of 5 hours"
            ),
            LoadWorkingModes.OFF_AFTER_6H: (
                "Load is turned on by light control, and goes off after a time delay of 6 hours"
            ),
            LoadWorkingModes.OFF_AFTER_7H: (
                "Load is turned on by light control, and goes off after a time delay of 7 hours"
            ),
            LoadWorkingModes.OFF_AFTER_8H: (
                "Load is turned on by light control, and goes off after a time delay of 8 hours"
            ),
            LoadWorkingModes.OFF_AFTER_9H: (
                "Load is turned on by light control, and goes off after a time delay of 9 hours"
            ),
            LoadWorkingModes.OFF_AFTER_10H: (
                "Load is turned on by light control, and goes off after a time delay of 10 hours"
            ),
            LoadWorkingModes.OFF_AFTER_11H: (
                "Load is turned on by light control, and goes off after a time delay of 11 hours"
            ),
            LoadWorkingModes.OFF_AFTER_12H: (
                "Load is turned on by light control, and goes off after a time delay of 12 hours"
            ),
            LoadWorkingModes.OFF_AFTER_13H: (
                "Load is turned on by light control, and goes off after a time delay of 13 hours"
            ),
            LoadWorkingModes.OFF_AFTER_14H: (
                "Load is turned on by light control, and goes off after a time delay of 14 hours"
            ),
            LoadWorkingModes.MANUAL: "Manual on/off of load",
            LoadWorkingModes.DEBUG: "Debug mode",
            LoadWorkingModes.NORMAL_ON: "Load is always on",
        }.get(self, "Unknown load working mode")

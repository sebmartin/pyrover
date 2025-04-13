from unittest import mock

import pytest

from pyrover.renogy_rover import RenogyRoverController
from pyrover.types import (
    BatteryType,
    ChargingMethod,
    ChargingModeController,
    ChargingState,
    Fault,
    LoadWorkingModes,
    Toggle,
    ProductType,
)
from tests.fakes.fake_modbus import create_fake_modbus


@pytest.fixture
def fake_modbus():
    return create_fake_modbus()


@pytest.fixture()
def controller(fake_modbus):
    with mock.patch("pyrover.renogy_rover._create_controller") as mock_create_controller:
        mock_create_controller.return_value = fake_modbus
        yield RenogyRoverController(port=123, address="/dev/ttyUSB0")


def test_controller_init_fails_if_controller_serial_is_none(fake_modbus):
    fake_modbus.serial = None
    with mock.patch("pyrover.renogy_rover._create_controller") as mock_create_controller:
        mock_create_controller.return_value = fake_modbus
        with pytest.raises(AssertionError):
            RenogyRoverController(port=123, address="/dev/ttyUSB0")


@pytest.mark.parametrize(
    "addr,bytes,metric,expected",
    [
        (0x000A, 2, "max_system_voltage", 48),
        (0x000A, 2, "rated_charging_current", 20),
        (0x000B, 2, "rated_discharging_current", 40),
        (0x000C, 16, "product_model", "RNG-CTRL-RVR40"),
        (0x0014, 4, "software_version", "16.34.52"),
        (0x0016, 4, "hardware_version", "17.52.34"),
        (0x0018, 4, "serial_number", 305419896),
        (0x001A, 2, "device_address", 4660),
        (0x0100, 2, "battery_percentage", 98),
        (0x0101, 2, "battery_voltage", 12.4),
        (0x0102, 2, "charging_current", 31.12),
        (0x0103, 2, "controller_temperature", -5),
        (0x0103, 2, "battery_temperature", 20),
        (0x0104, 2, "load_voltage", 14.5),
        (0x0105, 2, "load_current", 32.11),
        (0x0106, 2, "load_power", 460),
        (0x0107, 2, "solar_voltage", 12.5),
        (0x0108, 2, "solar_current", 24.4),
        (0x0109, 2, "charging_power", 305),
        (0x010B, 2, "battery_min_voltage_today", 12.8),
        (0x010C, 2, "battery_max_voltage_today", 5.5),
        (0x010D, 2, "max_charging_current_today", 30.11),
        (0x010E, 2, "max_discharging_current_today", 2.05),
        (0x010F, 2, "max_charging_power_today", 385),
        (0x0110, 2, "max_discharging_power_today", 105),
        (0x0111, 2, "charging_amphours_today", 170),
        (0x0112, 2, "discharging_amphours_today", 12),
        (0x0113, 2, "power_generation_today", 1.345),
        (0x0114, 2, "power_consumption_today", 0.0123),
        (0x0115, 2, "total_operating_days", 180),
        (0x0116, 2, "total_battery_over_discharges", 5),
        (0x0117, 2, "total_battery_full_charges", 123),
        (0x0118, 4, "total_battery_charge_amphours", 5439745),
        (0x011A, 4, "total_battery_discharge_amphours", 17105410),
        (0x011C, 4, "cumulative_power_generation", 1717.0947),
        (0x011E, 4, "cumulative_power_consumption", 3388.2372),
        (0x0120, 2, "street_light_brightness", 62),
        (0xE002, 2, "nominal_battery_capacity", 200),
        (0xE003, 2, "system_voltage_setting", 12),  # parameterize
        (0xE003, 2, "recognized_voltage", 12),  # parameterize
        (0xE005, 2, "over_voltage_threshold", 16.0),
        (0xE006, 2, "charging_voltage_limit", 15.5),
        (0xE007, 2, "equalizing_charging_voltage", 14.4),
        (0xE008, 2, "boost_charging_voltage", 14.4),
        (0xE009, 2, "floating_voltage", 14.4),
        (0xE00A, 2, "boost_charging_recovery_voltage", 13.2),
        (0xE00B, 2, "over_discharge_recovery_voltage", 12.6),
        (0xE00C, 2, "under_voltage_warning_level", 12.0),
        (0xE00D, 2, "over_discharge_voltage", 11.1),
        (0xE00E, 2, "discharging_limit_voltage", 10.6),
        (0xE00F, 2, "end_of_charge_soc", 100),
        (0xE00F, 2, "end_of_discharge_soc", 50),
        (0xE010, 2, "over_discharge_time_delay", 5),
        (0xE011, 2, "equalizing_charging_time", 0),
        (0xE012, 2, "boost_charging_time", 0),
        (0xE013, 2, "equalizing_charging_interval", 0),
        (0xE014, 2, "temperature_compensation_factor", 0),
        (0xE015, 2, "first_stage_operating_duration", 0),
        (0xE016, 2, "first_stage_operating_power", 0),
        (0xE017, 2, "second_stage_operating_duration", 0),
        (0xE018, 2, "second_stage_operating_power", 0),
        (0xE019, 2, "third_stage_operating_duration", 0),
        (0xE01A, 2, "third_stage_operating_power", 0),
        (0xE01B, 2, "morning_on_operating_duration", 0),
        (0xE01C, 2, "morning_on_operating_power", 0),
        (0xE01E, 2, "light_control_delay", 5),
        (0xE01F, 2, "light_control_voltage", 10),
        (0xE020, 2, "led_load_current_setting", 6.6),
    ],
)
def test_controller_metrics(addr, bytes, metric, expected, controller, fake_modbus):
    assert hasattr(controller, metric), f"Controller does not have metric {metric}"
    assert getattr(controller, metric)() == expected, f"Unexpected value for metric {metric}"
    if bytes == 2:
        fake_modbus.read_register.assert_called_with(addr)
    elif bytes > 4:
        fake_modbus.read_string.assert_called_with(addr, number_of_registers=bytes // 2)
    else:
        fake_modbus.read_registers.assert_called_with(addr, number_of_registers=bytes // 2)


@pytest.mark.parametrize(
    "addr,bytes,value,metric,expected",
    [
        (0x000B, 2, 0xFF00, "product_type", ProductType.CHARGE_CONTROLLER),
        (0x000B, 2, 0xFF01, "product_type", ProductType.INVERTER),
        (0x0120, 2, 0x70FF, "street_light_status", Toggle.OFF),
        (0x0120, 2, 0x80FF, "street_light_status", Toggle.ON),
        # TODO: v-- verify battery type values from actual device --v
        (0xE004, 2, 0x0001, "battery_type", BatteryType.OPEN),
        (0xE004, 2, 0x0002, "battery_type", BatteryType.SEALED),
        (0xE004, 2, 0x0003, "battery_type", BatteryType.GEL),
        (0xE004, 2, 0x0004, "battery_type", BatteryType.LITHIUM),
        (0xE004, 2, 0x0005, "battery_type", BatteryType.SELF_CUSTOMIZED),
        (0x0120, 2, 0xFF00, "charging_state", ChargingState.DEACTIVATED),
        (0x0120, 2, 0xFF01, "charging_state", ChargingState.ACTIVATED),
        (0x0120, 2, 0xFF02, "charging_state", ChargingState.MPPT),
        (0x0120, 2, 0xFF03, "charging_state", ChargingState.EQUALIZING),
        (0x0120, 2, 0xFF04, "charging_state", ChargingState.BOOST),
        (0x0120, 2, 0xFF05, "charging_state", ChargingState.FLOATING),
        (0x0120, 2, 0xFF06, "charging_state", ChargingState.CURRENT_LIMITING),
        (
            0x0121,
            4,
            [0x0000, 0xFFFF],
            "controller_fault_information",
            [],
        ),
        (
            0x0121,
            4,
            [
                0xFFFF,
                0xFFFF,
            ],
            "controller_fault_information",
            [
                Fault.BATTERY_OVER_DISCHARGE,
                Fault.BATTERY_OVER_VOLTAGE,
                Fault.BATTERY_UNDER_VOLTAGE,
                Fault.LOAD_SHORT_CIRCUIT,
                Fault.LOAD_OVER_CURRENT,
                Fault.CONTROL_TEMPERATURE_TOO_HIGH,
                Fault.AMBIENT_TEMPERATURE_TOO_HIGH,
                Fault.PHOTOVOLTAIC_OVER_POWER,
                Fault.PHOTOVOLTAIC_INPUT_SHORT_CIRCUIT,
                Fault.PHOTOVOLTAIC_INPUT_OVER_VOLTAGE,
                Fault.SOLAR_COUNTER_CURRENT,
                Fault.SOLAR_WORKING_POINT_OVER_VOLTAGE,
                Fault.SOLAR_REVERSELY_CONNECTED,
                Fault.ANTI_REVERSE_MOS_SHORT_CIRCUIT,
                Fault.CIRCUIT_CHARGE_MOS_SHORT_CIRCUIT,
            ],
        ),
        (0xE01D, 2, 0x0000, "load_working_mode", LoadWorkingModes.SOLE_LIGHT_CONTROL),
        (0xE01D, 2, 0x0001, "load_working_mode", LoadWorkingModes.OFF_AFTER_1H),
        (0xE01D, 2, 0x0002, "load_working_mode", LoadWorkingModes.OFF_AFTER_2H),
        (0xE01D, 2, 0x0003, "load_working_mode", LoadWorkingModes.OFF_AFTER_3H),
        (0xE01D, 2, 0x0004, "load_working_mode", LoadWorkingModes.OFF_AFTER_4H),
        (0xE01D, 2, 0x0005, "load_working_mode", LoadWorkingModes.OFF_AFTER_5H),
        (0xE01D, 2, 0x0006, "load_working_mode", LoadWorkingModes.OFF_AFTER_6H),
        (0xE01D, 2, 0x0007, "load_working_mode", LoadWorkingModes.OFF_AFTER_7H),
        (0xE01D, 2, 0x0008, "load_working_mode", LoadWorkingModes.OFF_AFTER_8H),
        (0xE01D, 2, 0x0009, "load_working_mode", LoadWorkingModes.OFF_AFTER_9H),
        (0xE01D, 2, 0x000A, "load_working_mode", LoadWorkingModes.OFF_AFTER_10H),
        (0xE01D, 2, 0x000B, "load_working_mode", LoadWorkingModes.OFF_AFTER_11H),
        (0xE01D, 2, 0x000C, "load_working_mode", LoadWorkingModes.OFF_AFTER_12H),
        (0xE01D, 2, 0x000D, "load_working_mode", LoadWorkingModes.OFF_AFTER_13H),
        (0xE01D, 2, 0x000E, "load_working_mode", LoadWorkingModes.OFF_AFTER_14H),
        (0xE01D, 2, 0x000F, "load_working_mode", LoadWorkingModes.MANUAL),
        (0xE01D, 2, 0x0010, "load_working_mode", LoadWorkingModes.DEBUG),
        (0xE01D, 2, 0x0011, "load_working_mode", LoadWorkingModes.NORMAL_ON),
        (0xE021, 2, 0xF0FF, "charging_mode_controlled_by", ChargingModeController.SOC),
        (
            0xE021,
            2,
            0xF4FF,
            "charging_mode_controlled_by",
            ChargingModeController.VOLTAGE,
        ),
        (0xE021, 2, 0xF0FF, "special_power_control_state", Toggle.OFF),
        (0xE021, 2, 0xF2FF, "special_power_control_state", Toggle.ON),
        (0xE021, 2, 0xF0FF, "each_night_on_function_state", Toggle.OFF),
        (0xE021, 2, 0xF1FF, "each_night_on_function_state", Toggle.ON),
        (0xE021, 2, 0xFF00, "no_charging_below_freezing", Toggle.OFF),
        (0xE021, 2, 0xFF04, "no_charging_below_freezing", Toggle.ON),
        (0xE021, 2, 0xFF00, "charging_method", ChargingMethod.DIRECT),
        (0xE021, 2, 0xFF01, "charging_method", ChargingMethod.PWM),
    ],
)
def test_controller_metrics_enums(addr, bytes, value, metric, expected, controller, fake_modbus):
    fake_modbus.set_value(addr, value)
    assert hasattr(controller, metric), f"Controller does not have metric {metric}"
    assert getattr(controller, metric)() == expected, f"Unexpected value for metric {metric}"
    if bytes == 2:
        fake_modbus.read_register.assert_called_with(addr)
    elif bytes > 4:
        fake_modbus.read_string.assert_called_with(addr, number_of_registers=bytes // 2)
    else:
        fake_modbus.read_registers.assert_called_with(addr, number_of_registers=bytes // 2)


@pytest.mark.parametrize(
    "value,expected,expected_str",
    [
        ([0x0001, 0xFFFF], Fault.BATTERY_OVER_DISCHARGE, "Battery over discharge"),
        ([0x0002, 0xFFFF], Fault.BATTERY_OVER_VOLTAGE, "Battery over voltage"),
        ([0x0004, 0xFFFF], Fault.BATTERY_UNDER_VOLTAGE, "Battery under voltage"),
        ([0x0008, 0xFFFF], Fault.LOAD_SHORT_CIRCUIT, "Load short circuit"),
        ([0x0010, 0xFFFF], Fault.LOAD_OVER_CURRENT, "Load over current"),
        (
            [0x0020, 0xFFFF],
            Fault.CONTROL_TEMPERATURE_TOO_HIGH,
            "Control temperature too high",
        ),
        (
            [0x0040, 0xFFFF],
            Fault.AMBIENT_TEMPERATURE_TOO_HIGH,
            "Ambient temperature too high",
        ),
        ([0x0080, 0xFFFF], Fault.PHOTOVOLTAIC_OVER_POWER, "Photovoltaic over power"),
        (
            [0x0100, 0xFFFF],
            Fault.PHOTOVOLTAIC_INPUT_SHORT_CIRCUIT,
            "Photovoltaic input short circuit",
        ),
        (
            [0x0200, 0xFFFF],
            Fault.PHOTOVOLTAIC_INPUT_OVER_VOLTAGE,
            "Photovoltaic input over voltage",
        ),
        ([0x0400, 0xFFFF], Fault.SOLAR_COUNTER_CURRENT, "Solar counter current"),
        (
            [0x0800, 0xFFFF],
            Fault.SOLAR_WORKING_POINT_OVER_VOLTAGE,
            "Solar working point over voltage",
        ),
        (
            [0x1000, 0xFFFF],
            Fault.SOLAR_REVERSELY_CONNECTED,
            "Solar reversely connected",
        ),
        (
            [0x2000, 0xFFFF],
            Fault.ANTI_REVERSE_MOS_SHORT_CIRCUIT,
            "Anti-reverse MOS short circuit",
        ),
        (
            [0x4000, 0xFFFF],
            Fault.CIRCUIT_CHARGE_MOS_SHORT_CIRCUIT,
            "Circuit charge MOS short circuit",
        ),
    ],
)
def test_controller_individual_fault_codes_and_messages(
    value, expected, expected_str, controller: RenogyRoverController, fake_modbus
):
    fake_modbus.set_value(0x0121, value)
    faults = controller.controller_fault_information()
    assert len(faults) == 1
    fault = faults[0]
    assert fault == expected
    assert str(fault) == expected_str

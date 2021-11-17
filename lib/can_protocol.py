import struct

ARBITRATION_IDS = {
    "CONTROLLER_COMMAND": 0x00,
    "BMS_STATE_CHANGE": 0x0B,
    "MC_STATE_CHANGE": 0x15,
    "MANUAL_CONTROL": 0x08
}

STATE_IDS = {
    "RESTING": 0x00,
    "LV_READY": 0x01,
    "ARMED": 0x02,
    "AUTO_PILOT": 0x03,
    "BRAKING": 0x04,
    "EMERGENCY_BRAKE": 0x05,
    "SYSTEM_FAILURE": 0x06,
    "MANUAL_OPERATION_WAITING": 0x07,
    "ACCELERATING": 0x08,
    "AT_SPEED": 0x09,
    "DECELERATING": 0x0a,
    "INVALID": 0x0b,
    "NACK": 0xff
}

def get_state_name(state_id: int):
    for k in STATE_IDS:
        if STATE_IDS[k] == state_id:
            return k
    return "INVALID"


def _le_int_to_float(bytes_: list):
    tmp = bytearray(bytes_)
    tmp.reverse()
    return struct.unpack(">f", tmp)[0]

ID_LUT = {}

def decode_STATE_CHANGE_REQ(payload: list):
    print(f"STATE_CHANGE_REQ: STATE_ID = {STATE_IDS[payload[0]]}")

ID_LUT[0x000] = decode_STATE_CHANGE_REQ

def decode_BMS_HEALTH_CHECK(payload: list):
    pack_curr = _le_int_to_float(payload[0:4])
    cell_temp = _le_int_to_float(payload[4:8])
    print(f"BMS_HEALTH_CHECK: BATTERY_PACK_CURRENT = {pack_curr}, AVERAGE_CELL_TEMPERATURE = {cell_temp}")

ID_LUT[0x001] = decode_BMS_HEALTH_CHECK

def decode_MOTOR_CONTROLLER_HEALTH_CHECK(payload: list):
    igbt_temp = _le_int_to_float(payload[0:4])
    motor_voltage = _le_int_to_float(payload[4:8])
    print(f"MOTOR_CONTROLLER_HEALTH_CHECK: IGBT_TEMPERATURE = {igbt_temp}, MOTOR_VOLTAGE = {motor_voltage}")

ID_LUT[0x002] = decode_MOTOR_CONTROLLER_HEALTH_CHECK

def decode_MANUAL_CONTROL_1(payload: list):
    target_speed = _le_int_to_float(payload[0:4])
    target_freq = _le_int_to_float(payload[4:8])
    print(f"MANUAL_CONTROL_1: TARGET_SPEED = {target_speed}, TARGET_FREQUENCY = {target_freq}")

ID_LUT[0x006] = decode_MANUAL_CONTROL_1

def decode_MANUAL_CONTROL_2(payload: list):
    target_power = payload[0:4]
    print(f"MANUAL_CONTROL_2: TARGET_POWER = {target_power}")

ID_LUT[0x007] = decode_MANUAL_CONTROL_2

def decode_MANUAL_CONTROL_3(payload: list):
    temp_limit = _le_int_to_float(payload[0:4])
    curr_limit = _le_int_to_float(payload[4:8])
    print(f"MANUAL_CONTROL_3: SET_TEMPERATURE_LIMIT = {temp_limit}, SET_CURRENT_LIMIT = {curr_limit}")

ID_LUT[0x008] = decode_MANUAL_CONTROL_3

def decode_BMS_FAULT_REPORT(payload: list):
    severity_lut = {
        0: "SEVERE",
        1: "DANGER",
        2: "WARNING"
    }
    error_lut = {
        0: "BATTERY_OVERVOLTAGE",
        1: "BATTERY_UNDERVOLTAGE",
        2: "BATTERY_OVERCURRENT",
        3: "BATTERY_SOC",
        4: "CELL_UNDERVOLTAGE",
        5: "CELL_OVERVOLTAGE",
        6: "CELL_TEMPERATURE",
        7: "BUCK_TEMPERATURE"
    }
    print(f"BMS_FAULT_REPORT: SEVERITY = {severity_lut[payload[0]]}, ERROR = {error_lut[payload[1]]}")

ID_LUT[0x00A] = decode_BMS_FAULT_REPORT

def decode_BMS_STATE_CHANGE_ACK_NACK(payload: list):
    ack_lut = {0: "ACK", 255: "NACK"}
    print(f"BMS_STATE_CHANGE_ACK_NACK: STATE_ID = {STATE_IDS[payload[0]]}, ACK = {ack_lut[payload[1]]}")

ID_LUT[0x00B] = decode_BMS_STATE_CHANGE_ACK_NACK

def decode_BMS_DATA_1(payload: list):
    pack_voltage = _le_int_to_float(payload[0:4])
    soc = _le_int_to_float(payload[4:8])
    print(f"BMS_DATA_1: BATTERY_PACK_VOLTAGE = {pack_voltage}, STATE_OF_CHARGE = {soc}")

ID_LUT[0x00C] = decode_BMS_DATA_1

def decode_BMS_DATA_2(payload: list):
    buck_temp = _le_int_to_float(payload[0:4])
    curr = _le_int_to_float(payload[4:8])
    print(f"BMS_DATA_2: BUCK_TEMPERATURE = {buck_temp}, BMS_CURRENT = {curr}")

ID_LUT[0x00D] = decode_BMS_DATA_2

def decode_BMS_DATA_3(payload: list):
    cap_voltage = _le_int_to_float(payload[0:4])
    print(f"BMS_DATA_3: LINK_CAP_VOLTAGE = {cap_voltage}")

ID_LUT[0x00E] = decode_BMS_DATA_3

def decode_MOTOR_CONTROLLER_FAULT_REPORT(payload: list):
    pass

def decode_MOTOR_CONTROLLER_STATE_CHANGE_ACK_NACK(payload: list):
    pass

def decode_MOTOR_CONTROLLER_DATA_1(payload: list):
    pass

def decode_MOTOR_CONTROLLER_DATA_2(payload: list):
    pass

def decode_RING_ENCODER(payload: list):
    pass

def decode_PRESSURE_SENSOR_HIGH(payload: list):
    pass

def decode_PRESSURE_SENSOR_LOW(payload: list):
    pass

def decode_PRESSURE_SENSOR_LOW_2(payload: list):
    pass

def decode_5_VOLTS(payload: list):
    pass

def decode_12_VOLTS(payload: list):
    pass

def decode_24_VOLTS(payload: list):
    pass

# This is something like 0x580
def decode_ROBOTEQ_RESPONSE(payload: list):
    pass

# This is something like 0x600
def decode_ROBOTEQ_COMMAND(payload: list):
    pass

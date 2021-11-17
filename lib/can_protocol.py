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
    print(f"")
ID_LUT[0x001] = decode_BMS_HEALTH_CHECK

def decode_MOTOR_CONTROLLER_HEALTH_CHECK(payload: list):
    pass

def decode_MANUAL_CONTROL_A(payload: list):
    pass

def decode_MANUAL_CONTROL_B(payload: list):
    pass

def decode_MANUAL_CONTROL_C(payload: list):
    pass

def decode_BMS_FAULT_REPORT(payload: list):
    pass

def decode_BMS_STATE_CHANGE_ACK_NACK(payload: list):
    pass

def decode_BMS_DATA_1(payload: list):
    pass

def decode_BMS_DATA_2(payload: list):
    pass

def decode_BMS_DATA_3(payload: list):
    pass

def decode_MOTOR_CONTROLLER_FAULT_REPORT(payload: list):
    print("Motor controller DNE lul")
ID_LUT[0x014] = decode_MOTOR_CONTROLLER_FAULT_REPORT

def decode_MOTOR_CONTROLLER_STATE_CHANGE_ACK_NACK(payload: list):
    print(f"MOTOR_CONTROLLER_STATE_CHANGE_ACK_NACK: STATE_ID = {STATE_IDS[payload[0]]}")
ID_LUT[0x015] = decode_MOTOR_CONTROLLER_STATE_CHANGE_ACK_NACK

def decode_MOTOR_CONTROLLER_DATA_1(payload: list):
    speed = _le_int_to_float(payload[0:3])
    current = _le_int_to_float(payload[4:7])
    print(f"MOTOR_CONTROLLER_DATA_1: POD_SPEED = {speed}, MOTOR_CURRENT = {current}")
ID_LUT[0x016] = decode_MOTOR_CONTROLLER_DATA_1

def decode_MOTOR_CONTROLLER_DATA_2(payload: list):
    current = _le_int_to_float(payload[0:3])
    voltage = _le_int_to_float(payload[4:7])
    print(f"MOTOR_CONTROLLER_DATA_2: BATTERY_CURRENT = {current}, BATTERY_VOLTAGE = {voltage}")
ID_LUT[0x017] = decode_MOTOR_CONTROLLER_DATA_2

def decode_RING_ENCODER(payload: list):
    speed = _le_int_to_float(payload[0:3])
    print(f"RING_ENCODER: POD_SPEED = {speed}")
ID_LUT[0x01f] = decode_RING_ENCODER

def decode_PRESSURE_SENSOR_HIGH(payload: list):
    pressure = _le_int_to_float(payload[0:3])
    print(f"PRESSURE_SENSOR_HIGH: PRESSURE = {pressure}")
ID_LUT[0x020] = decode_PRESSURE_SENSOR_HIGH

def decode_PRESSURE_SENSOR_LOW(payload: list):
    pressure = _le_int_to_float(payload[0:3])
    print(f"PRESSURE_SENSOR_LOW: PRESSURE = {pressure}")
ID_LUT[0x021] = decode_PRESSURE_SENSOR_LOW

def decode_PRESSURE_SENSOR_LOW_2(payload: list):
    pressure = _le_int_to_float(payload[0:3])
    print(f"PRESSURE_SENSOR_LOW_2: PRESSURE = {pressure}")
ID_LUT[0x022] = decode_PRESSURE_SENSOR_LOW_2

def decode_5_VOLTS(payload: list):
    current = _le_int_to_float(payload[0:3])
    print(f"5V_CURRENT: CURRENT = {current}")
ID_LUT[0x032] = decode_5_VOLTS

def decode_12_VOLTS(payload: list):
    current = _le_int_to_float(payload[0:3])
    print(f"12V_CURRENT: CURRENT = {current}")
ID_LUT[0x032] = decode_12_VOLTS

def decode_24_VOLTS(payload: list):
    current = _le_int_to_float(payload[0:3])
    print(f"24V_CURRENT: CURRENT = {current}")
ID_LUT[0x032] = decode_24_VOLTS

# This is something like 0x580
def decode_ROBOTEQ_RESPONSE(ID: int, payload: list):
    pass
ID_LUT[0x580] = decode_ROBOTEQ_RESPONSE
ID_LUT[0x581] = decode_ROBOTEQ_RESPONSE
ID_LUT[0x582] = decode_ROBOTEQ_RESPONSE

# This is something like 0x600
def decode_ROBOTEQ_COMMAND(payload: list):
    pass
ID_LUT[0x600] = decode_ROBOTEQ_COMMAND
ID_LUT[0x601] = decode_ROBOTEQ_COMMAND
ID_LUT[0x602] = decode_ROBOTEQ_COMMAND
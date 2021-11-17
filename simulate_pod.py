import sys
import click
from lib import CANBus, CANFrame, ARBITRATION_IDS, STATE_IDS

def watch_acks_on_rx(state_acks):
    def on_rx(frame, timestamp):
        if frame.arb_id == ARBITRATION_IDS["BMS_STATE_CHANGE"]:
            if frame.payload[0] == STATE_IDS["LV_READY"]:
                state_acks[0] = True
    return on_rx

@click.command()
@click.option("--interface", help = "ex. can0", required = True)
def simulate_pod(interface):
    with CANBus(interface) as bus:
        state_acks = [False]
        bus.set_rx_callback(watch_acks_on_rx(state_acks))

        while (1):
            req_state = input("Enter state: ")
            if req_state not in STATE_IDS.keys():
                print("Error: received invalid state name...\n")
                continue

            print(f"sending STATE_CHANGE_REQ with STATE_ID = {STATE_IDS[req_state]}")
            frame = CANFrame(ARBITRATION_IDS["CONTROLLER_COMMAND"], STATE_IDS[req_state])
            bus.put_frame(frame)

            print("waiting for ACK...")
            if req_state in ["ARMED", "AUTO_PILOT", "BREAKING", "EMERGENCY_BRAKE"]
            while not state_acks[0]:
                pass

            print(f"ACK received, transitioned to {STATE_IDS[req]}")


if __name__ == "__main__":
    try:
        simulate_pod()
    except KeyboardInterrupt:
        sys.exit(0)


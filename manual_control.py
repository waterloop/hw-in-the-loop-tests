import sys
import click
from lib import CANBus, CANFrame, ARBITRATION_IDS, STATE_IDS, get_state_name

def watch_acks_on_rx(waiting_state):
    def on_rx(frame, timestamp):
        if frame.arb_id == ARBITRATION_IDS["BMS_STATE_CHANGE"]:
            if frame.payload[0] == waiting_state['state']:
                waiting_state["ack"] = True
    return on_rx

def state_change(bus, waiting_state, target_state):
    initial_state = waiting_state["state"]

    waiting_state["state"] = target_state
    waiting_state["ack"] = False

    frame = CANFrame(ARBITRATION_IDS["CONTROLLER_COMMAND"], [target_state])
    bus.put_frame(frame)

    print(f"Waiting for transition from {get_state_name(initial_state)} to {get_state_name(target_state)}")

    while not waiting_state["ack"]:
        pass

    print(f"Transition to {get_state_name(target_state)} success")

@click.command()
@click.option("--interface", help = "ex. can0", required = True)
def manual_control(interface):
    with CANBus(interface) as bus:

        waiting_state = {
            "state": 0x00,
            "ack": False
        }
        bus.set_rx_callback(watch_acks_on_rx(waiting_state))

        state_change(bus, waiting_state, STATE_IDS["LV_READY"])
        state_change(bus, waiting_state, STATE_IDS["ARMED"])
        state_change(bus, waiting_state, STATE_IDS["MANUAL_OPERATION_WAITING"])

        print("Manual Operation Started")
        print("-" * 30)

        while(1):
            throttle = input("Enter target throttle percentage: ")
            
            # Set up manual control frame -> We could import the roboteq 
            # commands and send them here for manual control
            frame = CANFrame(ARBITRATION_IDS["MANUAL_CONTROL"], [0x00])
            bus.put_frame(frame)





if __name__ == "__main__":
    try:
        manual_control()
    except KeyboardInterrupt:
        sys.exit(0)


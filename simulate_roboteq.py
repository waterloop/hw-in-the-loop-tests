import sys
import time
import click
from lib import CANBus, CANFrame

def on_rx(frame, timestamp):
    frame_dict = frame.to_dict()
    print(f"received {frame_dict} at {str(timestamp)}\n")

@click.command()
@click.option("--interface", help = "ex. can0", required = True)
def simulate_roboteq(interface):
    with CANBus(interface) as bus:
        bus.set_rx_callback(on_rx)

        while (1):
            bus.send_set_motor_command(node_id = 1, motor = 1, throttle_percent = 50)
            time.sleep(100E-3)


if __name__ == "__main__":
    try:
        simulate_roboteq()
    except KeyboardInterrupt:
        sys.exit(0)


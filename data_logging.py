import csv
import sys
import time
import click
from lib import CANBus, print_can_msg

def on_rx(frame, timestamp):
    frame_dict = frame.to_dict()
    print_can_msg(frame)

@click.command()
@click.option("--interface", help = "ex. can0", required = True)
def data_logging(interface):
    with CANBus(interface) as bus:
        bus.set_rx_callback(on_rx)

        while (1):
            pass


if __name__ == "__main__":
    try:
        data_logging()
    except KeyboardInterrupt:
        sys.exit(0)


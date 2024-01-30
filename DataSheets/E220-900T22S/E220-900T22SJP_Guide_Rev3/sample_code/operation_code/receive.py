import serial
import time
import argparse
import hexdump


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("serial_port")
    parser.add_argument("-b", "--baud", default="9600")
    parser.add_argument("-m", "--model", default="E220-900JP")
    parser.add_argument("--rssi", action="store_true")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    if args.model == "E220-900JP":
        print("serial port:")
        print(args.serial_port)

        print("receive waiting...")
        with serial.Serial(args.serial_port, int(args.baud), timeout=None) as ser:
            payload = bytes()
            while True:
                if ser.in_waiting != 0:
                    payload = payload + ser.read()
                elif ser.in_waiting == 0 and len(payload) != 0:
                    time.sleep(0.030)
                    if ser.in_waiting == 0:
                        print("recv data hex dump:")
                        hexdump.hexdump(payload)
                        if args.rssi:
                            rssi = int(payload[-1]) - 256
                            print(f"RSSI: {rssi} dBm")
                        print("RECEIVED\n")
                        payload = bytes()
    else:
        print("INVALID")
        return


if __name__ == "__main__":
    main()

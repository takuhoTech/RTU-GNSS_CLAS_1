import serial
import sys
import argparse
import hexdump


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("serial_port")
    parser.add_argument("-b", "--baud", default="9600")
    parser.add_argument("-m", "--model", default="E220-900JP")
    parser.add_argument("-p", "--payload_length")
    parser.add_argument("-a", "--ascii_text")
    parser.add_argument("-f", "--fixed_mode", action="store_true")
    parser.add_argument("--target_address")
    parser.add_argument("--target_channel")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    if args.model == "E220-900JP":
        if args.fixed_mode:
            if (args.target_address != None) and (args.target_channel != None):
                t_addr = int(args.target_address)
                t_addr_H = t_addr >> 8
                t_addr_L = t_addr & 0xFF
                t_ch = int(args.target_channel)
                payload = bytes([t_addr_H, t_addr_L, t_ch])
            else:
                print("INVALID")
                return
        else:
            payload = bytes([])

        if args.payload_length != None:
            count = int(args.payload_length) // 256
            if count > 0:
                payload = payload + bytes(range(256))
                for i in range(count - 1):
                    payload = payload + bytes(range(256))
                payload = payload + bytes(range(int(args.payload_length) % 256))
            else:
                payload = payload + bytes(range(int(args.payload_length)))
        elif args.ascii_text != None:
            payload = payload + args.ascii_text.encode()
        else:
            payload = payload + sys.stdin.buffer.read()

        print("serial port:")
        print(args.serial_port)

        print("send data hex dump:")
        hexdump.hexdump(payload)

        with serial.Serial(args.serial_port, int(args.baud), timeout=None) as ser:
            while True:
                if ser.out_waiting == 0:
                    break
            ser.write(payload)
            ser.flush()
            print("SENT")
    else:
        print("INVALID")
        return


if __name__ == "__main__":
    main()

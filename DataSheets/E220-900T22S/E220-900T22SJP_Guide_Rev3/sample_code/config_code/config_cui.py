import serial
import struct
import time
import argparse
import configparser


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("serial_port")
    parser.add_argument("-m", "--model", default="E220-900JP")
    parser.add_argument("-r", "--read", action="store_true")
    parser.add_argument("-w", "--write", action="store_true")
    parser.add_argument("-a", "--start_addr")
    parser.add_argument("-l", "--length")
    parser.add_argument("-p", "--params", nargs="*")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--apply", action="store_true")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    ser = serial.Serial(args.serial_port, timeout=None)

    if args.model == "E220-900JP":
        if args.write:  # レジスタ書き込み
            if args.start_addr == None or args.params == None:
                print("INVALID")
                return

            length = len(args.params)
            params_list = []
            for i in args.params:
                params_list.append(int(i, 16))

            command = [0xC0, int(args.start_addr, 16), length] + params_list
            response = []

            for value in command:
                data = struct.pack("B", value)
                ser.write(data)

            ser.flush()
            time.sleep(1)

            while ser.in_waiting:
                value = ser.read()
                data = struct.unpack("B", value)
                response.append("0x" + format(data[0], "02x"))

            print(response)

            ser.close()

        elif args.read:  # レジスタ読み込み
            if args.start_addr == None or args.length == None:
                print("INVALID")
                return

            command = [0xC1, int(args.start_addr, 16), int(args.length, 16)]
            response = []

            for value in command:
                data = struct.pack("B", value)
                ser.write(data)

            ser.flush()
            time.sleep(1)

            while ser.in_waiting:
                value = ser.read()
                data = struct.unpack("B", value)
                response.append("0x" + format(data[0], "02x"))

            print(response)

            ser.close()

        elif args.list:  # 現在のパラメータ設定状態を一覧出力
            command = [0xC1, 0x00, 0x08]
            response = []

            print("# Command Request")
            command_hex = list(map(lambda n: "0x" + format(n, "02x"), command))
            print(command_hex)

            for value in command:
                data = struct.pack("B", value)
                ser.write(data)

            ser.flush()
            time.sleep(1)

            while ser.in_waiting:
                value = ser.read()
                data = struct.unpack("B", value)
                response.append("0x" + format(data[0], "02x"))

            print("# Command Response")
            print(response)

            print()
            print("現在の設定一覧")

            _, _, _, ADDH, ADDL, REG0, REG1, REG2, REG3, CRYPT_H, CRYPT_L = response

            ADDH = int(ADDH, 16) << 8
            ADDL = int(ADDL, 16)
            address = ADDH + ADDL
            print(f'Address             : 0x{format(address, "04x")}')

            REG0 = int(REG0, 16)

            UART = REG0 & 0b1110_0000
            UART = UART >> 5
            uart_setting = {
                0b000: "1200bps",
                0b001: "2400bps",
                0b010: "4800bps",
                0b011: "9600bps",
                0b100: "19200bps",
                0b101: "38400bps",
                0b110: "57600bps",
                0b111: "115200bps",
            }
            print(f"UART                : {uart_setting[UART]}")

            AIR_DATA_RATE = REG0 & 0b0001_1111
            BW = REG0 & 0b0000_0011
            air_data_rate_setting = {
                0b00000: "15,625bps, SF: 5, BW:125kHz",
                0b00100: " 9,375bps, SF: 6, BW:125kHz",
                0b01000: " 5,469bps, SF: 7, BW:125kHz",
                0b01100: " 3,125bps, SF: 8, BW:125kHz",
                0b10000: " 1,758bps, SF: 9, BW:125kHz",
                0b00001: "31,250bps, SF: 5, BW:250kHz",
                0b00101: "18,750bps, SF: 6, BW:250kHz",
                0b01001: "10,938bps, SF: 7, BW:250kHz",
                0b01101: " 6,250bps, SF: 8, BW:250kHz",
                0b10001: " 3,516bps, SF: 9, BW:250kHz",
                0b10101: " 1,953bps, SF:10, BW:250kHz",
                0b00010: "62,500bps, SF: 5, BW:500kHz",
                0b00110: "37,500bps, SF: 6, BW:500kHz",
                0b01010: "21,875bps, SF: 7, BW:500kHz",
                0b01110: "12,500bps, SF: 8, BW:500kHz",
                0b10010: " 7,031bps, SF: 9, BW:500kHz",
                0b10110: " 3,906bps, SF:10, BW:500kHz",
                0b11010: " 2,148bps, SF:11, BW:500kHz",
            }
            print(
                f"Air Data Rate       : {air_data_rate_setting[AIR_DATA_RATE].strip()}"
            )

            REG1 = int(REG1, 16)

            SUB_PACKET_LEN = REG1 & 0b1100_0000
            SUB_PACKET_LEN = SUB_PACKET_LEN >> 6
            sub_packet_setting = {
                0b00: "200bytes",
                0b01: "128bytes",
                0b10: "64bytes",
                0b11: "32bytes",
            }
            print(f"Sub Packet Size     : {sub_packet_setting[SUB_PACKET_LEN]}")

            RSSI_AMBIENT = REG1 & 0b0010_0000
            RSSI_AMBIENT = RSSI_AMBIENT >> 5
            rssi_ambient_setting = {
                0b0: "Disable",
                0b1: "Enable",
            }
            print(f"RSSI Ambient noise  : {rssi_ambient_setting[RSSI_AMBIENT]}")

            # TRANSMIT_PAUSE = REG1 & 0b0001_0000
            # TRANSMIT_PAUSE = TRANSMIT_PAUSE >> 4
            # transmit_pause_setting = {
            #     0b0: 'Enable',
            #     0b1: 'Disable',
            # }
            # print(
            #     f'Transmission pause  : {transmit_pause_setting[TRANSMIT_PAUSE]}'
            # )

            TRANSMIT_POWER = REG1 & 0b0000_0011
            transmit_power_setting = {
                0b00: "Unavailable",
                0b01: "13dBm",
                0b10: "7dBm",
                0b11: "0dBm",
            }
            print(f"Transmitting Power  : {transmit_power_setting[TRANSMIT_POWER]}")

            CH = int(REG2, 16)

            if BW == 0b00:
                frequency = 920.6 + CH * 0.2
            elif BW == 0b01:
                frequency = 920.7 + CH * 0.2
            elif BW == 0b10:
                frequency = 920.8 + CH * 0.2

            print(f"CH                  : {CH}")
            print(f"Actual frequency    : {frequency:.1f}MHz")

            REG3 = int(REG3, 16)

            RSSI_BYTE = REG3 & 0b1000_0000
            RSSI_BYTE = RSSI_BYTE >> 7
            rssi_byte_setting = {
                0b0: "Disable",
                0b1: "Enable",
            }
            print(f"RSSI Byte           : {rssi_byte_setting[RSSI_BYTE]}")

            TRANSMIT_METHOD = REG3 & 0b0100_0000
            TRANSMIT_METHOD = TRANSMIT_METHOD >> 6
            transmit_method_setting = {
                0b0: "Transparent transmission mode",
                0b1: "Fixed transmission mode",
            }
            print(f"Transmission Method : {transmit_method_setting[TRANSMIT_METHOD]}")

            # LBT = REG3 & 0b0001_0000
            # LBT = LBT >> 4
            # lbt_setting = {
            #     0b0: 'Enable',
            #     0b1: 'Disable',
            # }
            # print(f'LBT                 : {lbt_setting[LBT]}')

            WOR_CYCLE = REG3 & 0b0000_0111
            wor_cycle_setting = {
                0b000: "500ms",
                0b001: "1000ms",
                0b010: "1500ms",
                0b011: "2000ms",
                0b100: "2500ms",
                0b101: "3000ms",
                0b110: "3500ms",
                0b111: "4000ms",
            }
            print(f"WOR Cycle           : {wor_cycle_setting[WOR_CYCLE]}")

            ser.close()

        elif args.apply:  # 設定ファイルを適用
            inifile = configparser.ConfigParser()
            inifile.read("setting.ini")

            command = [0xC0, 0x00, 0x08]

            # 設定ファイルから読み込み
            own_address = inifile.get("E220-900JP", "own_address")
            baud_rate = inifile.get("E220-900JP", "baud_rate")
            bw = inifile.get("E220-900JP", "bw")
            sf = inifile.get("E220-900JP", "sf")
            subpacket_size = inifile.get("E220-900JP", "subpacket_size")
            rssi_ambient_noise_flag = inifile.get(
                "E220-900JP", "rssi_ambient_noise_flag"
            )
            transmitting_power = inifile.get("E220-900JP", "transmitting_power")
            own_channel = inifile.get("E220-900JP", "own_channel")
            rssi_byte_flag = inifile.get("E220-900JP", "rssi_byte_flag")
            transmission_method_type = inifile.get(
                "E220-900JP", "transmission_method_type"
            )
            wor_cycle = inifile.get("E220-900JP", "wor_cycle")
            encryption_key = inifile.get("E220-900JP", "encryption_key")

            # Address 00H, 01H
            # own_address
            own_address = int(own_address)
            ADDH = own_address >> 8
            ADDL = own_address & 0b1111_1111
            command.append(ADDH)
            command.append(ADDL)

            # Address 02H
            REG0 = 0

            # baud_rate
            baud_rate = int(baud_rate)

            baud_rate_bit = {
                1200: 0b000,
                2400: 0b001,
                4800: 0b010,
                9600: 0b011,
                19200: 0b100,
                38400: 0b101,
                57600: 0b110,
                115200: 0b111,
            }

            if baud_rate in baud_rate_bit:
                baud_rate = baud_rate_bit[baud_rate]
            else:
                baud_rate = baud_rate_bit[9600]

            baud_rate = baud_rate << 5
            REG0 = REG0 | baud_rate

            # air_data_rate
            bw = int(bw)
            sf = int(sf)
            air_data_rate = (bw, sf)

            air_data_rate_bit = {
                (125, 5): 0b00000,
                (125, 6): 0b00100,
                (125, 7): 0b01000,
                (125, 8): 0b01100,
                (125, 9): 0b10000,
                (250, 5): 0b00001,
                (250, 6): 0b00101,
                (250, 7): 0b01001,
                (250, 8): 0b01101,
                (250, 9): 0b10001,
                (250, 10): 0b10101,
                (500, 5): 0b00010,
                (500, 6): 0b00110,
                (500, 7): 0b01010,
                (500, 8): 0b01110,
                (500, 9): 0b10010,
                (500, 10): 0b10110,
                (500, 11): 0b11010,
            }

            if air_data_rate in air_data_rate_bit:
                air_data_rate = air_data_rate_bit[air_data_rate]
            else:
                air_data_rate = air_data_rate_bit[(125, 7)]

            REG0 = REG0 | air_data_rate
            command.append(REG0)

            # Address 03H
            REG1 = 0

            # subpacket_size
            subpacket_size = int(subpacket_size)

            subpacket_size_bit = {200: 0b00, 128: 0b01, 64: 0b10, 32: 0b11}

            if subpacket_size in subpacket_size_bit:
                subpacket_size = subpacket_size_bit[subpacket_size]
            else:
                subpacket_size = subpacket_size_bit[200]

            subpacket_size = subpacket_size << 6
            REG1 = REG1 | subpacket_size

            # rssi_ambient_noise_flag
            rssi_ambient_noise_flag = int(rssi_ambient_noise_flag)

            if rssi_ambient_noise_flag == 0:
                rssi_ambient_noise_flag = 0b0
            elif rssi_ambient_noise_flag == 1:
                rssi_ambient_noise_flag = 0b1
            else:
                rssi_ambient_noise_flag = 0b0

            rssi_ambient_noise_flag = rssi_ambient_noise_flag << 5
            REG1 = REG1 | rssi_ambient_noise_flag

            # # transmission_pause_flag
            # transmission_pause_flag = int(transmission_pause_flag)

            # if transmission_pause_flag == 0:
            #     transmission_pause_flag = 0b1
            # elif transmission_pause_flag == 1:
            #     transmission_pause_flag = 0b0
            # else:
            #     transmission_pause_flag = 0b0

            # transmission_pause_flag = transmission_pause_flag << 4
            # REG1 = REG1 | transmission_pause_flag

            # transmitting_power
            transmitting_power = int(transmitting_power)

            transmitting_power_bit = {13: 0b01, 7: 0b10, 0: 0b11}

            if transmitting_power in transmitting_power_bit:
                transmitting_power = transmitting_power_bit[transmitting_power]
            else:
                transmitting_power = transmitting_power_bit[13]

            REG1 = REG1 | transmitting_power
            command.append(REG1)

            # Address 04H
            # own_channel
            REG2 = 0

            own_channel = int(own_channel)

            if bw == 125:
                if 0 < own_channel < 37:
                    pass
                else:
                    own_channel = 0
            elif bw == 250:
                if 0 < own_channel < 36:
                    pass
                else:
                    own_channel = 0
            elif bw == 500:
                if 0 < own_channel < 30:
                    pass
                else:
                    own_channel = 0
            else:
                own_channel = 0

            REG2 = REG2 | own_channel
            command.append(REG2)

            # Address 05H
            REG3 = 0

            # rssi_byte_flag
            rssi_byte_flag = int(rssi_byte_flag)

            if rssi_byte_flag == 0:
                rssi_byte_flag = 0b0
            elif rssi_byte_flag == 1:
                rssi_byte_flag = 0b1
            else:
                rssi_byte_flag = 0b1

            rssi_byte_flag = rssi_byte_flag << 7
            REG3 = REG3 | rssi_byte_flag

            # transmission_method_type
            transmission_method_type = int(transmission_method_type)

            if transmission_method_type == 1:
                transmission_method_type = 0b0
            elif transmission_method_type == 2:
                transmission_method_type = 0b1
            else:
                transmission_method_type = 0b1

            transmission_method_type = transmission_method_type << 6
            REG3 = REG3 | transmission_method_type

            # # lbt_flag
            # lbt_flag = int(lbt_flag)

            # if lbt_flag == 0:
            #     lbt_flag = 0b1
            # elif lbt_flag == 1:
            #     lbt_flag = 0b0
            # else:
            #     lbt_flag = 0b0

            # lbt_flag = lbt_flag << 4
            # REG3 = REG3 | lbt_flag

            # wor_cycle
            wor_cycle = int(wor_cycle)

            wor_cycle_bit = {
                500: 0b000,
                1000: 0b001,
                1500: 0b010,
                2000: 0b011,
                2500: 0b100,
                3000: 0b101,
                3500: 0b110,
                4000: 0b111,
            }

            if wor_cycle in wor_cycle_bit:
                wor_cycle = wor_cycle_bit[wor_cycle]
            else:
                wor_cycle = wor_cycle_bit[2000]

            REG3 = REG3 | wor_cycle
            command.append(REG3)

            # Address 06H, 07H
            # encryption_key
            encryption_key = int(encryption_key)
            CRYPT_H = encryption_key >> 8
            CRYPT_L = encryption_key & 0b1111_1111
            command.append(CRYPT_H)
            command.append(CRYPT_L)

            print("# Command Request")
            command_hex = list(map(lambda n: "0x" + format(n, "02x"), command))
            print(command_hex)

            for value in command:
                data = struct.pack("B", value)
                ser.write(data)

            ser.flush()
            time.sleep(1)

            response = []

            while ser.in_waiting:
                value = ser.read()
                data = struct.unpack("B", value)
                response.append("0x" + format(data[0], "02x"))

            print("# Command Response")
            print(response)

            ser.close()

        else:
            print("INVALID")
            return
    else:
        print("INVALID")
        return


if __name__ == "__main__":
    main()

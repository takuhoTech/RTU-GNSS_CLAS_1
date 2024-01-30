import PySimpleGUI as sg
import sys
import glob
import serial
import struct
import time

serial_port_values = []
uart_values = ["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
bw_values = ["125", "250", "500"]
sf_values = ["5", "6", "7", "8", "9", "10", "11"]
sub_packet_values = ["200", "128", "64", "32"]
on_off_values = ["有効", "無効"]
transmitting_power_values = ["Unavailable", "13", "7", "0"]
transmission_method_values = ["トランスペアレント送信モード", "固定送信モード"]
wor_cycle_values = ["500", "1000", "1500", "2000", "2500", "3000", "3500", "4000"]


def serial_ports():
    """Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def serial_open(port):
    try:
        ser = serial.Serial(port)
    except (OSError, serial.SerialException):
        return None

    return ser


def serial_close(ser: serial.Serial):
    try:
        ser.close()
    except (OSError, serial.SerialException):
        pass


def load_parameters(ser: serial.Serial, window: sg.Window):
    try:
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

        _, _, _, ADDH, ADDL, REG0, REG1, REG2, REG3, CRYPT_H, CRYPT_L = response

        ADDH = int(ADDH, 16) << 8
        ADDL = int(ADDL, 16)
        address = ADDH + ADDL
        window["addr"].update(address, disabled=False, text_color="#000000")

        REG0 = int(REG0, 16)

        UART = REG0 & 0b1110_0000
        UART = UART >> 5
        window["uart_combo"].update(uart_values[UART], disabled=False)

        SF = REG0 & 0b0001_1100
        SF = SF >> 2
        BW = REG0 & 0b0000_0011
        window["bw_combo"].update(bw_values[BW], disabled=False)
        window["sf_combo"].update(sf_values[SF], disabled=False)

        REG1 = int(REG1, 16)

        SUB_PACKET_LEN = REG1 & 0b1100_0000
        SUB_PACKET_LEN = SUB_PACKET_LEN >> 6
        window["sub_packet_combo"].update(
            sub_packet_values[SUB_PACKET_LEN], disabled=False
        )

        RSSI_AMBIENT = REG1 & 0b0010_0000
        RSSI_AMBIENT = RSSI_AMBIENT >> 5
        window["rssi_ambient_combo"].update(
            on_off_values[int(not RSSI_AMBIENT)], disabled=False
        )

        # TRANSMIT_PAUSE = REG1 & 0b0001_0000
        # TRANSMIT_PAUSE = TRANSMIT_PAUSE >> 4
        # window["transmission_pause_combo"].update(on_off_values[TRANSMIT_PAUSE], disabled=False)

        TRANSMIT_POWER = REG1 & 0b0000_0011
        window["transmitting_power_combo"].update(
            transmitting_power_values[TRANSMIT_POWER], disabled=False
        )

        CH = int(REG2, 16)
        window["channel"].update(CH, disabled=False, text_color="#000000")

        if BW == 0b00:
            frequency = 920.6 + CH * 0.2
        elif BW == 0b01:
            frequency = 920.7 + CH * 0.2
        elif BW == 0b10:
            frequency = 920.8 + CH * 0.2
        window["freq"].update(f"Frequency: {frequency:.1f}MHz")

        REG3 = int(REG3, 16)

        RSSI_BYTE = REG3 & 0b1000_0000
        RSSI_BYTE = RSSI_BYTE >> 7
        window["rssi_byte_combo"].update(
            on_off_values[int(not RSSI_BYTE)], disabled=False
        )

        TRANSMIT_METHOD = REG3 & 0b0100_0000
        TRANSMIT_METHOD = TRANSMIT_METHOD >> 6
        window["transmission_method_combo"].update(
            transmission_method_values[TRANSMIT_METHOD], disabled=False
        )

        # LBT = REG3 & 0b0001_0000
        # LBT = LBT >> 4
        # window["lbt_combo"].update(on_off_values[LBT], disabled=False)

        WOR_CYCLE = REG3 & 0b0000_0111
        window["wor_cycle_combo"].update(wor_cycle_values[WOR_CYCLE], disabled=False)

        CRYPT_H = int(CRYPT_H, 16) << 8
        CRYPT_L = int(CRYPT_L, 16)
        key = CRYPT_H + CRYPT_L
        window["encryption_key"].update(key, disabled=False, text_color="#000000")
    except Exception as e:
        sg.popup("Module not responding.")
        return False
    else:
        sg.popup("Loading parameters succeeded.")
        return True


def write_parameters(ser: serial.Serial, window: sg.Window, values):
    try:
        command = [0xC0, 0x00, 0x08]
        response = []

        # 読み込み
        address = int(values["addr"])
        uart = uart_values.index(values["uart_combo"])
        bw = bw_values.index(values["bw_combo"])
        sf = sf_values.index(values["sf_combo"])
        sub_packet_size = sub_packet_values.index(values["sub_packet_combo"])
        rssi_ambient_noise = int(not on_off_values.index(values["rssi_ambient_combo"]))
        # transmission_pause = on_off_values.index(values["transmission_pause_combo"])
        transmitting_power = transmitting_power_values.index(
            values["transmitting_power_combo"]
        )
        ch = int(values["channel"])
        rssi_byte = int(not on_off_values.index(values["rssi_byte_combo"]))
        transmission_method = transmission_method_values.index(
            values["transmission_method_combo"]
        )
        # lbt = on_off_values.index(values["lbt_combo"])
        wor_cycle = wor_cycle_values.index(values["wor_cycle_combo"])
        key = int(values["encryption_key"])

        # Address 00H, 01H
        ADDH = address >> 8
        ADDL = address & 0b1111_1111
        command.append(ADDH)
        command.append(ADDL)

        # Address 02H
        REG0 = 0

        uart = uart << 5
        REG0 = REG0 | uart

        sf = sf << 2
        air_data_rate = sf | bw
        REG0 = REG0 | air_data_rate
        command.append(REG0)

        # Address 03H
        REG1 = 0

        sub_packet_size = sub_packet_size << 6
        REG1 = REG1 | sub_packet_size

        rssi_ambient_noise = rssi_ambient_noise << 5
        REG1 = REG1 | rssi_ambient_noise

        # transmission_pause = transmission_pause << 4
        # REG1 = REG1 | transmission_pause

        REG1 = REG1 | transmitting_power
        command.append(REG1)

        # Address 04H
        REG2 = 0

        REG2 = ch

        if bw == 0b00:
            frequency = 920.6 + ch * 0.2
        elif bw == 0b01:
            frequency = 920.7 + ch * 0.2
        elif bw == 0b10:
            frequency = 920.8 + ch * 0.2
        window["freq"].update(f"Frequency: {frequency:.1f}MHz")

        command.append(REG2)

        # Address 05H
        REG3 = 0

        rssi_byte = rssi_byte << 7
        REG3 = REG3 | rssi_byte

        transmission_method = transmission_method << 6
        REG3 = REG3 | transmission_method

        # lbt = lbt << 4
        # REG3 = REG3 | lbt

        REG3 = REG3 | wor_cycle
        command.append(REG3)

        # Address 06H, 07H
        CRYPT_H = key >> 8
        CRYPT_L = key & 0b1111_1111
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

        while ser.in_waiting:
            value = ser.read()
            data = struct.unpack("B", value)
            response.append("0x" + format(data[0], "02x"))

        print("# Command Response")
        print(response)
    except Exception as e:
        sg.popup("Writing parameters failed.")
    else:
        sg.popup("Writing parameters succeeded.")


def reset_parameters(window: sg.Window):
    window["addr"].update(0)
    window["uart_combo"].update(uart_values[3])
    window["bw_combo"].update(bw_values[2])
    window["sf_combo"].update(sf_values[0])
    window["sub_packet_combo"].update(sub_packet_values[0])
    window["rssi_ambient_combo"].update(on_off_values[1])
    # window["transmission_pause_combo"].update(on_off_values[0])
    window["transmitting_power_combo"].update(transmitting_power_values[1])
    window["channel"].update(0)
    frequency = 920.6 + 0 * 0.2
    window["freq"].update(f"Frequency: {frequency:.1f}MHz")
    window["rssi_byte_combo"].update(on_off_values[1])
    window["transmission_method_combo"].update(transmission_method_values[0])
    # window["lbt_combo"].update(on_off_values[0])
    window["wor_cycle_combo"].update(wor_cycle_values[3])
    window["encryption_key"].update(0)

    sg.popup("Restore default parameters.")


def reload_port(window: sg.Window, values):
    serial_port_values = serial_ports()

    if len(serial_port_values) == 0:
        serial_port_values = [""]

    window["serial_port_combo"].update(
        values=serial_port_values, value=serial_port_values[0]
    )


def create_layout():
    serial_port_values = serial_ports()

    if len(serial_port_values) == 0:
        serial_port_values = [""]

    layout = [
        [
            sg.Text("シリアルポート", size=14, justification="right"),
            sg.Combo(
                serial_port_values,
                default_value=serial_port_values[0],
                size=8,
                readonly=True,
                key="serial_port_combo",
            ),
            sg.Button("Open", size=6, key="port"),
            sg.Button("Reload", size=6, key="reload"),
        ],
        [
            sg.Text("アドレス", size=14, justification="right"),
            sg.Input(size=8, disabled=True, key="addr"),
        ],
        [
            sg.Text("UART", size=14, justification="right"),
            sg.Combo(
                uart_values, size=8, readonly=True, disabled=True, key="uart_combo"
            ),
            sg.Text("bps"),
        ],
        [
            sg.Text("SF", size=14, justification="right"),
            sg.Combo(sf_values, size=8, readonly=True, disabled=True, key="sf_combo"),
        ],
        [
            sg.Text("BW", size=14, justification="right"),
            sg.Combo(bw_values, size=8, readonly=True, disabled=True, key="bw_combo"),
            sg.Text("kHz"),
        ],
        [
            sg.Text("サブパケット長", size=14, justification="right"),
            sg.Combo(
                sub_packet_values,
                size=8,
                readonly=True,
                disabled=True,
                key="sub_packet_combo",
            ),
            sg.Text("bytes"),
        ],
        [
            sg.Text("RSSI環境ノイズ", size=14, justification="right"),
            sg.Combo(
                on_off_values,
                size=8,
                readonly=True,
                disabled=True,
                key="rssi_ambient_combo",
            ),
        ],
        # [sg.Text("送信休止時間", size=14, justification="right"), sg.Combo(on_off_values, size=8, readonly=True, disabled=True, key="transmission_pause_combo")],
        [
            sg.Text("送信電力", size=14, justification="right"),
            sg.Combo(
                transmitting_power_values,
                size=8,
                readonly=True,
                disabled=True,
                key="transmitting_power_combo",
            ),
            sg.Text("dBm"),
        ],
        [
            sg.Text("周波数チャネル", size=14, justification="right"),
            sg.Input(size=8, disabled=True, key="channel"),
            sg.Text(size=(20, 1), key="freq"),
        ],
        [
            sg.Text("RSSIバイト", size=14, justification="right"),
            sg.Combo(
                on_off_values,
                size=8,
                readonly=True,
                disabled=True,
                key="rssi_byte_combo",
            ),
        ],
        [
            sg.Text("送信方法", size=14, justification="right"),
            sg.Combo(
                transmission_method_values,
                size=29,
                readonly=True,
                disabled=True,
                key="transmission_method_combo",
            ),
        ],
        # [sg.Text("LBT", size=14, justification="right"), sg.Combo(on_off_values, size=8, readonly=True, disabled=True, key="lbt_combo")],
        [
            sg.Text("WORサイクル", size=14, justification="right"),
            sg.Combo(
                wor_cycle_values,
                size=8,
                readonly=True,
                disabled=True,
                key="wor_cycle_combo",
            ),
            sg.Text("ms"),
        ],
        [
            sg.Text("暗号化キー", size=14, justification="right"),
            sg.Input(size=8, disabled=True, key="encryption_key"),
        ],
        [
            sg.Button("Get", size=10, key="get_button", disabled=True),
            sg.Button("Set Param", size=10, key="set_button", disabled=True),
            sg.Button("Param Reset", size=10, key="reset_button", disabled=True),
        ],
    ]

    return layout


def main():
    layout = create_layout()
    window = sg.Window("E220-900T22S(JP) Config", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            if window["port"].get_text() == "Close":
                serial_close(ser)
            break
        elif event == "port" and window["port"].get_text() == "Open":
            ser = serial_open(window["serial_port_combo"].get())
            if ser == None:
                sg.popup("Failed to open serial port!!!")
                continue
            window["get_button"].update(disabled=False)
            window["serial_port_combo"].update(disabled=True)
            window["reload"].update(disabled=True)
            window["port"].update("Close")
        elif event == "port" and window["port"].get_text() == "Close":
            serial_close(ser)
            window["get_button"].update(disabled=True)
            window["set_button"].update(disabled=True)
            window["reset_button"].update(disabled=True)
            window["serial_port_combo"].update(disabled=False)
            window["reload"].update(disabled=False)
            window["addr"].update(disabled=True, text_color="#7f7f7f")
            window["uart_combo"].update(disabled=True)
            window["bw_combo"].update(disabled=True)
            window["sf_combo"].update(disabled=True)
            window["sub_packet_combo"].update(disabled=True)
            window["rssi_ambient_combo"].update(disabled=True)
            # window["transmission_pause_combo"].update(disabled=True)
            window["transmitting_power_combo"].update(disabled=True)
            window["channel"].update(disabled=True, text_color="#7f7f7f")
            window["rssi_byte_combo"].update(disabled=True)
            window["transmission_method_combo"].update(disabled=True)
            # window["lbt_combo"].update(disabled=True)
            window["wor_cycle_combo"].update(disabled=True)
            window["encryption_key"].update(disabled=True, text_color="#7f7f7f")
            window["port"].update("Open")
        elif event == "reload":
            reload_port(window, values)
        elif event == "get_button":
            if load_parameters(ser, window):
                window["set_button"].update(disabled=False)
                window["reset_button"].update(disabled=False)
        elif event == "set_button":
            write_parameters(ser, window, values)
        elif event == "reset_button":
            reset_parameters(window)


if __name__ == "__main__":
    main()

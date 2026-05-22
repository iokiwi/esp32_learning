# ESP32 C3 Mini Development Board Learning

A huge shout out to this resource for helping piece things together [Kevin's Blog | ESP32-C3 0.42 OLED](https://emalliab.wordpress.com/2025/02/12/esp32-c3-0-42-oled/)

![Image](https://emalliab.wordpress.com/wp-content/uploads/2025/02/image-1.png?w=2000&h=)


## Initial Setup

1. Download and install [Thonny - Python IDE for beginners](https://thonny.org/) 


Tools
 * [esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32c3/)

Get [esptool](https://pypi.org/project/esptool/) - "A Python-based, open-source, platform-independent serial utility for flashing, provisioning, and interacting with Espressif SoCs." [Espressive | Esptool Documentation | Quickstart](https://docs.espressif.com/projects/esptool/en/latest/esp32c3/#quick-start)

```bash
pip install esptool
```

Download the MicroPython Firmware from [MicroPython | C3 mini | Firmware](https://micropython.org/download/LOLIN_C3_MINI/)

At time of writing the latest is `v1.28.0 (2026-04-06).bin` which resulted in a download called `OLIN_C3_MINI-20260406-v1.28.0.bin`

Plugin the ESP32 to your laptop.

Figure out the serial port that the device. As described in [MicroPython | C3 mini | Installation Instructions](https://micropython.org/download/LOLIN_C3_MINI/)

> * On Linux, the port name is usually similar to `/dev/ttyACM0`.
> * On Mac, the port name is usually similar to `/dev/cu.usbmodem01`.
> * On Windows, the port name is usually similar `to COM4`

Erase the board. Since I am on a mac
```bash
$ esptool --port /dev/cu.usbmodem1101 erase_flash
```

Flash MicroPython onto the board
```bash
$ esptool --port /dev/cu.usbmodem1101 write_flash 0 ~/Downloads/OLIN_C3_MINI-20260406-v1.28.0.bin
```
```
Warning: Deprecated: Command 'write_flash' is deprecated. Use 'write-flash' instead.
esptool v5.2.0
Connected to ESP32-C3 on /dev/cu.usbmodem1101:
Chip type:          ESP32-C3 (QFN32) (revision v0.4)
Features:           Wi-Fi, BT 5 (LE), Single Core, 160MHz, Embedded Flash 4MB (XMC)
Crystal frequency:  40MHz
USB mode:           USB-Serial/JTAG
MAC:                14:63:93:76:39:7c

Stub flasher running.

Configuring flash size...
Flash will be erased from 0x00000000 to 0x001a5fff...
Wrote 1724672 bytes (1035222 compressed) at 0x00000000 in 3.9 seconds (3513.7 kbit/s).
Hash of data verified.

Hard resetting via RTS pin...
```

# Connect to the board

## Thonny (easiest)
 [thonny](https://thonny.org/)

![img](docs/img/thonny_interpreter.png)

## mpremote
 * [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html)

List devices
```bash
$ mpremote devs
```
```
/dev/cu.usbmodem1101 14:63:93:76:39:7C 303a:1001 Espressif USB JTAG/serial debug unit
/dev/cu.Bluetooth-Incoming-Port None 0000:0000 None None
/dev/cu.debug-console None 0000:0000 None None
/dev/cu.wlan-debug None 0000:0000 None None
```

```bash
$ mpremote connect /dev/cu.usbmodem1101
Connected to MicroPython at /dev/cu.usbmodem1101
Use Ctrl-] or Ctrl-x to exit this shell

>>>
```

```python
 >>> help()
Welcome to MicroPython on the ESP32!

For online docs please visit http://docs.micropython.org/
[...]
```

## Installing Dependencies

```python
>>> import mip
>>> mip.install("urequests")
```

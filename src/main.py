import network
import time
import machine
import urequests
import _thread

from machine import Pin, I2C
import ssd1306

OLED_WIDTH = 128
OLED_HEIGHT = 64

# For some reason the visible frame doesn't start at 0, 0
OLED_OFFSET_X = 28
OLED_OFFSET_Y = 24

# Flash LED
LED_PIN = machine.Pin(8, machine.Pin.OUT)

def _x(x):
    return x + OLED_OFFSET_X

def _y(y):
    return y + OLED_OFFSET_Y


def flash_led(pin, reps=10, period=0.25):
    for i in range(reps*2):
        if i % 2 == 0:
            pin.value(0)
        else:
            pin.value(1)
        time.sleep(period)


def connect_to_wifi(ssid=None, password=None):
    sta_if = network.WLAN(network.WLAN.IF_STA)    # Get reference to station network interface
    sta_if.active(True)                           # Acivate interface

    nets = sta_if.scan()                          # Scan for available access points
    print("(ssid, bssid, channel, RSSI, security, hidden)")
    for net in nets:
        print(net)

    if not sta_if.isconnected():
        print("Connecting to '{ssid}'...")
        sta_if.connect(ssid, password)

        timeout = 10
        while not sta_if.isconnected() and timeout > 0:
            print(f"Attempts remaining {timeout}: Connecting to '{ssid}'...")
            flash_led(LED_PIN, reps=1, period=0.5);
            timeout -= 1            

    if sta_if.isconnected():
        private_ip_address = get_private_ip()
        print(f"Connected: {private_ip_address}")
        return True
    return False

def get_public_ip():
   _thread.start_new_thread(flash_led, (LED_PIN, 30, 0.1))
   response = urequests.get("http://icanhazip.com")  # NOTE: use HTTP, not HTTPS
   public_ip_address = response.text.strip()
   return public_ip_address

def get_private_ip():
    sta_if = network.WLAN(network.WLAN.IF_STA)    # Get reference to station network interface
    ip = sta_if.ifconfig()[0]
    return ip

flash_led(LED_PIN, reps=3, period=0.5)

WIFI_SSID = ""
WIFI_PASSWORD = ""

connect_to_wifi(
    ssid=WIFI_SSID,
    password=WIFI_PASSWORD
)

public_ip_address = get_public_ip()
private_ip_address = get_private_ip()

# Draw on the screen
i2c = machine.SoftI2C(scl=machine.Pin(6), sda=machine.Pin(5))
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

while True:
    oled.fill(0)
    oled.text("Hello,", _x(0), _y(0))
    oled.text("World!", _x(0), _y(10))
    oled.show()
    time.sleep(1)

    oled.fill(0)
    oled.text("Public", _x(0), _y(0))
    oled.text("IPv4", _x(0), _y(10))
    oled.text(".".join(public_ip_address.split(".")[:2]), _x(0), _y(20))
    oled.text(".".join(public_ip_address.split(".")[2:]), _x(0), _y(30))
    oled.show()
    time.sleep(4)
    
    oled.fill(0)
    oled.text("Private", _x(0), _y(0))
    oled.text("IPv4", _x(0), _y(10))
    oled.text(".".join(private_ip_address.split(".")[:2]), _x(0), _y(20))
    oled.text(".".join(private_ip_address.split(".")[2:]), _x(0), _y(30))
    oled.show()
    time.sleep(4)


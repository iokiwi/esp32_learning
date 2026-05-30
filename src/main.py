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

WIFI_SSID = ""
WIFI_PASSWORD = ""

LED_PIN = machine.Pin(8, machine.Pin.OUT)
AHT20_ADDR = 0x38

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

def draw_lines(lines=None, i2c=None, oled=None):
    
    if i2c is None:
        i2c = machine.SoftI2C(
            scl=machine.Pin(6),
            sda=machine.Pin(5)
        )

    if oled is None:
        oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

    oled.fill(0)
    y = 0
    for line in lines:
        oled.text(line, _x(0), _y(y))     
        y += 10
    oled.show()


def aht20_init(i2c):
    time.sleep_ms(40)
    i2c.writeto(AHT20_ADDR, b"\xBE\x08\x00")
    time.sleep_ms(10)

def aht20_read(i2c):
    i2c.writeto(AHT20_ADDR, b"\xAC\x33\x00")
    time.sleep_ms(80)

    data = i2c.readfrom(AHT20_ADDR, 6)

    raw_humidity = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
    raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

    humidity = raw_humidity * 100 / 1048576
    temperature = raw_temperature * 200 / 1048576 - 50

    return temperature, humidity


def show_ip():
    while True:
        draw_lines([
            "Public",
            "IPv4",
             ".".join(public_ip_address.split(".")[:2]),
             ".".join(public_ip_address.split(".")[2:]),
        ])
        sleep(3)        
        draw_lines([
            "Private",
            "IPv4",
            ".".join(private_ip_address.split(".")[:2]),
            ".".join(private_ip_address.split(".")[2:]),
        ])
        sleep(3)

def main():

    # connect_to_wifi(ssid=WIFI_SSID, password=WIFI_PASSWORD)
    # public_ip_address = get_public_ip()
    # private_ip_address = get_private_ip()

    i2c = machine.SoftI2C(
        scl=machine.Pin(6), # Serial Clock
        sda=machine.Pin(5), # Serial Data
        freq=100000,
    )

    print([hex(addr) for addr in i2c.scan()])
    aht20_init(i2c)
    
    while True:
        temperature, humidity = aht20_read(i2c)
        draw_lines(
            lines=[
                f"T {temperature:0.1f} C",
                f"H {humidity:0.1f} %"
            ],
            i2c=i2c,
        )
        print("Temperature: {:.1f} C".format(temperature))
        print("Humidity: {:.1f} %".format(humidity))
        time.sleep(2)
        #print("Deep sleeping in 3")
        #draw_lines(["3"])
        #time.sleep(1)
        #draw_lines(["2"])
        #time.sleep(1)
        #draw_lines(["1"])
        #time.sleep(1)
        #draw_lines(["       ", "       ", "       ", "       "])
        #machine.deepsleep(5_000)
        

main()

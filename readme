# Xmas lights in Bordel 

Workshop will guide you through setup of microcontroller with Micropython enviroment and using it to control Neopixel lights. 

## Prerequisties 

* Microcontroller with ESP8266 or ESP32 chip, for example NodeMCU
* Computer (preferably with Linux)
* Neopixel LED stripe - WS2812, WS2812B or WS2811 will do


# X-Lights Workshop

Workshop will guide you through setup of microcontroller with Micropython enviroment and using it to control Neopixel lights. 

# Prerequisites

## Hardware

- Board with ESP32 or ESP8266 chip (other microcontrollers such as Arduino or STM32 should work too)
- Solderless breadboard
- Wires for connections
- Neopixel LED stripe - WS2812, WS2812B or WS2811 will do
- DC power sources 5V/12V (up to 12V can be used to power the lights, but NOT the ESP, which has to be powered via USB in such a case!)
- Micro USB cable for connecting microcontroller with PC

(optionally)
- 1 mF capacitor
- 470 resistor

## Software

You will need to install [Python](https://www.python.org/downloads/) and pip on your computor. There is bunch of different tools in Python which can help us to use ESP microcontroller. To make it easier, we can use GUI IDE called [Thonny](https://thonny.org/). 

You can simply install it with pip for example:
```
pip3 install thonny
```
Other command tools installable with pip which can be helpfull are:

- esptool (flashing firmware)
- adafruit-ampy (copying, executing files)
- picom (terminal REPL prompt)

## Firmware
For this workshop, we will use [Micropython][micropython] enviroment. Download newest Micropython firmware suitable for your microcontroller. For example [here for ESP8266](https://micropython.org/download/esp8266/). 

# Preparing microcontroller

## GUI

Using Thonny, first go to `Tool -> Options -> Interpreter`. 
Here pick interpreter with Micropython for your chip and click on `Install or update firmware`. Make sure microcontroller is connected and pick USB port to communicate with it. Choose downloaded firmware from your drive and install it on microcontroller. This will take few seconds or minutes and your device is ready to be run code in Micropython. 

## Command line

Connect the microcontroller to your computer via data-USB cable. In the GNU/Linux it should appear as a port addressable by /dev/ttyUSB0.

To be in the same starting situation, we erase all the flash memory as
```
esptool.py --port /dev/ttyUSB0 erase_flash
```
Then we can upload the micropython firmware downloaded (e.g. espXXXX.bin) using:
```
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 espXXXX.bin
```

To get the micropython command line prompt we can use picocom
```
picocom /dev/ttyUSB0 --baud 115200
```

To upload, download, run code or act on the micro-Python file system run ampy, e.g.
```
ampy --port /dev/ttyUSB0 --baud 115200 put color.py
ampy --port /dev/ttyUSB0 --baud 115200 run ws2812.py
```
The boot.py or main.py will be run on the startup.

## Wiring and connecting lights

Place microcontroller on the breadboard, connect to computer and now let's connect Neopixel lights. 
* Ground (GND) of the microcontroller board and negative potential of lights power supply has to be connected. 
    * Make sure to connect these, otherwise, the signal won't get through properly and the lights will be incontrollable.
* Connect data wire to one of pin outputs on the board, for example D2.
    * Reffer to pinout
    * Optionally use small (300-500ohm) resistor between data wire and pin
* Coonect LEDs to power supply and optionally put capacitor between potentials

Now everything should be setup to blink your LEDs. 

## Hello Lights


To start with the lights we follow [the manual][upy] in Micropython documentation. According this manual the lights use the Machine pin 4, which can be found in ESP2812 pinout image to be D2.

![Image](ESP8266-NodeMCU-kit-12-E-pinout-gpio-pin.png "ESP8266 pinout")

[upy]: https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html

```
from machine import Pin
from neopixel import NeoPixel

N = 50                  # number of LED in the chain
pin = Pin(4, Pin.OUT)   # set GPIO4 to output to drive NeoPixels
np = NeoPixel(pin, N)   # create NeoPixel driver on GPIO0 for 8 pixels
np[0] = (255, 255, 255) # set the first pixel to white
np.write()              # write data to all pixels
r, g, b = np[0]         # get first pixel colour
```
After running the code you can see that the LED number 0 (i.e. the first one) is turned on white. This is because `np[0]` represents the first pixel of the variable `np` (number 0).

Actually every LED is composed of three colors that have intensity between 0 and 255 (i.e. codified by 8 bits). The line `np[0] = (255,255,255)` encodes the maximal intensity in order of (green, red, blue) colors.

## Turn on All

Now lets setup a color of the whole chain to be pink, which is encoded as `pink = (0,255,50)`. 

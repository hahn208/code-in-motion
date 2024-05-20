# Code in Motion

This project hosts a socket server on Raspberry Pi and converts text input into a dazzling display on an LED strip. The client code connects to the socket and streams the content. My goal here was to have a light show as I'm coding a project.

## Client Code `(socket_client.py)`

Code within socket_client.py will connect to the socket then stream key-strokes.

Requires pynput to capture keyboard. Specify the host device address listening for a connection (eg Raspberry Pi)

`$ python3 socket_client raspberrypi.local`

Currently using `~` as the escape character to close the socket.

## Server Code `(socket_led_server.py)`

Code within the host script receives data through the socket. The data is converted to a tuple of RGB values to display on an LED strip.

Requires the [Adafruit NeoPixel libraries](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage).

Socket will open on `0.0.0.0:10000`, which is hard-coded in the script. `sudo` required for driving pixels on a Raspberry Pi.

`$ sudo python3 socket_led_server.py`

## Haiku

`Code paints vibrant light` \
`Inspired lanterns dance and glow` \
`Motion brings new dreams`

---
import select
import socket
import time
import board
import neopixel

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('0.0.0.0', 10000)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Set socket to non-blocking mode
sock.setblocking(False)

# Lists to hold the sockets we'll be monitoring
inputs = [sock]

# Variable to hold the iteration increment
last_shift_time = time.time()

# Interval for advancing pixel sequence
shift_interval = 0.05

# Choose the pin to use on the Raspberry Pi GPIO
pixel_pin = board.D18

# Set the number of pixels. No idea why, I needed to add two.
num_pixels = 10

# If there is a white led, set the brightness [0~255]
white_level = 64

# The order of the pixel colors - RGB, GRB, RGBW, or GRBW. Some NeoPixels have red and green reversed!
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=True, pixel_order=ORDER)

# Make an inactive pixel based on the existence of a white led
inactive_pixel = (0, 0, 0) if ORDER in (neopixel.RGB, neopixel.GRB) else (0, 0, 0, 0)

# Factor the luminosity into the pixel Tuple
def set_lum(pixel, lum):
    return tuple(round(p * lum / 100) for p in pixel)

# Given a value [0~255] and luminosity, return an rgb|w Tuple
def wheel(pos, lum = 100):
    # The colours are a transition r - g - b - back to r.
    if 0 > pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)

    if ORDER in (neopixel.RGB, neopixel.GRB):
        return set_lum((r, g, b), lum)

    # RGBW | GRBW
    return set_lum((r, g, b, white_level), lum)

# Starting value for the led sequence
iter = 0
led_list = [inactive_pixel]

# Populate a List of of inactive pixels
for i in range(num_pixels - 1):
    led_list = [inactive_pixel] + led_list

print('Listening for client connection.')

while True:
    # Check if it's time to splice a color
    current_time = time.time()

    if current_time - last_shift_time >= shift_interval:
        # Shift new pixel color into the List at a lower brightness for a trailing effect.
        led_list = [tuple(p // 5 for p in led_list[0])] + led_list

        # Pop the last item off
        del led_list[-1]

        # Set colors
        for x in range(num_pixels-1):
            pixels[x] = led_list[x]

        last_shift_time = current_time

    # Wait for at least one of the sockets to be ready for processing
    readable, _, _ = select.select(inputs, [], [], 0.075)

    # Handle inputs
    for s in readable:
        if s is sock:
            # New connection
            connection, client_address = sock.accept()
            print('client connected:', client_address)
            connection.setblocking(False)
            inputs.append(connection)
        else:
            # Incoming data on an existing connection
            data = s.recv(16)
            kdata = data.decode()

            if isinstance(kdata, str):
                kchar = kdata[0]
            else:
                kchar = next(iter(kdata))

            # Shift new pixel color into array
            # Multiplying the key code by 6 (arbitrary) increases the color range relative to key pressed
            led_list = [wheel(ord(kchar) * 6 & 255)] + led_list

            # Pop the last item off
            del led_list[-1]

            if data:
                s.sendall(data)
            else:
                # No data means the client has disconnected
                print('client disconnected')
                s.close()
                inputs.remove(s)

# Clear leds
pixels.fill(inactive_pixel)

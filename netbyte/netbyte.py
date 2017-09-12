#                __  __          __
#    ____  ___  / /_/ /_  __  __/ /____
#   / __ \/ _ \/ __/ __ \/ / / / __/ _ \
#  / / / /  __/ /_/ /_/ / /_/ / /_/  __/
# /_/ /_/\___/\__/_.___/\__, /\__/\___/
#                      /____/
#                       Author: sc0tfree
#                       Twitter: @sc0tfree
#                       Email: henry@sc0tfree.com

import socket
import errno
import argparse
import sys
import time
import util.output as out
import util.text as text
from util.readasync import ReadAsync


def description():
    '''
    argparse description text
    '''
    return '''
Netbyte is a Netcat-style tool that facilitates probing proprietary TCP and UDP services.
It is lightweight, fully interactive and provides formatted output in both hexadecimal and ASCII.'''


def parse_arguments():
    '''
    Parse command line arguments

    Returns:
        argparse Namespace object
    '''
    parser = argparse.ArgumentParser(description=description(), formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('hostname', metavar='HOSTNAME', help='Host or IP to connect to')
    parser.add_argument('port', metavar='PORT', help='Connection port')
    parser.add_argument('-u', dest='udp', action="store_true", default=False, help='Use UDP instead of default TCP')

    if len(sys.argv) == 1:

        parser.print_help()

        exit(1)

    args = parser.parse_args()
    return args


def main():
    '''
    Main function: Connects to host/port and spawns ReadAsync
    '''

    args = parse_arguments()

    if args.udp:
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connection.settimeout(2)

    address = (args.hostname, int(args.port))

    try:
        connection.connect(address)

    except socket.error:
        out.print_error("Could not establish connection to " + address[0] + ":" + str(address[1]))

    # print(Fore.GREEN + Style.BRIGHT + "Connection established" + Style.RESET_ALL)

    try:
        connection.setblocking(0)
        stdin = ReadAsync(sys.stdin.readline)

        while True:
            try:
                data = connection.recv(4096)
                if not data:
                    raise socket.error
                out.print_ascii(data)
                out.print_hex(to_hex(data))
            except socket.error, e:
                if e.errno != errno.EWOULDBLOCK:
                    raise
            try:
                connection.send(stdin.dequeue())
            except Empty:
                time.sleep(0.1)

    except KeyboardInterrupt:
        connection.close()
        out.print_error("\nExiting...")
    except socket.error:
        out.print_error("Connection closed")
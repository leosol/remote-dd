import argparse
import logging
import utils
from engine import PyRemoteDDServer, PyRemoteDDClient

DEFAULT_PORT = "9191"
DEFAULT_BLOCK_SIZE = 4096*1024


def parse_args():
    parser = argparse.ArgumentParser(description="Start PyRemoteDD to Dump Physical Drives to a destination",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--debug", action="store_true", dest="debug_mode",
                        help="Run in debug mode (dump debug messages).")
    parser.add_argument("--server", action="store_true", dest="server_mode",
                        default=False, help="Server Mode. This mode is to provide raw disk data.")
    parser.add_argument("--client", action="store_true", dest="client_mode", default=False,
                        help="Client Mode. This mode is to receive raw disk data.")
    parser.add_argument("--listen", action="store_true", dest="listen",
                        help="Run in debug mode (dump debug messages).")

    parser.add_argument("-c", action="store", dest="connect_ip", required=False,
                        help="The IP address to connect to.")
    parser.add_argument("-p", action="store", dest="connect_port", required=False,
                        default=DEFAULT_PORT,
                        help="The TCP port to connect to.")
    parser.add_argument("-k", action="store", dest="password", required=False,
                        default=utils.generate_password())

    parser.add_argument("-if", action="store", dest="input_file", required=False,
                        help="The physical device or file to read data from")
    parser.add_argument("-of", action="store", dest="output_file", required=False,
                        help="The file to write data to")
    parser.add_argument("-bs", action="store", dest="block_size", required=False,
                        default=DEFAULT_BLOCK_SIZE,
                        help="Block Size")
    parser.add_argument("-skip", action="store", dest="skip_blocks", required=False,
                        default=0,
                        help="Blocks to skip from file start")
    parser.add_argument("-count", action="store", dest="count", required=False,
                        default=-1,
                        help="Number of blocks to read")

    options = parser.parse_args()
    return options


def main():
    opts = parse_args()
    server_mode = opts.server_mode
    client_mode = opts.client_mode
    listen = opts.listen
    ip = opts.connect_ip
    port = int(opts.connect_port)
    input_file = opts.input_file
    output_file = opts.output_file
    block_size = opts.block_size
    skip_blocks = opts.skip_blocks
    password = opts.password
    count = opts.count
    logging.basicConfig(level=logging.DEBUG if opts.debug_mode else logging.INFO)

    if not server_mode and not client_mode:
        print("You must set which mode to run: --server to read data from disk / --client to write received data")
        exit(-1)

    if server_mode:
        if listen:
            print(f"Server password is: {password}")
        server = PyRemoteDDServer(input_file=input_file, block_size=block_size, skip_count=skip_blocks,
                                  read_count=count, ip_address=ip,
                                  tcp_port=port, listen=listen, password=password)
        server.start()
    if client_mode:
        if listen:
            print(f"Client password is: {password}")
        client = PyRemoteDDClient(output_file=output_file, block_size=block_size, skip_count=skip_blocks,
                                  read_count=count, ip_address=ip,
                                  tcp_port=port, listen=listen, password=password)
        client.start()


if __name__ == "__main__":
    main()

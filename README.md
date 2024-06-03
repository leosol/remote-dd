# PY-REMOTE-DD
### Provide remote dd functionality over internet to remote sites

Creates a remote disk copy using python to a TCP destination protected by a password. 

*Alert*: it does not use SSL (yet)

```
usage: py-remote-dd.exe [-h] [--debug] [--server] [--client] [--listen] [-c CONNECT_IP] [-p CONNECT_PORT]
                        [-k PASSWORD] [-if INPUT_FILE] [-of OUTPUT_FILE] [-bs BLOCK_SIZE] [-skip SKIP_BLOCKS]
                        [-count COUNT]

Start PyRemoteDD to Dump Physical Drives to a destination

options:
  -h, --help         show this help message and exit
  --debug            Run in debug mode (dump debug messages).
  --server           Server Mode. This mode is to provide raw disk data.
  --client           Client Mode. This mode is to receive raw disk data.
  --listen           Run in debug mode (dump debug messages).
  -c CONNECT_IP      The IP address to connect to.
  -p CONNECT_PORT    The TCP port to connect to.
  -k PASSWORD
  -if INPUT_FILE     The physical device or file to read data from
  -of OUTPUT_FILE    The file to write data to
  -bs BLOCK_SIZE     Block Size
  -skip SKIP_BLOCKS  Blocks to skip from file start
  -count COUNT       Number of blocks to read

  # RAW disk access via SERVER MODE
  main -if \\.\PhysicalDrive7 --listen --server -k passwd123 --debug
  # RAW disk access on the client via CLIENT MODE
  py-remote-dd.exe -of I:\Temp\file.dd --client -k passwd123 -c 192.168.200.1 --debug
```

### Download EXE
[download](https://github.com/leosol/py-remote-dd/blob/main/dist/py-remote-dd.exe)


### Installation
```bash
# Clone the repository
git clone https://github.com/leosol/py-remote-dd
```

### Create EXE Yourself
```bash
cd py-remote-dd
cd src
pip install pyinstaller
pyinstaller -F main.py
```

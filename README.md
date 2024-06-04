# REMOTE-DD - efective remote RAW disk access
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

### DIRECT CONNECTION (No NAT)

- The provider of the RAW disk access will listen to connections. 
- Validate the password and provide RAW access via network.

```bash
# on server
py-remote-dd.exe --debug --server --listen -k MySecretPasswd -if \\.\PhysicalDrive0 
```

```bash
# on client
py-remote-dd.exe --debug --client -c 192.168.200.1 -k MySecretPasswd -of .\Evidence.dd
```

### REVERSE CONNECTION (With NAT)

- The provider of the RAW disk access is under NAT and can't receive connections
- It will connect to the remote client, validate password and provide RAW access.

```bash
# on server
py-remote-dd.exe --debug --server -ip 10.1.1.101 -k MySecretPasswd -if \\.\PhysicalDrive0 
```

```bash
# on client
py-remote-dd.exe --debug --client --listen -k MySecretPasswd -of .\Evidence.dd
```

### Network Errors and Retries
- If output file already exists, a seek will be performed to the size of the acquired data
- This means that on the next run, will continue from the last block just read
- To start a new RAW disk access, choose a non existing file or a zero size file

### Download EXE

Pre-built version under dist folder.

Check instructions below for building it yourself

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


# LC29H_Multi-CH_GNSS_Receiver

Implementation of a logging platform for multiple GNSS receivers.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Documentation

This multi channels GNSS receiver is based on the LC29H module from Quectel.

The output is UART connected to a 2 channel UART to Ethernet module. This one is configured to be a TCP server at IP adress 192.168.50.1xx. There are 2 TCP servers per module, on port 2000 and 2001, each connected to a Quectel LC29H.

These 4CH boards are to be connected to a network switch to be acessed all at once. The Python logger script can be executed on any computer connected to the 192.168.50.xx network, in this use-case it is executed on a Raspberry-Pi.

## User-guide

### First connect to the RPi via SSH protocol
ipaddress: 192.168.50.2
id/pw: esa/estec

### Then set the correct date (UTC)
`sudo date MMJJHHMMYYYY.ss`

example command: `sudo date 071610392024.20`

output: `Tue 16 Jul 10:39:20 CEST 2024`

### Go to the Documents/GNSS_logger directory
```
cd Documents/GNSS_logger/
```

### Create a new screen terminal (enable the script to keep running when we close the ssh session)
```
screen -S log_gnss
```

### Launch the logging process and confirm (specify the execution time using one of these commands (by default the execution time is 1min)):
```
python logger_multi_receiver_v1.8.0.py --execution_time_s 10
python logger_multi_receiver_v1.8.0.py --execution_time_min 10
python logger_multi_receiver_v1.8.0.py --execution_time_h 10
```

**Wait for all the servers to be connected then hit enter.**

The remaining time is then displayed every seconds. If for any reason the user needs to stop it, the way to do it is by hitting ctrl+c (2 times).
You can now close the terminal.

You can reconnect to the terminal by SSH and using this command:
```
screen -r log_gnss
```

### When the logging is finished you can retrieve the logging files by using SFTP protocol (FileZilla for example).
Just connect to the server using the previous logins and navigate to the `Documents/GNSS_logger` folder.
Here you will find log files in the format YYMMDD_HHMMSS_RXX where RXX is the receiver identifier.

### These log files are NMEA RTCM3 format and can be converted to RINEX using RTKCONV.

### Finally, the RPi can be powered off using the command :
ctrl+D (to close the log_gnss screen)
`sudo shutdown now`



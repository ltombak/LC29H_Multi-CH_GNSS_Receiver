import socket
import time
import threading
from datetime import datetime
import argparse

# 16 Channels Receivers

def logging(client_socket, execution_time, label):
    # Get the current time and format it
    current_time = datetime.now().strftime("%y%m%d_%H%M%S")
    # Open a binary file for logging with the timestamp and label in the filename
    log_file_name = f"{current_time}_{label}.log"

    with open(log_file_name, 'ab') as log_file:
        start_time = time.time()
        end_time = start_time + execution_time

        while time.time() < end_time:
            # Receive data from the server
            data = client_socket.recv(1024)

            if not data:
                break

            # Log the received data as bytes
            log_file.write(data)


def receive_and_log(server_address, server_port, execution_time, label, start_event):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_address, server_port))
        print(f"Connected to {server_address}:{server_port}")

        # Wait for the signal to start logging
        start_event.wait()

        # Start the logging
        logging(client_socket, execution_time, label)

    except Exception as e:
        print(f"Error connecting to {server_address}:{server_port}: {e}")

    finally:
        # Close the socket
        client_socket.close()


def print_time_left(execution_time, start_event):

    start_time = time.time()
    end_time = start_time + execution_time

    current_time = datetime.now().strftime("%y%m%d_%H%M%S")
    print(f"\nMeasurement start: {current_time}")

    while time.time() < end_time:
        # Calculate time left
        time_left = end_time - time.time()
        minutes, seconds = divmod(time_left, 60)
        # Print the time left in "xx min yy s" format
        print(f"Time left: {int(minutes)} min {int(seconds)} s")
        time.sleep(1)

    # Ensure final time left is printed as zero
    # print("Time left: 0 min 0 s")


def logger(execution_time):
    # Common server details
    servers = [
        ("192.168.50.100", 2000, "R1"),
        ("192.168.50.100", 2001, "R2"),
        ("192.168.50.101", 2000, "R3"),
        ("192.168.50.101", 2001, "R4"),
        ("192.168.50.102", 2000, "R5"),
        ("192.168.50.102", 2001, "R6"),
        ("192.168.50.103", 2000, "R7"),
        ("192.168.50.103", 2001, "R8"),
        ("192.168.50.104", 2000, "R9"),
        ("192.168.50.104", 2001, "R10"),
        ("192.168.50.105", 2000, "R11"),
        ("192.168.50.105", 2001, "R12"),
        ("192.168.50.106", 2000, "R13"),
        ("192.168.50.106", 2001, "R14")
    ]

    threads = []
    start_event = threading.Event()

    for i in range(len(servers)):
        thread = threading.Thread(target=receive_and_log,
                                  args=(servers[i][0], servers[i][1], execution_time, servers[i][2], start_event))
        threads.append(thread)

    # Start all threads
    for i in range(len(servers)):
        print(f"Starting thread[{i}]")
        threads[i].start()
        time.sleep(0.5)

    # Create the time_thread but wait to start it
    time_thread = threading.Thread(target=print_time_left, args=(execution_time, start_event))

    # Wait for the user input to start logging
    input("Press Enter to start logging...")

    # Signal all threads to start logging
    start_event.set()
    # Start the time_thread
    time_thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    time_thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-receiver logger")
    parser.add_argument("--execution_time_s", type=int, default=0, help="Execution time in seconds")
    parser.add_argument("--execution_time_min", type=int, default=10, help="Execution time in minutes")
    parser.add_argument("--execution_time_h", type=int, default=0, help="Execution time in hours")

    args = parser.parse_args()

    execution_time = args.execution_time_s + (args.execution_time_min * 60) + (args.execution_time_h * 3600)
    print(f"Execution time: {execution_time} seconds")
    logger(execution_time)

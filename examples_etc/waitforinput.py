import threading
import queue
import time
import sys


def start_trader(name):
    def print_name(name):
        print(
            f"""
            {name} is working...
            """
        )
        time.sleep(5)

    thread = threading.Thread(target=print_name, args=(name))
    thread.daemon = True
    thread.start()


def get_input():

    message = "Waiting for inputs... \n"
    channel = queue.Queue()
    response = input(message)
    channel.put(response)
    response = channel.get(False)

    if response == "exit":
        sys.exit()
    elif response == "start trader":
        name = input("Name the trader")
        start_trader(name)

    time.sleep(1)
    get_input()


if __name__ == "__main__":
    thread = threading.Thread(target=get_input, args=())
    thread.start()

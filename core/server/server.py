import sys
import argparse
import logging
import yavide_utils
from multiprocessing import Process, Queue

# TODO remove. Used only for sleep() 
import time

def client_1(server_queue):
    while True:
        server_queue.put([1, None, "[1] Hello there"])
        time.sleep(1)

def client_2(server_queue):
    while True:
        server_queue.put([2, None, "[2] Hello there"])
        time.sleep(1)

def client_3(server_queue):
    while True:
        server_queue.put([3, None, "[3] Hello there"])
        time.sleep(1)

def client_4(server_queue):
    while True:
        server_queue.put([4, None, "[4] Hello there"])
        time.sleep(1)
           
class Server():
    def __init__(self, clients):
        self.queue = Queue()
        self.clients = clients

    def run(self):
        for client in self.clients:
            process = Process(target=client, args=(self.queue,))
            process.start()

        while True:
            data = self.queue.get()
            yavide_utils.YavideUtils.send_vim_remote_command("YAVIDE1", ":echomsg '" + data[2] + "'")
            print data
        self.clients.join()

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)s] %(funcName)25s(): %(message)s'
    logging.basicConfig(filename='.yavide_indexer.log', filemode='w', format=FORMAT, level=logging.INFO)

    clients = [client_1, client_2, client_3, client_4]
    server = Server(clients)
    server.run()

if __name__ == "__main__":
    main()


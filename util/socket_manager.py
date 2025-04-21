import logging
import socket
import sys
import threading
from time import sleep

from util import boto3_manager


class socket_client:
    def __init__(self):
        self.HOST = '0.0.0.0'
        self.PORT = 3570
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def startup(self):

        try:

            self.socket.bind((self.HOST, self.PORT))

        except socket.error as message:

            print('Bind failed. Error Code : '
                  + str(message[0]) + ' Message '
                  + message[1])

        logging.info("Socket Has Been Bound, Listening on Port \'3570\'")

        self.socket.listen(9)

    def accept(self):
        connection, address = self.socket.accept()
        message = connection.recv(1024).decode()

        print(f"Connection Established With {address}, Recieved: {message}")

        return message


class socket_event_dispatch(threading.Thread):

    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

    def run(self):
        client = socket_client()
        client.startup()
        response = client.accept()

        if (response.endswith("shutdown")):
            boto3_manager.boto3_client().stop_server()

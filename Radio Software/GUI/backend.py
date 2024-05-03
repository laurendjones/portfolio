import serial.tools.list_ports
from threading import Thread
import time

from xbee import XBee
from logger import Logger

class backend:
    def __init__(self):
        self.logger = Logger()

    def setup(self, response_callback, error_callback):
        self.response_callback = response_callback

        xbee_com_port = None
        com_ports = serial.tools.list_ports.comports()
        description = "Silicon Labs CP210x"
        for com_port in com_ports:
            if not com_port.description.startswith(description):
                continue
            if not xbee_com_port == None:
                error_callback(f"Multiple ports matching description \"{description}\" found.\nTerminating program.")
                raise Exception
            xbee_com_port = com_port
        if xbee_com_port == None:
            error_callback(f"No ports matching description \"{description}\" found.\nTerminating program.")
            raise Exception

        self.xbee = XBee(xbee_com_port.device, 57600)

        t = Thread(target=self.write_data, daemon=True)
        t.start()

    def request_data(self):
        self.response_callback(self.xbee.read())

    def write_data(self):
        old_data = self.xbee.read()
        while True:
            new_data = self.xbee.read()
            if new_data != old_data:
                self.logger.write_data(new_data)
                old_data = new_data
            time.sleep(0.025)

    def set_logging(self, do_logging):
        self.logger.set_logging(do_logging)

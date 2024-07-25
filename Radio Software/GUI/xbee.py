import copy
import serial
from threading import Lock, Thread

from DataModel.XbeeData import XbeeData
from DataModel.eCVTData import eCVTData
from DataModel.ElectronsData import ElectronsData
from DataModel.IMUData import IMUData
from DataModel.IOData import IOData


class XBee:
    def __init__(self, port, baud):
        self.lock = Lock()
        self.serial = serial.Serial(port, baud)
        self.ecvt_data = eCVTData()
        self.electrons_data = ElectronsData()
        self.imu_data = IMUData()
        self.io_data = IOData()
        self.safe_data = XbeeData(self.ecvt_data, self.electrons_data, self.imu_data, self.io_data)

        t = Thread(target=self.poll_serial)
        t.daemon = True
        t.start()

    def poll_serial(self):
        start_byte = (42).to_bytes(1, "big")
        end_byte = (59).to_bytes(1, "big")

        while True:
            for i in range(4):
                success = True
                if self.serial.read(1) != start_byte:
                    success = False
                    break
            if not success:
                continue

            ecvt_read = self.serial.read(self.ecvt_data.size)
            electrons_read = self.serial.read(self.electrons_data.size)
            imu_read = self.serial.read(self.imu_data.size)
            io_read = self.serial.read(3)

            for i in range(4):
                success = True
                if self.serial.read(1) != end_byte:
                    success = False
                    break
            if not success:
                continue

            self.ecvt_data.update(ecvt_read)
            self.electrons_data.update(electrons_read)
            self.imu_data.update(imu_read)
            self.io_data.update(io_read)

            copy_ecvt_data = copy.deepcopy(self.ecvt_data)
            copy_electrons_data = copy.deepcopy(self.electrons_data)
            copy_imu_data = copy.deepcopy(self.imu_data)
            copy_io_data = copy.deepcopy(self.io_data)

            with self.lock:
                self.safe_data = XbeeData(copy_ecvt_data, copy_electrons_data, copy_imu_data, copy_io_data)

    def read(self):
        with self.lock:
            return self.safe_data

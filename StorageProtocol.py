import storage
import supervisor

class StorageProtocol:
    def __init__(self):
        usb_mode = supervisor.runtime.usb_connected
        self.write_active = not usb_mode
        storage.remount("/", usb_mode)


    def write(self, fileName, data, writeMethod = "w"):
        if not self.write_active: return

        with open(fileName, writeMethod) as file:
            file.write(data)
            file.close()


    def read(self, fileName):
        data = []
        with open(fileName, "r") as file:
            data = file.readlines()
            file.close()

        return data

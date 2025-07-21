import storage
import supervisor

class StorageProtocol:
    def __init__(self):
        if supervisor.runtime.usb_connected:
            self.write_active = False
            
        else:
            # if we aren't connected via USB
            # CircuitPython can write to the drive
            storage.remount("/", False)
            self.write_active = True

    
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

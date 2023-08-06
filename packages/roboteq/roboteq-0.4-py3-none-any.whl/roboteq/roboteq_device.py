import serial


class RoboteqDevice:
    """Initializes A Roboteq device object
    
    """
    def __init__(self) -> None:
        """Initializes A Roboteq device object
        
        """
        self.is_roboteq_connected = False
        self.port = ""
        self.baudrate = 115_200
        self.ser = None

    def connect(self, port: str, baudrate: int = 115_200) -> bool:
        """Attempts to make a serial connection to the roboteq controller
        
        """
        self.port = port
        self.baudrate = baudrate
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
            )
            # reset the connection if need be
            if self.ser.isOpen():
                self.ser.close()
            self.ser.open()
            self.is_roboteq_connected = True

        except:
            print("ROBOTEQ ERROR: Unable to connect to roboteq motor controller")
            print("Please turn on the roboteq power.")
            self.is_roboteq_connected = False

        return self.is_roboteq_connected

    def set_config(
        self, config_item: str, channel: int = None, value: int = None
    ) -> None:
        self.send_command(f"{config_item} {channel} {value}")

    def get_value(
        self, config_item: str, channel: int = None, value: int = None
    ) -> None:
        self.getdata()
        self.send_command(f"{config_item} {channel} {value}")
        result = self.getdata()
        return result

    def getdata(self):
        info = ""
        while self.ser.inWaiting() > 0:
            info += str(self.ser.read())

        return info

    def command_motor(
        self, command_item: str, channel: [str, int] = None, value: [str, int] = None
    ) -> None:
        """Sends a command to a specific motor channel
        
        """
        self.send_command(f"{command_item} {channel} {value}")

    def send_command(self, command: str) -> None:
        if command[-1] != "\r":
            command += "\r"
            self.ser.write(command.encode())

"""
Library to control the motor through the arduino.
"""
import serial

class Arduino():
    """
    Class to connect Arduino

    Attributes:
        conn (serial.Serial): serial connection

    Methods:
        send_command(pin_number, digital_value)
        read_command()
        close()
    """
    
    def __init__(self, serial_port='/dev/ttyACM0', baud_rate=9600, read_timeout=5):
        """
        Constructor

        Args:
            serial_port (str): serial port
            baud_rate (int): baud rate
            read_timeout (int): read timeout

        Returns:
            None
        """
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout # Timeout for readline()
        print 'Connection initialized'
    
    def send_command(self, pin_number, digital_value, buzzer=False, forward=False, turn=""):
        """
        Writes the digital_value on pin_number
        Internally sends b'WS{pin_number}:{digital_value}' over the serial
        connection 

        Args:
            pin_number (int): pin number
            digital_value (int): digital value
            buzzer (bool): if True, buzzer is activated
        
        Returns:
            None
        """
        if buzzer:
            command = "Wb{}:{}".format(str(pin_number),str(digital_value)).encode()
        else:
            if forward:
                command = "WF{}:{}".format(str(pin_number),str(digital_value)).encode()
            else:
                if turn == "Left":
                    command = "WL{}:{}".format(str(pin_number),str(digital_value)).encode()
                elif turn == "Right":
                    command = "WR{}:{}".format(str(pin_number),str(digital_value)).encode()
        self.conn.write(command)

    def read_command(self):
        """
        Reads the serial connection
        Internally reads b'R{pin_number}:{digital_value}' over the serial
        connection 

        Args:
            None
        
        Returns:
            pin_number (int): pin number
            digital_value (int): digital value
        """
        command = self.conn.readline()
        command = command.decode()
        command = command.split(' ')
        pin_number = int(command[1])
        digital_value = int(command[2])
        return pin_number, digital_value

    def close(self):
        """
        Closes the serial connection
        """
        self.conn.close()
        print 'Connection closed'
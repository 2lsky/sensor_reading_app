import serial
class port_connection():
    def __init__(self,port,baudrate,stopbits,parity,bytesize):
        self.port = port
        self.baudrate = baudrate
        self.stopbits = eval('serial.' + stopbits)
        self.parity = eval('serial.' + parity)
        self.bytesize = eval('serial.' + bytesize)
        self.flag_of_error = False
        try:
            self.serial_port = serial.Serial(port=self.port, baudrate=self.baudrate, parity=self.parity,stopbits=self.stopbits, bytesize=self.bytesize)
        except:
            self.flag_of_error = True
    def write_to_port(self,write_command):
        try:
            self.serial_port.write(write_command)
            self.flag_of_error = False
        except:
            self.flag_of_error = True
    def read_from_port(self,pattern_for_reading):
        try:
            self.flag_of_error = False
            return pattern_for_reading(self.serial_port.read_all())
        except:
            self.flag_of_error = True
    def close_port(self):
        if self.flag_of_error is False:
            self.serial_port.close()
        else:
            pass
    def reset(self):
        if self.flag_of_error is False:
            self.serial_port.reset_output_buffer()
        else:
            pass
class Mitutoyo_connection_throw_MUX(port_connection):
    def __init__(self,port,baudrate,stopbits,parity,bytesize):
        super().__init__(port,baudrate,stopbits,parity,bytesize)
#class HART_connection(port_connection):
    #def __init__(self,port,baudrate,stopbits,parity,bytesize,type_of_write_command):
        #if type_of_write_command == 0:
            #write_command = bytes.fromhex('')
            #pattern_for_reading
        #elif type_of_write_command == 1:
            #write_command = bytes.fromhex('FFFFFFFFFFFFFFFFFFFF02')
            #pattern_for_reading =
        #super().__init__(port,baudrate,stopbits,parity,bytesize,write_command,pattern_for_reading)






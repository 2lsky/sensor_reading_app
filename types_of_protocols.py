from connector_module import Mitutoyo_connection_throw_MUX
from types_of_output_values import Mitutoyo_MUX_normal_output_value
import time
def Mitutoyo_throw_MUX_signal(port,time_step):
    connection = Mitutoyo_connection_throw_MUX(port,19200,'STOPBITS_ONE','PARITY_NONE','EIGHTBITS')
    connection.reset()
    time.sleep(time_step)
    connection.write_to_port(write_command =f'A\r'.encode(encoding='utf-8'))
    time.sleep(0.2)
    values = connection.read_from_port(pattern_for_reading=Mitutoyo_MUX_normal_output_value)
    connection.close_port()
    return values if values is not None else {}





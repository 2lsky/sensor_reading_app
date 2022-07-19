import threading
from types_of_protocols import Mitutoyo_throw_MUX_signal
from serial.tools import list_ports
import serial
import pandas as pd
import tkinter as tk
from tkinter import ttk,messagebox
import os
import numpy as np
from time import gmtime, strftime
ports = ['COM1','COM2','COM3','COM4']
numbers_of_values = [1,1,1,1]
number_of_values=dict(list(zip(range(len(numbers_of_values)),numbers_of_values)))
states_of_measurements=dict(list(zip(range(len(ports)),[False]*len(ports))))
#check_button_states=dict(list(zip(range(len(ports)),[0]*len(ports))))


class App(tk.Tk):

    def __init__(self,ports):
        super().__init__()
        self.title('Settings')
        if len(ports)!=0:
            self.geometry(f'{500+200*max(number_of_values.values())}x'+f'{150+150*len(ports)}')
        else:
            messagebox.showwarning('Error', 'Out of connection')
        self.options = {'padx': 10, 'pady': 10}
        self.values_for_ports = {}
        self.chosen_ports = {}
        self.chosen_number_of_values = {}
        self.frames = {}
        self.start_buttons = {}
        self.stop_buttons = {}
        self.check_buttons = {}
        self.threads = {}
        self.output_data = {}
        self.output_dataframe = pd.DataFrame()
        ####
        for i in range(len(ports)):
            sensor_frame = tk.Frame(self)
            self.frames[i] = sensor_frame
            frame_for_com_ports = tk.Frame(sensor_frame)
            port_label = tk.Label(frame_for_com_ports, text='COM-port')
            port_label.pack(side='left')
            names_of_port = ttk.Combobox(frame_for_com_ports, values=ports, height=1, width=6)
            names_of_port.pack(side='left', **self.options)
            names_of_port.set(ports[i])
            self.chosen_ports[i] = names_of_port
            self.start_buttons[i] = tk.Button(frame_for_com_ports, height=1, width=6, text='Start!')
            self.start_buttons[i].pack(side='left',**self.options)
            self.stop_buttons[i] = tk.Button(frame_for_com_ports, height=1, width=6, text='Stop!')
            self.stop_buttons[i].pack(side='left', **self.options)
            self.check_buttons[i] = ttk.Checkbutton(frame_for_com_ports,takefocus=False)
            self.check_buttons[i].pack(side='left',**self.options)
            frame_for_com_ports.pack(side='top', **self.options)
            ####
            frame_for_changer_of_number_of_values = tk.Frame(sensor_frame)
            label_for_changer_of_number_of_values = tk.Label(frame_for_changer_of_number_of_values, text='Number of values',height=1, width=20)
            label_for_changer_of_number_of_values.pack(side='left')
            self.chosen_number_of_values[i] = ttk.Combobox(frame_for_changer_of_number_of_values, height=1, width=10,values=list(range(1, 9)))
            self.chosen_number_of_values[i].set(number_of_values[i])
            self.chosen_number_of_values[i].pack(side='left')
            frame_for_changer_of_number_of_values.pack(side='top', **self.options)
            ####
            frame_for_values = tk.Frame(sensor_frame)
            values_for_certain_port = []
            self.values_for_ports[i] = values_for_certain_port
            frame_for_values.pack(side='top', **self.options)
            for i in range(number_of_values[i]):
                value_label = tk.Label(frame_for_values, text=f'Value {i+1}', height=1, width=10)
                value_label.pack(side='left')
                value = tk.Label(frame_for_values, height=1, width=10, relief='groove')
                value.pack(side='left')
                values_for_certain_port.append(value)
            sensor_frame.pack(**self.options)
        ####
        for j in range(len(ports)):
            self.start_buttons[j].config(command=lambda x=j:self.start_measurement(x))
            self.stop_buttons[j].config(command=lambda x=j:self.stop_measurement(x))
        #####
        frame_for_buttons = tk.Frame(self)
        self.button_for_update_ports = tk.Button(frame_for_buttons, command=self.update_number_of_ports, height=1,width=20, text='Update COM-ports')
        self.button_for_update_ports.pack(side='left', expand=1, padx=10, pady=5)
        self.button_for_update_number_of_values = tk.Button(frame_for_buttons,command=self.update_number_of_values, height=1,width=20, text='Update number of values')
        self.button_for_update_number_of_values.pack(side='left')
        self.button_for_start_for_chosen_ports = tk.Button(frame_for_buttons, command=self.start_measurement_for_chosen_ports, height=1,width=20, text='Start for choosen ports')
        self.button_for_start_for_chosen_ports.pack(side='left', expand=1, padx=10, pady=5)
        self.button_for_stop_for_chosen_ports = tk.Button(frame_for_buttons, command=self.stop_measurement_for_chosen_ports, height=1,width=20, text='Stop for choosen ports')
        self.button_for_stop_for_chosen_ports.pack(side='left', expand=1, padx=10, pady=5)
        frame_for_buttons.pack(side='top', expand=1)
        #####

    def update_number_of_ports(self):
        new_ports = []
        global ports,states_of_measurements
        for port in serial.tools.list_ports.comports():
            new_ports.append(port.name)
        if ports != new_ports:
            ports = new_ports
            states_of_measurements = dict(list(zip(range(len(ports)),[False]*len(ports))))
            self.quit_window()
            interface()

    def update_number_of_values(self):
        new_numbers_of_values = []
        global numbers_of_values, number_of_values, ports
        for i in range(len(ports)):
            new_numbers_of_values.append(self.chosen_number_of_values[i].get())
        for j in range(len(new_numbers_of_values)):
            if int(new_numbers_of_values[j]) != numbers_of_values[j]:
                numbers_of_values = [int(x) for x in new_numbers_of_values]
                number_of_values = dict(list(zip(range(len(ports)), numbers_of_values)))
                self.quit_window()
                interface()

    def start_measurement(self,number_of_frame):
        data_for_certain_port = []
        global states_of_measurements
        states_of_measurements[number_of_frame] = True
        for value in self.values_for_ports[number_of_frame]:
            value.config(background='lightgreen')
        self.chosen_ports[number_of_frame].config(state='disabled')
        self.check_buttons[number_of_frame].config(state='disabled')
        self.start_buttons[number_of_frame].config(state='disabled')
        self.chosen_number_of_values[number_of_frame].config(state='disabled')
        self.button_for_update_ports.config(state='disabled')
        self.button_for_update_number_of_values.config(state='disabled')
        self.threads[number_of_frame] = threading.Thread(target=self.measure,args=(number_of_frame,data_for_certain_port))
        self.threads[number_of_frame].start()

    def stop_measurement(self,number_of_frame):
        global states_of_measurements
        for value in self.values_for_ports[number_of_frame]:
            value.config(background='white')
        self.check_buttons[number_of_frame].config(state='active')
        self.start_buttons[number_of_frame].config(state='active')
        self.chosen_ports[number_of_frame].config(state='active')
        self.chosen_number_of_values[number_of_frame].config(state='active')
        states_of_measurements[number_of_frame] = False

    def measure(self,number_of_frame,data):
        if states_of_measurements[number_of_frame]:
            current_values = Mitutoyo_throw_MUX_signal(self.chosen_ports[number_of_frame].get(), 2)
            data.append(current_values)
            if current_values is not None:
                for j in range(len(self.values_for_ports[number_of_frame])):
                    if str(j + 1) in current_values.keys():
                        self.values_for_ports[number_of_frame][j].config(text=f'{current_values[str(j + 1)]}')
                    else:
                        self.values_for_ports[number_of_frame][j].config(text='None')
            self.frames[number_of_frame].update()
            if self.stop_buttons[number_of_frame]['state'] == 'disabled':
                self.output_data[self.chosen_ports[number_of_frame].get()] = data
            self.frames[number_of_frame].after(500, self.measure(number_of_frame,data))
        else:
            self.start_buttons[number_of_frame].config(state='active')
            self.check_buttons[number_of_frame].config(state='active')
            if list(states_of_measurements.values()) == [False]*len(list(states_of_measurements.values())):
                self.button_for_update_number_of_values.config(state='active')
                self.button_for_update_ports.config(state='active')
            if self.stop_buttons[number_of_frame]['state'] != 'disabled':
                self.window_for_save(self.chosen_ports[number_of_frame].get(),data)
            else:
                columns_for_dataframe=[]
                for i in range(0,number_of_values[number_of_frame]):
                    columns_for_dataframe.append(f'{self.chosen_ports[number_of_frame].get()} Value {i+1}')
                data_for_certain_port=pd.DataFrame(columns=columns_for_dataframe)
                for values in self.output_data[self.chosen_ports[number_of_frame].get()]:
                    data_for_certain_port.loc[len(data_for_certain_port)] = dict(list(zip([f'{self.chosen_ports[number_of_frame].get()} Value '+key for key in values.keys()],values.values())))
                for column in data_for_certain_port.columns:
                    self.output_dataframe[column] = data_for_certain_port[column]
                self.button_for_start_for_chosen_ports.config(state='active')
                self.stop_buttons[number_of_frame].config(state='active')
    def window_for_save(self,port,data_for_save):
        save_window = tk.Tk()
        label_question = tk.Label(save_window, text=f'Save data for {port}?',height=1, width=10*len(self.output_data.keys()))
        label_question.pack()
        save_button_yes = tk.Button(save_window, height=1, width=6, text='Yes',command=lambda data=data_for_save, port=port,window=save_window: self.save(data_for_save, port, window))
        save_button_yes.pack(side='top', **self.options)
        save_button_no = tk.Button(save_window, height=1, width=6, text='No',command=lambda data=data_for_save, window=save_window: self.dontsave(window))
        save_button_no.pack(side='top', **self.options)
        save_window.mainloop()

    def save(self,data,port,window):
        pd.DataFrame(data).to_csv('C:\\Users\\{}\\Desktop\\{} data {} .csv'.format(os.environ.get("USERNAME"),port,strftime("%Y_%m_%d_%H_%M_%S", gmtime())), sep=';', decimal=',')
        window.quit()

    def dontsave(self,window):
        window.quit()

    def start_measurement_for_chosen_ports(self):
        param = False
        self.button_for_start_for_chosen_ports.config(state='disabled')
        for i in range(len(self.check_buttons)):
            if len(self.check_buttons[i].state()) > 0 and (self.check_buttons[i].state()[0] != 'disabled' and self.check_buttons[i].state()[0] != 'alternate'):
                self.start_buttons[i].invoke()
                self.stop_buttons[i].config(state='disabled')
                param = True
        if not param:
            messagebox.showwarning('Error', 'Nothing to choose')
            self.button_for_start_for_chosen_ports.config(state='active')

    def stop_measurement_for_chosen_ports(self):
        for i in range(len(self.check_buttons.values())):
            if self.stop_buttons[i]['state'] == 'disabled':
                self.stop_buttons[i].config(state='active')
                self.stop_buttons[i].invoke()
                self.stop_buttons[i].config(state='disabled')
        list_of_ports = ','.join(self.output_data.keys())
        self.window_for_save(list_of_ports,self.output_dataframe)
    def quit_window(self):
        self.destroy()


def interface():
    app = App(ports)
    app.mainloop()


if __name__ == '__main__':
    interface()
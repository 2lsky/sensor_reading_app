import pandas as pd
###for transfer_in_different_encodings
encoding_dict = dict(zip(range(10, 16), list('ABCDEF')))
###types of sensors and its protocols
table_of_sensor_information = pd.read_csv('C:\\Users\\DTulskiy\\Desktop\\Sensor_information.csv',sep=';')
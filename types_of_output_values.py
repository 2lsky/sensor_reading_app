import re

import pandas as pd
def Mitutoyo_MUX_normal_output_value(raw_value):
   dict_of_values = {}
   for value in pd.Series(str(raw_value)[2:-1].split('\\r')).drop_duplicates().values:
      if len(value)!=0:
         if len(value)==3:
            dict_of_values[value[1]]=None
         else:
            sign = re.findall(r'[+-]',value)[0]
            dict_of_values[value.split(sign)[0][1]]=int(sign+'1')*float(value.split(sign)[1])
   return dict_of_values

#def HART_normal_output_value(raw_code):
    #output=[]
    #if len(raw_code)>0:
        #for char in raw_code:
            #output.append(binary_value(char))
        #binary_code=''.join(output)
        #extent=binary_code[1:9]
        #mantiss=binary_code[9:]
        #result=0
        #shift=int(decimal_value(extent))-127
        #for str in '1'+mantiss:
            #result+=int(str)*2**(shift)
            #shift-=1
        #return (-1)**(int(binary_code[0]))*result
    #else:
        #return 0
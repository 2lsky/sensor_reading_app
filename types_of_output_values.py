def Mitutoyo_MUX_output_value(raw_value):
    if len(raw_value[6:14])>2:
        sign = raw_value[5]
        value=float(raw_value[6:14])
    else:
        return None
    return (-1)*value if sign=='-' else value
def HART_output_value(raw_code):
    output=[]
    if len(raw_code)>0:
        for char in raw_code:
            output.append(binary_value(char))
        binary_code=''.join(output)
        extent=binary_code[1:9]
        mantiss=binary_code[9:]
        result=0
        shift=int(decimal_value(extent))-127
        for str in '1'+mantiss:
            result+=int(str)*2**(shift)
            shift-=1
        return (-1)**(int(binary_code[0]))*result
    else:
        return 0
from config import encoding_dict
class encodings():
    def __init__(self,value):
        self.value = value
        self.dict=encoding_dict
    def from_decimal_to_some_encoding(self, extent):
        end_values = []
        def right_value_for_encoding(something):
            return str(something) if something < 10 else self.dict[something]
        x=int(self.value)
        if x // extent < extent:
            end_values.append(right_value_for_encoding(x % extent))
            end_values.append(right_value_for_encoding(x // extent))
        else:
            while x // extent >= extent:
                end_values.append(right_value_for_encoding(x % extent))
                x = x // extent
                if x // extent < extent:
                    end_values.append(right_value_for_encoding(x % extent))
                    end_values.append(right_value_for_encoding(x // extent))
                    break
        return ''.join(end_values[::-1]) if end_values[-1]!='0' else ''.join(end_values[::-1])[1:]
    def from_some_encoding_to_decimal(self, extent):
        sum = 0
        j = 0
        def search_key_in_dict(something):
            flag = 0
            for key in list(self.dict.keys()):
                if something==self.dict[key]:
                    necessary_key=key
                    flag = 1
            return necessary_key if flag == 1 else int(something)
        for char in self.value[::-1]:
            sum += search_key_in_dict(char) * extent ** (j)
            j += 1
        return str(sum)

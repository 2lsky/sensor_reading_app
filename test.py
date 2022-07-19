import multiprocessing
from types_of_protocols import Mitutoyo_throw_MUX_signal
def func(port):
    print(port)
    #while 1:
        #print(Mitutoyo_throw_MUX_signal(port=port,time_step=2))
p1=multiprocessing.Process(target=func('COM4'))
p1.run()
p2=multiprocessing.Process(target=func('COM3'))
p2.run()
#ports = ['1','2','3']
#chanels = dict(list(zip(ports,[1,1,1])))
#print(chanels.keys())
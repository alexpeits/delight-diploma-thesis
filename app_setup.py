from lights import *


def test(light, sensor):
    cur_reads = []
    for i in xrange(0, 110, 10):
        light.dim_to_val(i)
        sensor.get_reading()
        cur_reads.append(sensor.current_read)
    return cur_reads


light_1 = Light('06')
light_2 = Light('07')
ldr_1 = LightSensor('03')
ldr_2 = LightSensor('04')
#sct_2 = DissipationSensor(addr='09', max_power=40)
#sct_1 = DissipationSensor('08',
#    [6, 18.21, 22.53, 25.65, 27.31, 28.68, 30.47, 31.75, 32.92, 35.85, 40.71],
#    40)
#sct_2 = DissipationSensor('09',
#    [6, 20.11, 22.77, 27.34, 28.94, 31.93, 34.56, 36.69, 38.65, 42.42, 48.10],
#    40)

#def foo():
#    ldr_1.get_reading()
#    ldr_2.get_reading()

setup()

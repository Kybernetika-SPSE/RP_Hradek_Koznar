from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
addr = 0x48

#  kalibrace
gain = 1.00
offset = 0.08

#  korekce nad 6V
korekce = 0.98


def read_adc_A0():
    config = bytearray(2)
    config[0] = 0xC2
    config[1] = 0x83

    i2c.writeto_mem(addr, 0x01, config)
    time.sleep(0.1)

    data = i2c.readfrom_mem(addr, 0x00, 2)

    raw = (data[0] << 8) | data[1]

    if raw > 0x7FFF:
        raw -= 0x10000

    return raw


while True:
    raw = read_adc_A0()

    # napětí na vstupu ADS1115
    v_adc = raw * 0.000125

    # základní kalibrace
    v_in = (v_adc * 4) * gain - offset

    #  rozdělení rozsahu
    if v_in > 6:
        v_in = v_in * korekce

    # ochrana
    if v_in < 0:
        v_in = 0

    print(round(v_in, 2))

    time.sleep(0.5)
    
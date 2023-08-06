from struct import pack
import time
from .recordgeneration import create_record_struct


def gen_test_data():
    test_data = bytearray(512)

    #

    # print(len(raw_data))

    # unixtime = unpack('d', unixtime)[0]
    # dataRate = unpack('h', dataRate)[0]
    dataRate = 833

    test_data[4:6] = pack('h', dataRate)
    test_data[22:30] = pack('d', time.time())

    for i, idx in enumerate(range(30, 510, 12)):
        ga = [(i * 100 + b) for b in range(6)]
        print(ga)
        test_data[idx:idx + 12] = pack('eeeeee', *ga)

    return test_data


data = gen_test_data()
for r in create_record_struct(data):
    print(r)

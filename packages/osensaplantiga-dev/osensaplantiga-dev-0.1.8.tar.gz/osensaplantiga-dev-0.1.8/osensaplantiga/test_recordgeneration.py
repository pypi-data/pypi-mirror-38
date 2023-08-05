from .recordgeneration import create_record_struct


def test_record_generation():

    with open("osensaplantiga/test_data/record.bin", "rb") as f:
        record_bytes = f.read()
    record_struct = create_record_struct(record_bytes)
    record_1 = record_struct[0]
    assert record_1['ax'] == 1.2392578125
    assert record_1['ay'] == -0.366455078125
    assert record_1['az'] == 0.54150390625
    assert record_1['gx'] == -98.4375
    assert record_1['gy'] == -252.875
    assert record_1['gz'] == -47.375
    assert record_1['time'] == 1541183746284365
    record_2 = record_struct[1]
    assert record_2['ax'] == 1.1943359375
    assert record_2['ay'] == -0.308349609375
    assert record_2['az'] == 0.6708984375
    assert record_2['gx'] == -99.9375
    assert record_2['gy'] == -240.5
    assert record_2['gz'] == -40.25
    assert record_2['time'] == 1541183746298771

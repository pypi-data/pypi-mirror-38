from struct import unpack
from .crc import calculate_crc
import logging

logger = logging.getLogger(__name__)


def create_record_struct(raw_bytes):
    "Takes a pod's 512 bytes and parses returns it parsed into anonymous record struct"
    raw_data = raw_bytes[30:-2]

    dataRate = raw_bytes[4:6]
    unixtime = raw_bytes[22:30]
    # Check if CRC is valid
    _crccheck = 0xFFFF
    for b in raw_data:
        _crccheck = calculate_crc(_crccheck, b)
    isvalid = (_crccheck == 0)
    if (isvalid is False):
        logger.info('Invalid data found!')
    data = []
    i = 0

    unixtime = unpack('d', unixtime)[0]
    dataRate = unpack('h', dataRate)[0]
    while i < len(raw_data):
        gx, gy, gz, ax, ay, az = unpack('eeeeee', raw_data[i: i + 12])
        time = int((unixtime + i / dataRate) * 1e6)
        data.append({"ax": ax, "ay": ay, "az": az, "gx": gx, "gy": gy, "gz": gz, 'time': time})
        i = i + 12
    return data


def create_structs_from_pod_data(pod, page_start, npages):
    "Reads npages number of pages, returns list of anonymous record objects with size npages"
    if npages < 1:
        raise AttributeError('Number of pages cannot be less than 0')
    if npages > 15:
        raise AttributeError('Number of pages cannot exceed 16 (8192 bytes)')
    page_size = 512
    adr = page_start * page_size
    nbytes = npages * page_size
    response = pod.read_flash(adr, nbytes)
    response = response[4:-2]
    # Convert to byte array
    datab = response.encode()
    # Split response into pages
    result = []
    for i in range(npages):
        start = i * page_size
        end = start + page_size
        result = result + create_record_struct(datab[start:end])
    return result


def create_structs_from_bytes(raw_bytes):
    "Reads bytes, creates anonymous record objects with size npages"
    page_size = 512
    i = 0
    # Split response into pages
    result = []
    while (i * page_size < len(raw_bytes)):
        start = i * page_size
        end = start + page_size
        result = result + create_record_struct(raw_bytes[start:end])
        i = i + 1
    return result


def read_pod_raw(pod, page_start, npages, raw_bytes):
    "Reads npages number of pages from pod, returns initial raw bytes combined with bytes read"
    if npages < 1:
        raise AttributeError('Number of pages cannot be less than 0')
    if npages > 15:
        raise AttributeError('Number of pages cannot exceed 16 (8192 bytes)')
    page_size = 512
    adr = page_start * page_size
    nbytes = npages * page_size
    response = pod.read_flash(adr, nbytes)
    response = response[4:-2]
    # Convert to byte array
    datab = response.encode()
    # Split response into pages
    for i in range(npages):
        start = i * page_size
        end = start + page_size
        raw_bytes = raw_bytes + datab[start:end]
    return raw_bytes


def read_flash_structs(pod, page_start, npages, pages_per_read=15):
    "Reads npages number of pages from pod, returns list of anonymous record objects with size npages"
    count = 0
    while count < npages:
        read_pages = pages_per_read if (npages - count) > pages_per_read else (npages - count)
        logger.info('\t\t...reading pages {}-{}'.format(page_start + count, page_start + count + read_pages - 1))
        yield from create_structs_from_pod_data(pod, page_start + count, read_pages)
        count += read_pages


def read_flash_raw(pod, page_start, npages, pages_per_read=15):
    "Reads npages number of pages from pod, returns pages as raw bytes"
    raw_bytes = b''
    count = 0
    while count < npages:
        read_pages = pages_per_read if (npages - count) > pages_per_read else (npages - count)
        logger.info('\t\t...reading pages {}-{}'.format(page_start + count, page_start + count + read_pages - 1))
        raw_bytes = read_pod_raw(pod, page_start + count, read_pages, raw_bytes)
        count += read_pages
    return raw_bytes

from typing import Tuple
from io import BytesIO

from crypto import decrypt_local
from tdf import RawTdfFile, parse_raw_tdf
from qt import read_qt_byte_array

def read_tdf_file(filepath: str) -> RawTdfFile:
    candidates = [filepath + 's', filepath]

    for candidate in candidates:
        try:
            with open(candidate, 'rb') as f:
                return parse_raw_tdf(f.read())
        except FileNotFoundError:
            pass

    raise FileNotFoundError()

def read_tdf_file1(filepath: str) -> RawTdfFile:
    candidates = [filepath + 's', filepath]

    for candidate in candidates:
        try:
            with open(candidate, 'rb') as f:
                return parse_raw_tdf(f.read())
        except FileNotFoundError:
            pass

    raise FileNotFoundError()
def read_encrypted_file(filepath: str, local_key: bytes) -> Tuple[int, bytes]:
    tdf_file = read_tdf_file(filepath)
    encrpyted_data = read_qt_byte_array(BytesIO(tdf_file.encrypted_data))
    return tdf_file.version, decrypt_local(encrpyted_data, local_key)

def read_encrypted_file1(filepath: str, local_key: bytes) -> Tuple[int, bytes]:
    tdf_file = read_tdf_file1(filepath)
    encrpyted_data = BytesIO(tdf_file.encrypted_data)
    return tdf_file.version, decrypt_local(encrpyted_data, local_key)
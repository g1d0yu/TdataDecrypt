import io
import os
import hashlib

from typing import Tuple, List, Dict, Union

from io import BytesIO

from qt import read_qt_int32, read_qt_uint64, read_qt_uint32, read_qt_byte_array, read_qt_utf8
from file_io import read_tdf_file, read_encrypted_file, read_encrypted_file1
from settings import SettingsBlocks, read_settings_blocks, proxy_proxyType, proxy_setting
from storage import decrypt_key_data_tdf, read_key_data_accounts, decrypt_settings_tdf, decrypt_maps_tdf


def file_to_to_str(filekey: bytes):
    return ''.join(f'{b:X}'[::-1] for b in filekey)


def compute_data_name_key(dataname: str):
    filekey = hashlib.md5(dataname.encode('utf8')).digest()[:8]
    return file_to_to_str(filekey)

def get_value(data:bytes):
    even_index_data = bytearray()  # 使用 bytearray 以便高效追加
    with io.BytesIO() as stream:
        stream.write(data)
        stream.seek(0)
        for i in range(1, stream.getbuffer().nbytes, 2):
            stream.seek(i)
            even_index_data.append(stream.read(1)[0])  # 读取一个字节并追加
    return even_index_data.decode('utf-8')

def get_proxy(data:bytes):
    ProxyItemDictType = Dict[str, Union[int, str, bytes, proxy_proxyType ]]
    proxy_item: ProxyItemDictType = {}
    with io.BytesIO() as stream:
        stream.write(data)
        stream.seek(0)
        proxy_item['proxy_protocol'] = proxy_proxyType(read_qt_int32(stream)).name
        proxy_item['proxy_host'] = get_value(read_qt_byte_array(stream))
        proxy_item['proxy_port'] = read_qt_int32(stream)
        proxy_item['proxy_user'] = get_value(read_qt_byte_array(stream))
        proxy_item['proxy_password'] = get_value(read_qt_byte_array(stream))
    return proxy_item

def compose_account_name(dataname: str, index: int):
    if index > 0:
        return f'{dataname}#{index+1}'
    else:
        return dataname

class ParsedAccount:
    def __init__(self):
        self.index: int = None
        self.info_data: InfoData = None

    def get_info(self):
        userDictType = Dict[str, Union[int, str, bytes, dict, list]]
        user_info: userDictType = {}
        user_info['userid'] = self.info_data.user_id
        user_info['username'] = self.info_data.username
        user_info['name'] = self.info_data.name
        user_info['phone'] = self.info_data.phone
        return user_info

class InfoData:
    def __init__(self):
        self.user_id: int = None
        self.name: str = None
        self.phone: str = None
        self.username: str = None

def read_setting_authorization(data: bytes) -> Dict:
    ProxyDictType = Dict[str, Union[int, str, bytes, dict, list, proxy_setting]]
    proxy_info: ProxyDictType = {}
    try:
        with io.BytesIO() as stream:
            proxy_list = []
            stream.write(data)
            stream.seek(0)
            size = int.from_bytes(stream.read(4), 'big', signed=True)
            stream.read(size + 20) if size > 0 else stream.read(20)
            read_qt_utf8(stream)
            read_qt_byte_array(stream)
            stream.read(36)
            read_qt_utf8(stream)
            read_qt_utf8(stream)
            stream.read(72)
            read_qt_byte_array(stream)
            stream.read(52)
            read_qt_byte_array(stream)
            stream.read(8)
            read_qt_byte_array(stream)
            stream.read(16)
            read_qt_byte_array(stream)
            size = int.from_bytes(stream.read(4), 'big', signed=True)
            if (size > 0) and (size < 10000):
                for i in range(size):
                    read_qt_byte_array(stream)
                    stream.read(2)
            count = int.from_bytes(stream.read(4), 'big', signed=True)
            if (count > 0) and (count < 10000):
                for i in range(count):
                    read_qt_byte_array(stream)
                    stream.read(1)
            stream.read(12)
            proxy = read_qt_byte_array(stream)
            p_s = BytesIO(proxy)
            proxy_info['proxyuseipv6'] = read_qt_int32(p_s)
            proxy_info['proxyuseforcall'] = read_qt_int32(p_s)
            proxy_info['proxytype'] = proxy_setting(read_qt_int32(p_s)).name
            proxy_info['proxyselected'] = get_proxy(read_qt_byte_array(p_s))
            for i in range(read_qt_int32(p_s)):
                proxy_list.append(get_proxy(read_qt_byte_array(p_s)))
            proxy_info['proxylist'] = proxy_list
            p_s.close()
    except:
        pass
    return proxy_info

class AccountReader:
    def __init__(self, base_path: str, index: int, dataname: str = None):
        self._base_path = base_path
        self._index = index
        self._account_name = compose_account_name(dataname, index)
        self._dataname_key = compute_data_name_key(self._account_name)

    def read(self, local_key: bytes) -> ParsedAccount:
        parsed_account = ParsedAccount()
        parsed_account.index = self._index
        parsed_account.info_data = self.read_mtp_data(local_key)
        return parsed_account

    def read_mtp_data(self, local_key: bytes) -> InfoData:
        mtp_data_file_path = os.path.join(self._base_path, self._dataname_key)
        version, mtp_data_settings = read_encrypted_file(mtp_data_file_path, local_key)
        blocks = read_settings_blocks(version, BytesIO(mtp_data_settings))
        mtp_authorization = blocks[SettingsBlocks.dbiMtpAuthorization]
        user_id = self.read_mtp_authorization(BytesIO(mtp_authorization))
        info_data = self.read_maps_data(local_key)
        mtp_data = InfoData()
        mtp_data.user_id = user_id
        mtp_data.name = info_data[1] + f'-' + info_data[0]
        mtp_data.phone = info_data[2]
        mtp_data.username = info_data[3]
        return mtp_data

    def read_mtp_authorization(self, data: BytesIO) -> int:
        legacy_user_id = read_qt_int32(data)
        legacy_main_dc_id = read_qt_int32(data)

        if legacy_user_id == -1 and legacy_main_dc_id == -1:
            user_id = read_qt_uint64(data)
        else:
            user_id = legacy_user_id
        return user_id

    def read_maps_data(self, local_key: bytes):
        info_data = []
        mtp_data_file_path = os.path.join(self._base_path, 'D877F783D5D3EF8C' + os.sep + 'maps')
        maps_tdf = read_tdf_file(mtp_data_file_path)
        decrypt_maps_data = decrypt_maps_tdf(maps_tdf,local_key)

        stream = BytesIO(decrypt_maps_data)
        stream.seek(4)
        Serialize = read_qt_byte_array(stream)
        stream.close()
        import io
        with io.BytesIO() as stream:
            stream.write(Serialize)
            stream.seek(8)
            if int.from_bytes(stream.read(8), 'big', signed=False) == 0x77FFFFFFFFFFFFFF:
                stream.read(12)
            if int.from_bytes(stream.read(4), 'big', signed=True) != -2147483648:
                stream.read(28)
                stream.read(int.from_bytes(stream.read(4), 'big', signed=True))
            size = int.from_bytes(stream.read(4), 'big', signed=True)
            stream.read(size + 4) if size > 0 else stream.read(4)
            for info in range(4):
                size = int.from_bytes(stream.read(4), 'big', signed=True)
                info_data.append(stream.read(size)) if size > 0 else info_data.append(b'')
        info_data = [get_value(info) for info in info_data]
        return info_data

class ParsedTdata:
    def __init__(self):
        self.proxy = None
        self.accounts: Dict[int, ParsedAccount] = None


class TdataReader:
    DEFAULT_DATANAME = 'data'

    def __init__(self, base_path: str, dataname: str = None):
        self._base_path = base_path
        self._dataname = dataname or TdataReader.DEFAULT_DATANAME

    def read(self, passcode: str = None) -> ParsedTdata:
        parsed_tdata = ParsedTdata()
        parsed_tdata.proxy = self.read_settings()
        local_key, account_indexes = self.read_key_data(passcode)

        accounts = {}
        for account_index in account_indexes:
            account_reader = AccountReader(self._base_path, account_index, self._dataname)
            accounts[account_index] = account_reader.read(local_key)

        parsed_tdata.accounts = accounts
        return parsed_tdata

    def read_key_data(self, passcode: str = None) -> Tuple[bytes, List[int]]:
        if passcode is None:
            passcode = ''

        key_data_tdf = read_tdf_file(self._path(self._key_data_name()))
        local_key, account_indexes_data = decrypt_key_data_tdf(passcode.encode(), key_data_tdf)
        account_indexes, _ = read_key_data_accounts(BytesIO(account_indexes_data))
        return local_key, account_indexes

    def read_settings(self):
        settings_tdf = read_tdf_file(self._path('settings'))
        settings_decrypted = decrypt_settings_tdf(settings_tdf)
        settings = read_settings_blocks(settings_tdf.version, BytesIO(settings_decrypted))
        return read_setting_authorization(settings[SettingsBlocks.dbiApplicationSettings])

    def _path(self, child: str) -> str:
        return os.path.join(self._base_path, child)

    def _key_data_name(self):
        return 'key_' + self._dataname

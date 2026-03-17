import datetime
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
        self.mtp_data: MtpData = None

    def __repr__(self):
        return f'ParsedAccount(index={self.index})'

class ParsedAccount1:
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


class MtpData:
    def __init__(self):
        self.user_id: int = None
        self.current_dc_id: int = None
        self.keys: Dict[int, bytes] = None
        self.keys_to_destroy: Dict[int, bytes] = None

    def __repr__(self):
        return f'MtpData(user_id={self.user_id})'


class InfoData:
    def __init__(self):
        self.user_id: int = None
        self.name: str = None
        self.phone: str = None
        self.username: str = None

    # def __repr__(self):
    #     return self


def read_mtp_authorization(data: BytesIO) -> MtpData:
    legacy_user_id = read_qt_int32(data)
    legacy_main_dc_id = read_qt_int32(data)

    if legacy_user_id == -1 and legacy_main_dc_id == -1:
        user_id = read_qt_uint64(data)
        main_dc_id = read_qt_int32(data)
    else:
        user_id = legacy_user_id
        main_dc_id = legacy_main_dc_id

    def read_keys():
        count = read_qt_int32(data)

        return {
            read_qt_int32(data): data.read(256)
            for _ in range(count)
        }

    mtp_data = MtpData()
    mtp_data.user_id = user_id
    mtp_data.current_dc_id = main_dc_id
    mtp_data.keys = read_keys()
    mtp_data.keys_to_destroy = read_keys()
    return mtp_data

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
            # 是否使用Ipv6
            # tryIPv6 = read_qt_int32(p_s)
            proxy_info['proxyuseipv6'] = read_qt_int32(p_s)
            # 是否使用代理打电话
            proxy_info['proxyuseforcall'] = read_qt_int32(p_s)
            # 设置中的哪一项0-1-2对应System-Enabled-Disabled
            proxy_info['proxytype'] = proxy_setting(read_qt_int32(p_s)).name
            # settings1 = proxy_setting(settings)
            # 正在使用的代理
            proxy_info['proxyselected'] = get_proxy(read_qt_byte_array(p_s))
            # 解析代理列表中每个代理
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
        parsed_account.mtp_data = self.read_mtp_data(local_key)
        return parsed_account

    def read1(self, local_key: bytes) -> ParsedAccount1:
        parsed_account = ParsedAccount1()
        parsed_account.index = self._index
        parsed_account.info_data = self.read_mtp_data1(local_key)
        return parsed_account

    def read_mtp_data(self, local_key: bytes) -> MtpData:
        mtp_data_file_path = os.path.join(self._base_path, self._dataname_key)
        #print(mtp_data_file_path)
        version, mtp_data_settings = read_encrypted_file(mtp_data_file_path, local_key)
        #print(mtp_data_settings)
        blocks = read_settings_blocks(version, BytesIO(mtp_data_settings))
        #print('blocks',blocks)
        mtp_authorization = blocks[SettingsBlocks.dbiMtpAuthorization]
        #print(mtp_authorization)
        return read_mtp_authorization(BytesIO(mtp_authorization))

    def read_mtp_data1(self, local_key: bytes) -> InfoData:
        mtp_data_file_path = os.path.join(self._base_path, self._dataname_key)
        #print(mtp_data_file_path)
        version, mtp_data_settings = read_encrypted_file(mtp_data_file_path, local_key)
        #print(mtp_data_settings)
        blocks = read_settings_blocks(version, BytesIO(mtp_data_settings))
        #print('blocks',blocks)
        mtp_authorization = blocks[SettingsBlocks.dbiMtpAuthorization]
        #print(mtp_authorization)
        user_id = self.read_mtp_authorization1(BytesIO(mtp_authorization))
        info_data = self.read_maps_data(local_key)
        mtp_data = InfoData()
        mtp_data.user_id = user_id
        mtp_data.name = info_data[1] + f'-' + info_data[0]
        mtp_data.phone = info_data[2]
        mtp_data.username = info_data[3]
        return mtp_data

    def read_mtp_authorization1(self, data: BytesIO) -> int:
        legacy_user_id = read_qt_int32(data)
        legacy_main_dc_id = read_qt_int32(data)

        if legacy_user_id == -1 and legacy_main_dc_id == -1:
            user_id = read_qt_uint64(data)
            main_dc_id = read_qt_int32(data)
        else:
            user_id = legacy_user_id
            main_dc_id = legacy_main_dc_id
        return user_id
        def read_keys():
            count = read_qt_int32(data)

            return {
                read_qt_int32(data): data.read(256)
                for _ in range(count)
            }

        mtp_data = InfoData()
        mtp_data.user_id = user_id
        mtp_data.current_dc_id = main_dc_id
        mtp_data.keys = read_keys()
        mtp_data.keys_to_destroy = read_keys()
        return mtp_data

    def read_maps_data(self, local_key: bytes):
        """
        解析 tdata/D877F783D5D3EF8C/maps 文件，解密并提取联系人基础信息（first_name、last_name、phone、username）以及 lastseen 等字段（仅用于调试打印）。
        参数:
          local_key: 从 key_data 解出的本地密钥，用于解密 maps.tdf 中的加密负载
        返回:
          [first_name, last_name, phone, username]（字符串，如遇空则为 ''）
        说明:
          本方法直接对 Telegram Desktop 使用的 Qt 序列化结构进行按字段偏移的跳读，未做完整模型化解析，注释尽量标明每一步的目的和原因。
        """
        # print(local_key)
        info_data = []
        # maps 文件位于 data 目录下 D877F783D5D3EF8C/maps。
        # 这里先按 TDF（Telegram Desktop 自定义容器）读取，再使用 local_key 解密出原始负载。
        mtp_data_file_path = os.path.join(self._base_path, 'D877F783D5D3EF8C\maps')
        maps_tdf = read_tdf_file(mtp_data_file_path)
        decrypt_maps_data = decrypt_maps_tdf(maps_tdf, local_key)

        # decrypt_maps_data 的开头通常是一个 4 字节的长度字段（int32），后面紧跟一个 Qt 的 QByteArray 数据块。
        # 早期调试时曾直接读取该长度并取其后的数据，见下面的注释代码。
        # import io
        # with io.BytesIO() as stream:
        #     stream.write(decrypt_maps_data)
        #     stream.seek(0)
        #     a = int.from_bytes(stream.read(4), 'big', signed=True)
        #     b = stream.read(a)

        # 为了统一使用已有的 Qt 读函数，这里先跳过前置的 4 字节长度，再直接 read_qt_byte_array 取得核心序列化负载 Serialize。
        stream = BytesIO(decrypt_maps_data)
        stream.seek(4)  # 跳过外层长度（int32）
        # a = read_qt_uint32(stream)
        Serialize = read_qt_byte_array(stream)  # 读取内部的 Qt QByteArray（length + data）
        stream.close()

        # 下面对 Serialize（内部真正的用户信息序列化块）做进一步解析。
        # 注意：这里并未构造完整的数据结构，而是按已知布局进行“跳读”，跳过用不到的字段，仅提取所需信息。
        import io
        import struct  # 保留作二进制调试用（当前未显式使用）

        with io.BytesIO() as stream:
            stream.write(Serialize)
            # 起始先跳过 8 字节的 peerIdSerialized（uint64）
            stream.seek(8)

            # 读取接下来的 8 字节，判断是否为特殊的版本标记 0x77FFFFFFFFFFFFFF。
            # 若等于该标记，则随后紧跟 version(int32) + photoId(uint64)，共 12 字节，这里按顺序跳过。
            if int.from_bytes(stream.read(8), 'big', signed=False) == 0x77FFFFFFFFFFFFFF:
                stream.read(12)  # version(4) + photoId(8)

            # 头像/图片尺寸等可能的占位字段：
            # 紧接着读取一个 int32，如果不是最小值 -2147483648，说明存在一段“图片/位置”相关的数据块：
            # - 先跳过 28 字节的固定字段（若按历史结构推断，包含若干个 int32/uint64 组合），
            # - 再读取一个长度（int32）并跳过对应长度的字节，这通常是一个 QByteArray（例如 fileReference 等）。
            if int.from_bytes(stream.read(4), 'big', signed=True) != -2147483648:
                stream.read(28)
                stream.read(int.from_bytes(stream.read(4), 'big', signed=True))

            # 继续读取一个长度 size，对应一个旧的 serialized 字段（历史兼容，当前未使用）。
            # 若 size > 0，额外包含紧随其后的 4 字节长度头，因此跳过 size + 4；否则也要跳过 4。
            size = int.from_bytes(stream.read(4), 'big', signed=True)
            stream.read(size + 4) if size > 0 else stream.read(4)

            # 接下来顺序读取 4 个“长度 + 数据”的块，对应：first_name、last_name、phone、username。
            # 若 size <= 0，表示该字段为空，直接追加空字节串 b''。
            for info in range(4):
                size = int.from_bytes(stream.read(4), 'big', signed=True)
                info_data.append(stream.read(size)) if size > 0 else info_data.append(b'')

            # 继续读取若干字段（这里保留变量名 a/b/c，保持与历史调试一致）：
            # a: 可能为 accessHash（uint64）；b: flags（int32）；c: 可能为 inlinePlaceholder（QByteArray）。
            a = read_qt_uint64(stream)
            b = read_qt_int32(stream)
            c = read_qt_byte_array(stream)

            # 最后读取 lastseen（uint32）。其高 2 位包含标志位，低 30 位是时间偏移，
            # 需要与 Telegram epoch（2013-08-01 00:00:00，Unix=1375315200）相加得到实际时间。
            lastseen = read_qt_uint32(stream)
            print(lastseen)  # 原始 lastseen（含标志位）
            lastseen1 = datetime.datetime.fromtimestamp((lastseen & 1073741823) + 1375315200)  # 0x3FFFFFFF = 1073741823，仅取低 30 位
            print(lastseen1)  # 解码后的“最近在线”时间（仅调试展示，不参与返回）

        # 将前面收集到的 4 个字节串字段转为字符串（UTF-8 或其他编码由 get_value() 自行处理）。
        info_data = [get_value(info) for info in info_data]
        return info_data

        # 下面是更详尽的字段逐个读取示例（保留作为参考），对应上面“跳读”的那些位置：
        # c = BytesIO(Serialize)
        # peerIdSerialized = hex(read_qt_uint64(c))
        # versionTag = read_qt_uint64(c)
        # print(c.tell())
        # if versionTag == 0x77FFFFFFFFFFFFFF:
        #     version = read_qt_int32(c)
        #     photoId = read_qt_uint64(c)
        #     print(c.tell())
        #     pass
        # else:
        #     photoId = versionTag
        # width = read_qt_int32(c)
        # min_number = -2147483648
        # if width == min_number:
        #     pass
        # else:
        #     height = read_qt_int32(c)
        #     dc = read_qt_int32(c)
        #     volume = read_qt_uint64(c)
        #     local = read_qt_int32(c)
        #     secret = read_qt_uint64(c)
        #     fileReference = read_qt_byte_array(c)
        #
        # # 有个已停产的字段，大概率不执行
        # print(c.tell())
        # serialized = read_qt_byte_array(c)
        # print(c.tell())
        # photoHasVideo = read_qt_int32(c)
        # print(c.tell())
        #
        # # first = read_qt_utf8(c)
        # # last = read_qt_utf8(c)
        # # phone = read_qt_utf8(c)
        # # username = read_qt_utf8(c)
        # first = read_qt_byte_array(c)
        # last = read_qt_byte_array(c)
        # phone = read_qt_byte_array(c)
        # username = read_qt_byte_array(c)
        #
        # access = read_qt_uint64(c)
        # flags = read_qt_int32(c)
        # inlinePlaceholder = read_qt_byte_array(c)
        #
        # lastseen = read_qt_uint32(c)
        #
        # contact = read_qt_int32(c)
        # botInfoVersion = read_qt_int32(c)
        #
        # # name = read_qt_byte_array(c)
        # # count = read_qt_int32(c)
        # # date = read_qt_int32(c)
        # # version = read_qt_int32(c)
        # # field1 = read_qt_int32(c)
        # # field2 = read_qt_int32(c)
        # # flags = read_qt_uint32(c)
        # # inviteLink = read_qt_byte_array(c)
        #
        # print(decrypt_maps_data)
        # return decrypt_maps_data
        #
        # # print(mtp_data_settings)


class ParsedTdata:
    def __init__(self):
        self.settings = None
        self.accounts: Dict[int, ParsedAccount] = None

class ParsedTdata1:
    def __init__(self):
        self.proxy = None
        self.accounts: Dict[int, ParsedAccount1] = None


class TdataReader:
    DEFAULT_DATANAME = 'data'

    def __init__(self, base_path: str, dataname: str = None):
        self._base_path = base_path
        self._dataname = dataname or TdataReader.DEFAULT_DATANAME

    def read(self, passcode: str = None) -> ParsedTdata1:

        parsed_tdata = ParsedTdata1()

        #不需要localkey
        parsed_tdata.proxy = self.read_settings()


        local_key, account_indexes = self.read_key_data(passcode)

        #parsed_tdata.maps = self.read_maps_data(local_key)

        accounts = {}

        for account_index in account_indexes:
            account_reader = AccountReader(self._base_path, account_index, self._dataname)
            accounts[account_index] = account_reader.read1(local_key)

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

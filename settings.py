from io import BytesIO
from enum import Enum

from qt import (
    read_qt_int32,
    read_qt_uint32,
    read_qt_int64,
    read_qt_uint64,
    read_qt_byte_array,
    read_qt_utf8, read_qt_uint16, read_qt_utf16, read_qt_uint8, read_qt_int
)
class proxy_setting(Enum):
    System = 0
    Enabled = 1
    Disabled = 2
class proxy_proxyType(Enum):
    NoneType = 0
    Socks5 =1
    Http=2
    Mtproto=3

class SettingsBlocks(Enum):
    dbiKey = 0x00
    dbiUser = 0x01

    dbiDcOptionOldOld = 0x02
    dbiChatSizeMaxOld = 0x03
    dbiMutePeerOld = 0x04
    dbiSendKeyOld = 0x05
    dbiAutoStart = 0x06
    dbiStartMinimized = 0x07
    dbiSoundFlashBounceNotifyOld = 0x08
    dbiWorkModeOld = 0x09
    dbiSeenTrayTooltip = 0x0a
    dbiDesktopNotifyOld = 0x0b
    dbiAutoUpdate = 0x0c
    dbiLastUpdateCheck = 0x0d
    dbiWindowPositionOld = 0x0e
    dbiConnectionTypeOldOld = 0x0f

    dbiDefaultAttach = 0x11
    dbiCatsAndDogsOld = 0x12
    dbiReplaceEmojiOld = 0x13
    dbiAskDownloadPathOld = 0x14
    dbiDownloadPathOldOld = 0x15
    dbiScaleOld = 0x16
    dbiEmojiTabOld = 0x17
    dbiRecentEmojiOldOldOld = 0x18
    dbiLoggedPhoneNumberOld = 0x19
    dbiMutedPeersOld = 0x1a

    dbiNotifyViewOld = 0x1c
    dbiSendToMenu = 0x1d
    dbiCompressPastedImageOld = 0x1e
    dbiLangOld = 0x1f
    dbiLangFileOld = 0x20
    dbiTileBackgroundOld = 0x21
    dbiAutoLockOld = 0x22
    dbiDialogLastPath = 0x23
    dbiRecentEmojiOldOld = 0x24
    dbiEmojiVariantsOldOld = 0x25
    dbiRecentStickers = 0x26
    dbiDcOptionOld = 0x27
    dbiTryIPv6Old = 0x28
    dbiSongVolumeOld = 0x29
    dbiWindowsNotificationsOld = 0x30
    dbiIncludeMutedOld = 0x31
    dbiMegagroupSizeMaxOld = 0x32
    dbiDownloadPathOld = 0x33
    dbiAutoDownloadOld = 0x34
    dbiSavedGifsLimitOld = 0x35
    dbiShowingSavedGifsOld = 0x36
    dbiAutoPlayOld = 0x37
    dbiAdaptiveForWideOld = 0x38
    dbiHiddenPinnedMessagesOld = 0x39
    dbiRecentEmojiOld = 0x3a
    dbiEmojiVariantsOld = 0x3b
    dbiDialogsModeOld = 0x40
    dbiModerateModeOld = 0x41
    dbiVideoVolumeOld = 0x42
    dbiStickersRecentLimitOld = 0x43
    dbiNativeNotificationsOld = 0x44
    dbiNotificationsCountOld = 0x45
    dbiNotificationsCornerOld = 0x46
    dbiThemeKeyOld = 0x47
    dbiDialogsWidthRatioOld = 0x48
    dbiUseExternalVideoPlayerOld = 0x49
    dbiDcOptionsOld = 0x4a
    dbiMtpAuthorization = 0x4b
    dbiLastSeenWarningSeenOld = 0x4c
    dbiSessionSettings = 0x4d
    dbiLangPackKey = 0x4e
    dbiConnectionTypeOld = 0x4f
    dbiStickersFavedLimitOld = 0x50
    dbiSuggestStickersByEmojiOld = 0x51
    dbiSuggestEmojiOld = 0x52
    dbiTxtDomainStringOldOld = 0x53
    dbiThemeKey = 0x54
    dbiTileBackground = 0x55
    dbiCacheSettingsOld = 0x56
    dbiPowerSaving = 0x57
    dbiScalePercent = 0x58
    dbiPlaybackSpeedOld = 0x59
    dbiLanguagesKey = 0x5a
    dbiCallSettingsOld = 0x5b
    dbiCacheSettings = 0x5c
    dbiTxtDomainStringOld = 0x5d
    dbiApplicationSettings = 0x5e
    dbiDialogsFiltersOld = 0x5f
    dbiFallbackProductionConfig = 0x60
    dbiBackgroundKey = 0x61

    dbiEncryptedWithSalt = 333
    dbiEncrypted = 444

    dbiVersion = 666


class lskType(int):  # nocov
    lskUserMap = 0x00
    lskDraft = 0x01  # data: PeerId peer
    lskDraftPosition = 0x02  # data: PeerId peer
    lskLegacyImages = 0x03  # legacy
    lskLocations = 0x04  # no data
    lskLegacyStickerImages = 0x05  # legacy
    lskLegacyAudios = 0x06  # legacy
    lskRecentStickersOld = 0x07  # no data
    lskBackgroundOldOld = 0x08  # no data
    lskUserSettings = 0x09  # no data
    lskRecentHashtagsAndBots = 0x0A  # no data
    lskStickersOld = 0x0B  # no data
    lskSavedPeersOld = 0x0C  # no data
    lskReportSpamStatusesOld = 0x0D  # no data
    lskSavedGifsOld = 0x0E  # no data
    lskSavedGifs = 0x0F  # no data
    lskStickersKeys = 0x10  # no data
    lskTrustedBots = 0x11  # no data
    lskFavedStickers = 0x12  # no data
    lskExportSettings = 0x13  # no data
    lskBackgroundOld = 0x14  # no data
    lskSelfSerialized = 0x15  # serialized self
    lskMasksKeys = 0x16  # no data
    lskCustomEmojiKeys = 0x17  # no data
    lskSearchSuggestions = 0x18  # no data
    lskWebviewTokens = 0x19  # data: QByteArray bots, QByteArray other


def read_boolean(data: BytesIO) -> bool:
    return read_qt_int32(data) == 1

def read_exact_bytes(data: BytesIO, size: int) -> bytes:
    value = data.read(size)
    if len(value) != size:
        raise StopIteration()
    return value

def read_qt_qstring(data: BytesIO) -> str:
    length = read_qt_int32(data)
    if length <= 0:
        return ''
    return read_exact_bytes(data, length).decode('utf-16-be', errors='ignore')

def read_qt_qbool(data: BytesIO) -> bool:
    return read_qt_uint8(data) != 0

def read_qt_list(data: BytesIO, item_reader):
    count = read_qt_uint32(data)
    return [item_reader(data) for _ in range(count)]

def read_qt_map(data: BytesIO, key_reader, value_reader):
    count = read_qt_uint32(data)
    return {
        key_reader(data): value_reader(data)
        for _ in range(count)
    }

def read_legacy_proxy(data: BytesIO):
    return {
        'proxy_type': read_qt_int32(data),
        'host': read_qt_qstring(data),
        'port': read_qt_int32(data),
        'user': read_qt_qstring(data),
        'password': read_qt_qstring(data)
    }


BOOLEAN_BLOCKS = {
    SettingsBlocks.dbiAutoStart,
    SettingsBlocks.dbiStartMinimized,
    SettingsBlocks.dbiSendToMenu,
    SettingsBlocks.dbiSeenTrayTooltip,
    SettingsBlocks.dbiAutoUpdate,
}

INT32_BLOCKS = {
    SettingsBlocks.dbiChatSizeMaxOld,
    SettingsBlocks.dbiSavedGifsLimitOld,
    SettingsBlocks.dbiStickersRecentLimitOld,
    SettingsBlocks.dbiStickersFavedLimitOld,
    SettingsBlocks.dbiMegagroupSizeMaxOld,
    SettingsBlocks.dbiUseExternalVideoPlayerOld,
    SettingsBlocks.dbiPowerSaving,
    SettingsBlocks.dbiSoundFlashBounceNotifyOld,
    SettingsBlocks.dbiAutoPlayOld,
    SettingsBlocks.dbiDialogsFiltersOld,
    SettingsBlocks.dbiModerateModeOld,
    SettingsBlocks.dbiIncludeMutedOld,
    SettingsBlocks.dbiShowingSavedGifsOld,
    SettingsBlocks.dbiDesktopNotifyOld,
    SettingsBlocks.dbiWindowsNotificationsOld,
    SettingsBlocks.dbiNativeNotificationsOld,
    SettingsBlocks.dbiNotificationsCountOld,
    SettingsBlocks.dbiNotificationsCornerOld,
    SettingsBlocks.dbiDialogsWidthRatioOld,
    SettingsBlocks.dbiLastSeenWarningSeenOld,
    SettingsBlocks.dbiWorkModeOld,
    SettingsBlocks.dbiTryIPv6Old,
    SettingsBlocks.dbiLastUpdateCheck,
    SettingsBlocks.dbiScaleOld,
    SettingsBlocks.dbiScalePercent,
    SettingsBlocks.dbiLangOld,
    SettingsBlocks.dbiSendKeyOld,
    SettingsBlocks.dbiCatsAndDogsOld,
    SettingsBlocks.dbiTileBackgroundOld,
    SettingsBlocks.dbiAdaptiveForWideOld,
    SettingsBlocks.dbiAutoLockOld,
    SettingsBlocks.dbiReplaceEmojiOld,
    SettingsBlocks.dbiSuggestEmojiOld,
    SettingsBlocks.dbiSuggestStickersByEmojiOld,
    SettingsBlocks.dbiDefaultAttach,
    SettingsBlocks.dbiNotifyViewOld,
    SettingsBlocks.dbiAskDownloadPathOld,
    SettingsBlocks.dbiCompressPastedImageOld,
    SettingsBlocks.dbiEmojiTabOld,
    SettingsBlocks.dbiVideoVolumeOld,
    SettingsBlocks.dbiPlaybackSpeedOld,
}

UINT64_BLOCKS = {
    SettingsBlocks.dbiThemeKeyOld,
    SettingsBlocks.dbiLangPackKey,
    SettingsBlocks.dbiLanguagesKey,
    SettingsBlocks.dbiMutePeerOld,
}

BYTE_ARRAY_BLOCKS = {
    SettingsBlocks.dbiDcOptionsOld,
    SettingsBlocks.dbiApplicationSettings,
    SettingsBlocks.dbiMtpAuthorization,
    SettingsBlocks.dbiSessionSettings,
    SettingsBlocks.dbiCallSettingsOld,
    SettingsBlocks.dbiFallbackProductionConfig,
}

QSTRING_BLOCKS = {
    SettingsBlocks.dbiTxtDomainStringOldOld,
    SettingsBlocks.dbiTxtDomainStringOld,
    SettingsBlocks.dbiLangFileOld,
    SettingsBlocks.dbiLoggedPhoneNumberOld,
    SettingsBlocks.dbiDownloadPathOldOld,
    SettingsBlocks.dbiDialogLastPath,
}

def read_settings_block(verison, data: BytesIO, block_id: SettingsBlocks):
    if block_id == SettingsBlocks.dbiKey:
        return {
            'dc_id': read_qt_int32(data),
            'key': read_exact_bytes(data, 256)
        }

    if block_id == SettingsBlocks.dbiUser:
        return {
            'user_id': read_qt_int32(data),
            'dc_id': read_qt_uint32(data)
        }

    if block_id in BOOLEAN_BLOCKS:
        return read_boolean(data)

    if block_id in INT32_BLOCKS:
        return read_qt_int32(data)

    if block_id in UINT64_BLOCKS:
        return read_qt_uint64(data)

    if block_id in BYTE_ARRAY_BLOCKS:
        return read_qt_byte_array(data)

    if block_id in QSTRING_BLOCKS:
        return read_qt_qstring(data)

    if block_id == SettingsBlocks.dbiSongVolumeOld:
        return read_qt_int32(data) / 1e6

    if block_id == SettingsBlocks.dbiDcOptionOldOld:
        return {
            'dc_id': read_qt_uint32(data),
            'host': read_qt_qstring(data),
            'ip': read_qt_qstring(data),
            'port': read_qt_uint32(data)
        }

    if block_id == SettingsBlocks.dbiDcOptionOld:
        return {
            'dc_id_with_shift': read_qt_uint32(data),
            'flags': read_qt_int32(data),
            'ip': read_qt_qstring(data),
            'port': read_qt_uint32(data)
        }

    if block_id == SettingsBlocks.dbiCacheSettingsOld:
        return {
            'size': read_qt_int64(data),
            'time': read_qt_int32(data)
        }

    if block_id == SettingsBlocks.dbiCacheSettings:
        return {
            'size': read_qt_int64(data),
            'time': read_qt_int32(data),
            'size_big': read_qt_int64(data),
            'time_big': read_qt_int32(data)
        }

    if block_id == SettingsBlocks.dbiAutoDownloadOld:
        return {
            'photo': read_qt_int32(data),
            'audio': read_qt_int32(data),
            'gif': read_qt_int32(data)
        }

    if block_id == SettingsBlocks.dbiDialogsModeOld:
        return {
            'enabled': read_qt_int32(data),
            'mode': read_qt_int32(data)
        }

    if block_id == SettingsBlocks.dbiConnectionTypeOldOld:
        connection_type = read_qt_int32(data)
        result = {'connection_type': connection_type}
        if connection_type in (2, 3):
            result['proxy'] = {
                'host': read_qt_qstring(data),
                'port': read_qt_int32(data),
                'user': read_qt_qstring(data),
                'password': read_qt_qstring(data)
            }
        return result

    if block_id == SettingsBlocks.dbiConnectionTypeOld:
        connection_type = read_qt_int32(data)
        result = {'connection_type': connection_type}
        if connection_type in (4, 5):
            count = read_qt_int32(data)
            index = read_qt_int32(data)
            settings = read_qt_int32(data) if connection_type == 5 else 0
            calls = read_qt_int32(data) if connection_type == 5 else None
            proxies = [read_legacy_proxy(data) for _ in range(count)]
            result.update({
                'count': count,
                'index': index,
                'settings': settings,
                'calls': calls,
                'proxies': proxies
            })
        else:
            result['proxy'] = read_legacy_proxy(data)
        return result

    if block_id == SettingsBlocks.dbiThemeKey:
        return {
            'day': read_qt_uint64(data),
            'night': read_qt_uint64(data),
            'night_mode': read_boolean(data)
        }

    if block_id == SettingsBlocks.dbiBackgroundKey:
        return {
            'day': read_qt_uint64(data),
            'night': read_qt_uint64(data)
        }

    if block_id == SettingsBlocks.dbiTileBackground:
        return {
            'day': read_qt_int32(data),
            'night': read_qt_int32(data)
        }

    if block_id == SettingsBlocks.dbiWindowPositionOld:
        return {
            'x': read_qt_int32(data),
            'y': read_qt_int32(data),
            'w': read_qt_int32(data),
            'h': read_qt_int32(data),
            'moncrc': read_qt_int32(data),
            'maximized': read_qt_qbool(data)
        }

    if block_id == SettingsBlocks.dbiMutedPeersOld:
        count = read_qt_uint32(data)
        return [read_qt_uint64(data) for _ in range(count)]

    if block_id == SettingsBlocks.dbiDownloadPathOld:
        return {
            'path': read_qt_qstring(data),
            'bookmark': read_qt_byte_array(data)
        }

    if block_id == SettingsBlocks.dbiRecentEmojiOldOldOld:
        return read_qt_list(
            data,
            lambda stream: (read_qt_uint32(stream), read_qt_uint16(stream))
        )

    if block_id == SettingsBlocks.dbiRecentEmojiOldOld:
        return read_qt_list(
            data,
            lambda stream: (read_qt_uint64(stream), read_qt_uint16(stream))
        )

    if block_id == SettingsBlocks.dbiRecentEmojiOld:
        return read_qt_list(
            data,
            lambda stream: (read_qt_qstring(stream), read_qt_uint16(stream))
        )

    if block_id == SettingsBlocks.dbiRecentStickers:
        return read_qt_list(
            data,
            lambda stream: (read_qt_uint64(stream), read_qt_uint16(stream))
        )

    if block_id == SettingsBlocks.dbiEmojiVariantsOldOld:
        return read_qt_map(data, read_qt_uint32, read_qt_uint64)

    if block_id == SettingsBlocks.dbiEmojiVariantsOld:
        return read_qt_map(data, read_qt_qstring, read_qt_int32)

    if block_id == SettingsBlocks.dbiHiddenPinnedMessagesOld:
        return read_qt_map(data, read_qt_uint64, read_qt_int32)

    raise Exception(f'Unknown block ID while reading settings: {block_id}')


def read_settings_blocks(version, data: BytesIO):
    blocks = {}
    try:
        while True:
            raw_block_id = read_qt_int32(data)
            try:
                block_id = SettingsBlocks(raw_block_id)
            except ValueError as exc:
                raise Exception(
                    f'Unknown raw block ID while reading settings: 0x{raw_block_id:08X} ({raw_block_id})'
                ) from exc
            block_data = read_settings_block(version, data, block_id)
            existing = blocks.get(block_id)
            if existing is None:
                blocks[block_id] = block_data
            elif isinstance(existing, list):
                existing.append(block_data)
            else:
                blocks[block_id] = [existing, block_data]
    except StopIteration:
        pass

    return blocks

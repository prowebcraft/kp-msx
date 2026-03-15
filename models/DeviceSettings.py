import config
from util import msx


class DeviceSettings:

    def __init__(self, data):
        if data is None:
            data = {}

        self.menu_blacklist = data.get('menu_blacklist', [])
        self.fourk = data.get('fourk', False)
        self.proxy = data.get('proxy', False)
        self.alternative_player = data.get('alternative_player', False)
        self.hevc = data.get('hevc', False)
        self.hdr = data.get('hdr', False)
        self.mixed_playlist = data.get('mixed_playlist', False)
        self.poster_size = data.get('poster_size', 'large')
        self.poster_proxy = data.get('poster_proxy', None)
        self.server = data.get('server', msx.LENNY)

    def to_dict(self):
        return {
            'menu_blacklist': self.menu_blacklist,
            'fourk': self.fourk,
            'proxy': self.proxy,
            'alternative_player': self.alternative_player,
            'hevc': self.hevc,
            'hdr': self.hdr,
            'mixed_playlist': self.mixed_playlist,
            'poster_size': self.poster_size,
            'poster_proxy': self.poster_proxy,
            'server': self.server
        }

    def to_fourk_msx_button(self):
        entry = msx.settings_button(
            msx.FOURK_ID, '4K',
            msx.format_action(f'/msx/settings/toggle/{msx.FOURK_ID}', module='execute'),
            "Выключатель 4К. Если телевизор старый, слабый или дешёвый, то лучше не включать."
        )
        entry.update(msx.stamp(self.fourk))
        return entry

    def to_hdr_msx_button(self):
        entry = msx.settings_button(
            msx.HDR_ID, 'HDR',
            msx.format_action(f'/msx/settings/toggle/{msx.HDR_ID}', module='execute'),
            "Выключатель HDR. Если телевизор старый, слабый или дешёвый, то лучше не включать."
        )
        entry.update(msx.stamp(self.hdr))
        return entry

    def to_hevc_msx_button(self):
        entry = msx.settings_button(
            msx.HEVC_ID, 'HEVC',
            msx.format_action(f'/msx/settings/toggle/{msx.HEVC_ID}', module='execute'),
            "Выключатель HEVC. Если телевизор старый, слабый или дешёвый, то лучше не включать."
        )
        entry.update(msx.stamp(self.hevc))
        return entry

    def to_mixed_playlist_msx_button(self):
        entry = msx.settings_button(
            msx.MIXED_PLAYLIST_ID, 'Смешанный плейлист',
            msx.format_action(f'/msx/settings/toggle/{msx.MIXED_PLAYLIST_ID}', module='execute'),
            "Выключатель смешанного плейлиста. Если телевизор старый, слабый или дешёвый, то лучше не включать."
        )
        entry.update(msx.stamp(self.mixed_playlist))
        return entry

    def to_server_msx_button(self):
        entry = msx.settings_button(
            msx.SERVER_ID, f'Сервер: {self.server}',
            msx.format_action(f'/msx/settings/toggle/{msx.SERVER_ID}', module='execute'),
            "Переключатель сервера. Для определения лучшего сервера используйте zamerka.com."
        )
        return entry

    def to_proxy_msx_button(self):
        entry = msx.settings_button(
            msx.PROXY_ID, 'Прокси для плейлиста',
            msx.format_action(f'/msx/settings/toggle/{msx.PROXY_ID}', module='execute'),
            "Включите, если видео не загружаются вообще (нет длительности, нет дорожек и субтитров в настройках плеера)."
        )
        entry.update(msx.stamp(self.proxy))
        return entry

    def to_alternative_player_msx_button(self):
        entry = msx.settings_button(
            msx.ALTERNATIVE_PLAYER_ID, 'Альтернативный плеер',
            msx.format_action(f'/msx/settings/toggle/{msx.ALTERNATIVE_PLAYER_ID}', module='execute'),
            "Включите, если телевизор очень старый (Tizen или webOS до 3 версии, год выпуска ТВ до 2018 года)."
        )
        entry.update(msx.stamp(self.alternative_player))
        return entry

    def to_posters_msx_button(self):
        entry = msx.settings_button(
            msx.POSTERS_ID, 'Ремонт постеров',
            msx.format_action(f'/msx/settings/posters', module='panel'),
            "Настройки загрузки постеров. Требуется перезапуск приложения."
        )
        return entry

    def to_menu_msx_button(self):
        entry = msx.settings_button(
            msx.MENU_ID, 'Пункты меню',
            msx.format_action(f'/msx/settings/menu_entries', module='panel'),
            "Здесь можно выключить или включить разделы главного меню слева. После изменения потребуется перезапустить приложение"
        )
        return entry

    def to_help_msx_button(self):
        entry = msx.settings_button(
            msx.HELP_ID, 'Справка','[]',
            "Исходный код: https://github.com/slonopot/kp-msx\n"
            f"Плеер: {config.PLAYER}\n"
            f"Альтернативный плеер: {config.ALTERNATIVE_PLAYER}\n"
            f"Протокол: {config.PROTOCOL}"
        )
        return entry



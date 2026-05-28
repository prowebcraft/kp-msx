import config
from util import msx


class Category:

    BLACKLIST = ['4k']

    STATIC_CATEGORIES = [
        lambda: {'id': 'continue', 'title': 'Продолжить просмотр', 'icon': 'play-circle-outline', 'path': '/msx/continue'},
        lambda: {'id': 'new', 'title': 'Новинки', 'path': '/msx/category', 'params': {'sort': 'created-', 'page': '{PAGE}'}, 'interaction': f'{config.MSX_HOST}/paging.html'},
        lambda: {'id': 'toons', 'title': 'Мультфильмы', 'path': '/msx/category', 'params': {'genre': '23', 'page': '{PAGE}'}, 'interaction': f'{config.MSX_HOST}/paging.html'},
        lambda: {'id': 'anime', 'title': 'Аниме', 'path': '/msx/category', 'params': {'genre': '25', 'page': '{PAGE}'}, 'interaction': f'{config.MSX_HOST}/paging.html'},
        lambda: {'id': 'collections', 'title': 'Подборки', 'path': '/msx/collections', 'params': {'page': '{PAGE}'}, 'interaction': f'{config.MSX_HOST}/paging.html'},
        lambda: {'id': 'sport', 'title': 'Спорт', 'path': '/msx/tv'},
        lambda: {'id': 'search', 'title': 'Поиск', 'icon': 'search', 'path': '/msx/search', 'params': {'q': '{INPUT}'}, 'interaction': 'http://msx.benzac.de/interaction/input.html', 'options': 'search:3|ru|Поиск'},
        lambda: {'id': 'bookmarks', 'title': 'Закладки', 'icon': 'bookmark', 'path': '/msx/bookmarks'},
        lambda: {'id': 'history', 'title': 'История', 'icon': 'history', 'path': '/msx/history', 'params': {'page': '{PAGE}'}, 'interaction': f'{config.MSX_HOST}/paging.html'},
        lambda: {'id': 'watching', 'title': 'Я смотрю', 'icon': 'tv', 'path': '/msx/watching'},
        lambda: {'id': 'settings', 'title': 'Настройки', 'icon': 'settings', 'path': '/msx/settings/screen'}
    ]

    def __init__(self, data, blacklisted : bool = False):
        self.id = data.get('id')
        self.title = data.get('title')
        self.blacklisted = self.id in Category.BLACKLIST or blacklisted
        self.ignored = self.id in Category.BLACKLIST

        self.path = data.get('path')
        self.icon = data.get('icon')
        self.params = {}
        self.interaction = None
        self.options = None

        if self.path is None:
            # Built-in category
            self.path = '/msx/category'
            self.params = {'category': self.id, 'page': '{PAGE}'}
            self.interaction = f'{config.MSX_HOST}/paging.html'
        else:
            # Custom category
            self.params = data.get('params', {})
            self.interaction = data.get('interaction')
            self.options = data.get('options')

    def to_msx(self):
        return {
            "type": "default",
            "label": self.title,
            "icon": self.icon,
            "data": msx.format_action(self.path, params=self.params, interaction=self.interaction, options=self.options)
        }

    def to_msx_settings_button(self):
        entry = {
            'id': self.id,
            "label": self.title,
            'action': msx.format_action(f'/msx/settings/toggle_menu_entry/{self.id}', module='execute')
        }
        entry.update(msx.stamp(not self.blacklisted))
        return entry

    @classmethod
    def static_categories(cls):
        return [cls(i()) for i in Category.STATIC_CATEGORIES]

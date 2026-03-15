from models.DeviceSettings import DeviceSettings
from models.Poster import Poster
from util import msx


class Collection:

    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.poster = Poster((data.get('posters') or {}))

    def to_msx(self, device_settings: 'DeviceSettings' = None):
        return {
            'title': self.title,
            'truncation': 'title',
            'image': self.poster.get(device_settings),
            'action': msx.format_action('/msx/collection', params={'collection_id': self.id}, module='content')
        }

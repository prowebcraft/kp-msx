from urllib.parse import urlencode

import config
from models.Playable import Playable
from models.SubtitleTrack import SubtitleTrack
from util import msx
from util.msx import content
from util.proxy import remember_domain, make_proxy_url

class Video(Playable):

    def __init__(self, data, content_id, content_title):
        super().__init__(data)

        self.content_id = content_id
        self.content_title = content_title

        self.title = data.get('title')

    def to_multivideo_entry(self, device_settings: 'DeviceSettings'=None) -> 'SubtitleTrack':
        entry = {
            "label": self.title,
            'action': self.msx_action(device_settings=device_settings),
            'properties': self.msx_properties(device_settings=device_settings),
        }
        return entry


    def trigger_ready(self):
        params = {
            'content_id': self.content_id
        }
        return msx.format_action('/msx/play', params=params, module='execute')

    def resume_key(self):
        return str(self.content_id) + ' ' + self.player_title() + ' ' + self.title

    def player_title(self):
        return self.content_title

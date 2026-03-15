from models.Episode import Episode



class Season:

    def __init__(self, data, content_id):
        self.content_id = content_id

        self.n = data.get('number')
        self.id = data.get('id')
        self.episodes = [Episode(i, content_id, self.n) for i in data.get('episodes')]

        self.watched = self._watched()

    def to_episode_pages(self, device_settings: 'DeviceSettings' = None):
        items = []
        for i, episode in enumerate(self.episodes):
            entry = {
                "label": episode.menu_title(),
                "playerLabel": episode.player_title(),
                'action': episode.msx_action(device_settings=device_settings),
                'stamp': '{ico:check}' if episode.watched else None,
                'focus': not episode.watched,
                'properties': episode.msx_properties(device_settings=device_settings),
            }
            items.append(entry)
        return items

    def _watched(self):
        watched = True
        for episode in self.episodes:
            watched = watched and episode.watched
        return watched
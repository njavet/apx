# general imports
import importlib

# project imports
from utils import exceptions


class StringProcessor:
    def __init__(self, emojis):
        self.emojis = emojis
        self.activity_processors = {}

    def process_string(self, input_string, user_id, recv_time=None):
        emoji, payload, comment = self._parse_activity(input_string)

        emoji_mapping = self.emojis[emoji]
        if '.' in emoji_mapping:
            module_name, unit_name = emoji_mapping.split('.')
        else:
            module_name, unit_name = emoji_mapping, None

        ap = self._load_activity_processor(emoji, module_name)

        # module specific activity processing
        ap.init_activity_unit(user_id, emoji, unit_name, comment)
        ap.activity.set_time(recv_time)
        ap.process_activity(payload)

    def _parse_activity(self, input_string):
        parts = input_string.split('//', 1)
        emoji_payload = parts[0]
        comment = parts[1] if len(parts) > 1 else None

        if not emoji_payload:
            raise exceptions.InvalidActivityError('Input is empty')

        emoji, payload = emoji_payload.split(maxsplit=1)

        if emoji not in self.emojis:
            raise exceptions.InvalidActivityError('Invalid emoji: {}'.format(emoji))

        return emoji, payload, comment

    def _load_activity_processor(self, emoji, name):
        if emoji not in self.activity_processors:
            module = importlib.import_module('apx.activities.' + name)
            ap = module.ActivityProcessor()
            self.activity_processors[emoji] = ap
        return self.activity_processors[emoji]


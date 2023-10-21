# general imports
import importlib

# project imports
from apx.utils import exceptions


class StringProcessor:
    def __init__(self, emojis):
        self.emojis = emojis
        self.activity_processors = {}

    def process_string(self, input_string, user_id, recv_time=None):
        emoji, payload, comment = self._parse_activity(input_string)
        module_name, unit_name = self._parse_names(self.emojis[emoji])
        ap = self._load_activity_processor(emoji, module_name)

        # module specific activity processing
        try:
            ap.process_activity(user_id, emoji, payload, recv_time, unit_name, comment)
        except exceptions.ActivityProcessingError as e:
            return ProcessingResult(False, error=str(e))
        except exceptions.ActivityProcessingWarning as e:
            return ProcessingResult(True, warning=str(e))
        else:
            return ProcessingResult(True)

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

    @staticmethod
    def _parse_names(emoji_mapping):
        if '.' in emoji_mapping:
            module_name, unit_name = emoji_mapping.split('.')
        else:
            module_name, unit_name = emoji_mapping, None
        return module_name, unit_name

    def _load_activity_processor(self, emoji, name):
        if emoji not in self.activity_processors:
            module = importlib.import_module('apx.activities.' + name)
            ap = module.ActivityProcessor()
            self.activity_processors[emoji] = ap
        return self.activity_processors[emoji]


class ProcessingResult:
    def __init__(self, success, data=None, warning=None, error=None):
        self.success = success
        self.data = data
        self.warning = warning
        self.error = error

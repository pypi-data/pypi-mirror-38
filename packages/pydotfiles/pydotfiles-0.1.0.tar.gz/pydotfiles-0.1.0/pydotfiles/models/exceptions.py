from .enums import PydotfilesErrorReason


class PydotfilesError(Exception):

    def __init__(self, reason, help_message_override=None):
        super().__init__()
        self.reason = reason
        self.help_message_override = help_message_override

    @property
    def help_message(self):
        return PydotfilesErrorReason.get_help_message(self.reason) if self.help_message_override is None else self.help_message_override

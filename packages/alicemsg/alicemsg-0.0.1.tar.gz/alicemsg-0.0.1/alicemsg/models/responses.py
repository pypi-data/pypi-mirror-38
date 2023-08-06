from .messages import Message


class AliceResponse(object):
    def __init__(self, message: Message, session: dict, version: str = '1.0'):
        if not isinstance(message, Message):
            raise TypeError('Response.message must be an instance of Message')
        if not isinstance(session, dict):
            raise TypeError('Response.session must be an instance of dict')
        if not isinstance(version, str):
            raise TypeError('Response.version must be an instance of str')
        session_keys = ('session_id', 'message_id', 'user_id')
        self.message = message
        self.session = {key: session[key] for key in session_keys}
        self.version = version

    def to_dict(self):
        return {
            'response': self.message.to_dict(),
            'session': self.session,
            'version': self.version
        }

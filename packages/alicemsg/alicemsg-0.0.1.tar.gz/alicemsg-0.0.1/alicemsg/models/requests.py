class CallbackRequest(object):
    def __init__(self, session: dict, locale: str, timezone: str, payload):
        if not isinstance(session, dict):
            raise TypeError('CallbackRequest.session must be an instance of dict')
        if not isinstance(locale, str):
            raise TypeError('CallbackRequest.locale must be an instance of str')
        if not isinstance(timezone, str):
            raise TypeError('CallbackRequest.timezone must be an instance of str')
        self.session = session
        self.locale = locale
        self.timezone = timezone
        self.payload = payload


class TextMessageRequest(object):
    def __init__(self, session: dict, locale: str, timezone: str, text: str, tokens: list):
        if not isinstance(session, dict):
            raise TypeError('TextMessageRequest.session must be an instance of dict')
        if not isinstance(locale, str):
            raise TypeError('TextMessageRequest.locale must be an instance of str')
        if not isinstance(timezone, str):
            raise TypeError('TextMessageRequest.timezone must be an instance of str')
        if not isinstance(text, str):
            raise TypeError('TextMessageRequest.text must be an instance of str')
        if not isinstance(tokens, list):
            raise TypeError('TextMessageRequest.tokens must be an instance of list')
        self.session = session
        self.locale = locale
        self.timezone = timezone
        self.text = text
        self.tokens = tokens

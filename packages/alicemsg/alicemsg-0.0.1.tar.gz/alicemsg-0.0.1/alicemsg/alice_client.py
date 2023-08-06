from .models.messages import Message
from .models.requests import CallbackRequest, TextMessageRequest
from .models.responses import AliceResponse


class AliceClient:
    def __init__(self):
        self.text_message_processor = None
        self.callback_processor = None

    def register_text_message_processor(self):
        def add(processor):
            self.text_message_processor = processor
            return processor

        return add

    def register_callback_processor(self):
        def add(processor):
            self.callback_processor = processor
            return processor

        return add

    def process_json(self, msg_json: dict):
        if not isinstance(msg_json, dict):
            raise TypeError('msg_json must be an instance of dict')
        if 'request' not in msg_json:
            raise KeyError('msg_json must contain field "request"')
        if 'type' not in msg_json['request']:
            raise KeyError('msg_json.request must contain field "type"')
        if not isinstance(msg_json['request']['type'], str):
            raise TypeError('msg_json.request.type must be an instance of str')
        if msg_json['request']['type'] == 'SimpleUtterance':
            if not self.text_message_processor:
                raise AttributeError('text_message_processor not declared')
            request = TextMessageRequest(
                session={'session_id': msg_json['session']['session_id'], 'user_id': msg_json['session']['user_id']},
                locale=msg_json['meta']['locale'], timezone=msg_json['meta']['timezone'],
                text=msg_json['request']['command'], tokens=msg_json['request']['nlu']['tokens'])
            message = self.text_message_processor(request)
            if not isinstance(message, Message):
                raise TypeError('message must be an instance of Message')
            return AliceResponse(message=message, session=msg_json['session'], version=msg_json['version'])
        elif msg_json['request']['type'] == 'ButtonPressed':
            if not self.callback_processor:
                raise AttributeError('callback_processor not declared')
            request = CallbackRequest(
                session={'session_id': msg_json['session']['session_id'], 'user_id': msg_json['session']['user_id']},
                locale=msg_json['meta']['locale'], timezone=msg_json['meta']['timezone'],
                payload=msg_json['request']['payload'])
            message = self.callback_processor(request)
            if not isinstance(message, Message):
                raise TypeError('message must be an instance of Message')
            return AliceResponse(message=message, session=msg_json['session'], version=msg_json['version'])
        else:
            raise ValueError('msg_json.request.type must have value "SimpleUtterance" or "ButtonPressed"')

class Button(object):
    def __init__(self, title: str, url: str = None, payload=None, hide: bool = True):
        if not isinstance(title, str):
            raise TypeError('Button.title must be an instance of str')
        if url is not None:
            if not isinstance(url, str):
                raise TypeError('Button.url must be an instance of str')
        if not isinstance(hide, bool):
            raise TypeError('Button.hide must be an instance of bool')
        self.title = title
        self.url = url
        self.payload = payload
        self.hide = hide

    def to_dict(self):
        result = {'title': self.title, 'hide': self.hide}
        if self.url:
            result['url'] = self.url
        if self.payload:
            result['payload'] = self.payload
        return result


class Buttons(object):
    def __init__(self, buttons: list = None):
        self.buttons = []
        if buttons:
            if not isinstance(buttons, list):
                raise TypeError('Buttons.buttons must be an instance of list')
            for button in buttons:
                if not isinstance(button, Button):
                    raise TypeError('Buttons.buttons items must be an instance of Button')
            self.buttons = buttons

    def add(self, button: Button):
        if not isinstance(button, Button):
            raise TypeError('button items must be an instance of Button')
        self.buttons.append(button)

    def to_dict(self):
        return [button.to_dict() for button in self.buttons]


class Message(object):
    def __init__(self, text: str, buttons: Buttons = None, end_session: bool = False):
        if not isinstance(text, str):
            raise TypeError('Message.text must be an instance of str')
        if not isinstance(end_session, bool):
            raise TypeError('Message.end_session must be an instance of bool')
        self.text = text
        self.end_session = end_session
        if buttons:
            if not isinstance(buttons, Buttons):
                raise TypeError('Message.buttons must be an instance of Buttons')
        self.buttons = buttons

    def to_dict(self):
        result = {'text': self.text, 'end_session': self.end_session}
        if self.buttons:
            result['buttons'] = self.buttons.to_dict()
        return result

class Card:
    def to_dict(self):
        pass


class SimpleCard(Card):
    def __init__(self, title: str=None, content: str=None):
        self.type = "Simple"
        self.title = title
        self.content = content

    def to_dict(self):
        d = {
            'type': self.type,
            'title': self.title,
            'content': self.content
        }
        return d


class StandardCard(Card):
    def __init__(self, title: str=None, text: str=None, small_image_url: str=None, large_item_url: str=None):
        self.type = "Standard"
        self.title = title
        self.text = text
        self.small_image_url = small_image_url
        self.large_item_url = large_item_url

    def to_dict(self):
        d = {
            'type': self.type,
            'title': self.title,
            'text': self.text
        }
        if self.small_image_url or self.large_item_url:
            d['image'] = {}
            if self.small_image_url:
                d['image']['smallImageUrl'] = self.small_image_url
            if self.large_item_url:
                d['image']['large_item_url'] = self.large_item_url

        return d


class LinkAccountCard(Card):
    def __init__(self):
        self.type = "LinkAccount"

    def to_dict(self):
        d = {
            'type': self.type
        }
        return d


class AskForPermissionsConsentCard(Card):
    def __init__(self, title: str=None, content: str=None, text: str=None):
        self.type = "AskForPermissionsConsent"
        self.title = title
        self.content = content
        self.text = text

    def to_dict(self):
        d = {
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'text': self.text
        }
        return d

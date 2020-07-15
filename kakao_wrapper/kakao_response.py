# -*- coding: utf-8 -*-
class KakaoChatbotResponse:
    def __init__(self):
        self.data = {}
        self.data['version'] = "2.0"
        self.SkillTemplate = {}

    def create_response(self):
        import json
        self.data['template'] = self.SkillTemplate
        return json.dumps(self.data)

    def add_quickreply(self, data, title, type="message"):
        if type == "block":
            quickreply = {'label': title, 'action': 'block', 'blockId': data}

        elif type == "message":
            quickreply = {'label': title, 'action': 'message', 'messageText': data}

        try:
            self.SkillTemplate['quickReplies'].append(quickreply)
        except KeyError:
            self.SkillTemplate['quickReplies'] = [quickreply]

    def add_output(self, data):
        try:
            self.SkillTemplate['outputs'].append(data)
        except KeyError:
            self.SkillTemplate['outputs'] = [data]

    def text(self, data):
        if len(data) > 1000:
            raise BaseException
        SimpleText = {'simpleText': {'text': data}}
        return SimpleText

    def image(self, url, caption):
        SimpleImage = {'simpleImage': {'imageUrl': url, 'altText': caption}}
        return SimpleImage

    def create_thumbnail(self, url, link=None):
        if link is not None:
            return {'imageUrl': url, 'link': {'web': link}}
        else:
            return {'imageUrl': url}

    def create_button(self, data, action, **kwargs):
        button = {'label': data, 'action': action}

        if action == 'webLink':
            button['webLinkUrl'] = kwargs.items['url']
        elif action == 'message':
            button['messageText'] = kwargs.items['text']
        elif action == 'block':
            button['messageText'] = kwargs.items['text']
            button['blockId'] = kwargs.items['block_id']
        elif action == 'phone':
            button['phoneNumber'] = kwargs.items['number']

        return button

    def card(self, title=None, description=None, image=None, buttons=None):
        BasicCard = {'basicCard': {}}

        if title is not None:
            BasicCard['basicCard']['title'] = title

        if description is not None:
            if len(description) > 230:
                raise BaseException
            BasicCard['basicCard']['description'] = description

        if image is not None:
            BasicCard['basicCard']['thumbnail'] = {'imageUrl': image, 'fixedRatio': True}

        if buttons is not None:
            if len(buttons) > 3:
                raise BaseException

            BasicCard['basicCard']['buttons'] = []
            for button in buttons:
                BasicCard['basicCard']['buttons'].append(button)

        return BasicCard

    def carousel(self, cards):
        Carousel = {'carousel': {'type': 'basicCard', 'items': []}}
        if len(cards) > 10:
            raise BaseException

        for card in cards:
            Carousel['carousel']['items'].append(card)

        return Carousel

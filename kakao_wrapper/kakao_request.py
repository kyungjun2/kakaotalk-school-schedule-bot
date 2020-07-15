# -*- coding: utf-8 -*-
class KakaoChatbotRequest:
    def __init__(self, payload):
        self.payload = payload

    def bot_info(self, detailed=False):
        # detailed가 True이면 봇의 고유 id도 제공
        if detailed:
            return (self.payload['bot']['name'], self.payload['bot']['id'],)
        else:
            return self.payload['bot']['name']

    def context(self, detailed=False):
        # detailed가 True이면 어떤 사용자의 요청인지도 제공
        if detailed:
            return (self.payload['userRequest']['block']['name'], self.payload['userRequest']['user']['id'],)
        else:
            return self.payload['userRequest']['block']['name']

    def params(self, detailed=False):
        # detailed가 True이면 사용자가 입력한 입력 원본 제공
        if detailed:
            response = []
            for (key, param) in self.payload['action']['detailParams'].items():
                response.append(({key: param['value']}, param['origin']))
            return response
        else:
            response = []
            for (key, param) in self.payload['action']['params'].items():
                response.append({key: param})
            return response

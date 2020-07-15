# -*- coding: utf-8 -*-
from __main__ import app


@app.route('/chatbot/management/list', methods=['POST'])
def management_menu_list():
    from kakao_wrapper.kakao_response import KakaoChatbotResponse as Response
    response = Response()

    response.add_output(response.text('관리 기능 목록입니다'))
    response.add_quickreply('일정 추가', '일정 추가')
    response.add_quickreply('사용자 인증', '사용자 인증')

    return response.create_response()


@app.route('/chatbot/management/authorize', methods=['POST'])
def authorize():
    from flask import request
    from kakao_wrapper.kakao_response import KakaoChatbotResponse as Response
    from kakao_wrapper.kakao_request import KakaoChatbotRequest as Request
    from database import Database
    import os

    payload = Request(request.get_json())
    response = Response()
    params = payload.params()
    db = Database()

    data = {'author': request.get_json()['userRequest']['user']['id']}
    for param in params:
        key = list(param.keys())
        data[key[0]] = param[key[0]]

    if data['auth_code'] != app.config['CHATBOT_AUTH_KEY']:
        response.add_output(response.text("인증코드가 틀렸습니다."))
    else:
        response.add_output(response.text("인증되었습니다."))
        db.add_authorize(data['author'], data['name'])

    if app.config['STRICT_AUTHENTICATION']:
        app.config['CHATBOT_AUTH_KEY'] = os.urandom(3).hex().upper()
        app.logger.info("SETTING NEW AUTH KEY : %s" % (app.config['CHATBOT_AUTH_KEY']))
    db.exit()
    return response.create_response()

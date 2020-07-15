# -*- coding: utf-8 -*-
from __main__ import app


@app.route('/chatbot/management/schedule/add', methods=['POST'])
def add_schedule():
    from flask import request
    from kakao_wrapper.kakao_response import KakaoChatbotResponse as Response
    from kakao_wrapper.kakao_request import KakaoChatbotRequest as Request
    from database import Database
    from datetime import datetime
    import json

    payload = Request(request.get_json())
    response = Response()
    params = payload.params()
    db = Database()

    data = {'author': request.get_json()['userRequest']['user']['id']}
    if not db.get_name(data['author']):
        response.add_output(response.text('인증되지 않은 사용자입니다.'))
        return response.create_response()

    for param in params:
        key = list(param.keys())
        data[key[0]] = param[key[0]]
    data['date'] = int(datetime.timestamp(datetime.fromisoformat(json.loads(data['date'])['date'])))

    response.add_output(response.text("일정 추가 요청"))
    if db.add_schedule(data):
        response.add_output(response.text("추가 성공"))
    else:
        response.add_output(response.text("추가 실패!"))

    db.exit()
    return response.create_response()


@app.route('/chatbot/management/schedule/remove')
def remove_schedule():
    # 20.06.25 TODO 일정 삭제 기능 제작
    pass

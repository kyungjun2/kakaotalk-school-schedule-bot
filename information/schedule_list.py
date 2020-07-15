# -*- coding: utf-8 -*-
from __main__ import app


@app.route('/chatbot/info/schedule/list', methods=['POST'])
def list_schedule(brief=False):
    from flask import request
    from kakao_wrapper.kakao_response import KakaoChatbotResponse as Response
    from kakao_wrapper.kakao_request import KakaoChatbotRequest as Request
    from database import Database
    from datetime import datetime

    if not brief:
        payload = Request(request.get_json())
        params = payload.params()
    response = Response()
    db = Database()
    try:
        mode = int(params[0]['mode']) if not brief else 2
        data = db.fetch_schedule(mode)

        for schedule in data:
            response.add_output(response.text("[{0}의 일정]\n \n제목 : {1}\n내용 : {2}\n\n등록자 : {3}".
                                              format(datetime.fromtimestamp(schedule[1]).strftime("%Y.%m.%d"),
                                                     schedule[2],
                                                     schedule[3],
                                                     db.get_name(schedule[0]))
                                              ))

        if len(data) == 0:
            response.add_output(response.text("일정이 없습니다."))
    except IndexError:
        response.add_output(response.text("언제의 일정을 받아올까요?\n"))
        response.add_quickreply(title="오늘", data="오늘 일정")
        response.add_quickreply(title="이번주", data="이번주 일정")
        response.add_quickreply(title="이번달", data="이번달 일정")
        # response.add_quickreply(title="지난 일정 보기", data="지난 일정")
        # 20.06.25 TODO 지나간 일정 보기 기능 제작
    db.exit()
    if not brief:
        return response.create_response()
    else:
        return response.SkillTemplate['outputs']

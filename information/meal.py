# -*- coding: utf-8 -*-
from __main__ import app


@app.route('/chatbot/info/meal', methods=['POST'])
def meal(brief=False):
    from flask import request
    from kakao_wrapper.kakao_response import KakaoChatbotResponse as Response
    from kakao_wrapper.kakao_request import KakaoChatbotRequest as Request
    from parsers.meal_parser import Parser as Meal
    import re

    if not brief:
        payload = Request(request.get_json())
        params = payload.params()
    response = Response()

    try:
        mode = int(params[0]['mode']) if not brief else 1
        try:
            for meal_data in Meal(mode):
                date = meal_data[0][4:6] + "월 " + meal_data[0][6:8] + "일"
                text = re.sub(r'(([\d]+\.)+)', '', meal_data[1])
                response.add_output(response.text(f"[{date}의 급식]\n \n{text}"))
        except KeyError:
            response.add_output(response.text("급식정보가 없습니다."))

    except IndexError:
        response.add_output(response.text("언제의 급식을 표시할까요?\n"))
        response.add_quickreply(title="오늘", data="오늘 급식")
        response.add_quickreply(title="내일", data="내일 급식")
        response.add_quickreply(title="이번주", data="이번주 급식")
    if not brief:
        return response.create_response()
    else:
        return response.SkillTemplate['outputs']

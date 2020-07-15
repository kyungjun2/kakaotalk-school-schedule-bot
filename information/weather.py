# -*- coding: utf-8 -*-
from __main__ import app


@app.route('/chatbot/info/weather', methods=['POST'])
def weather(brief=False):
    from flask import request
    from kakao_wrapper.kakao_response import KakaoChatbotResponse as Response
    from kakao_wrapper.kakao_request import KakaoChatbotRequest as Request
    from parsers.weather_parser import Parser

    if not brief:
        payload = Request(request.get_json())
        params = payload.params()
    response = Response()

    try:
        mode = int(params[0]['mode']) if not brief else 1
        try:
            weather_data = Parser(mode=mode)
            response.add_output(response.text(f"[%s의 날씨]\n \n%s" % (
                "오늘" if mode == 1 else "내일",
                f"강수확률 : {weather_data['rain_percentage']} 퍼센트 ({weather_data['rain_type']})%s" %
                ('\n\n우산을 준비하세요!' if weather_data['rain_percentage'] >= 40 else '')
            )))
        except KeyError:
            response.add_output(response.text("잠시 후 다시 시도해 주세요."))

    except IndexError:
        response.add_output(response.text("언제의 날씨를 표시할까요?\n"))
        response.add_quickreply(title="오늘", data="오늘 날씨")
        response.add_quickreply(title="내일", data="내일 날씨")
    if not brief:
        return response.create_response()
    else:
        return response.SkillTemplate['outputs']

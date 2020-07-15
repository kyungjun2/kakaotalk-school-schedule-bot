# -*- coding: utf-8 -*-
from __main__ import app


@app.route('/chatbot/info/timetable', methods=['post'])
def fetch_timetable(brief=False):
    from flask import request, abort
    from kakao_wrapper.kakao_response import KakaoChatbotResponse as Response
    from kakao_wrapper.kakao_request import KakaoChatbotRequest as Request
    from parsers.timetable_parser import Parser as Timetable

    if not brief:
        payload = Request(request.get_json())
        params = payload.params()
    response = Response()
    timetable = Timetable()

    try:
        mode = int(params[0]['mode']) if not brief else 1
        """
        mode
            - 1 : 오늘의 시간표
            - 2 : 내일의 시간표
            # - 3 : 이번주의 시간표
        """

        try:
            if mode == 1 or mode == 2:
                table = timetable.fetch_timetable(timetable.fetch_school_code("정발고등학교"), 2, 2, mode)
                if len(table) == 0:
                    raise KeyError

                result = ""

                for lecture in table:
                    result += f"{lecture[0]}교시 : {lecture[1]}\n"
                response.add_output(response.text(result))
            elif mode == 3:
                # 20.06.25 TODO 이번주 시간표 통째로 파싱
                pass
            else:
                abort(403)
        except KeyError:
            response.add_output(response.text("시간표 정보가 없습니다."))

    except IndexError:
        response.add_output(response.text("언제의 시간표를 표시할까요?\n"))
        response.add_quickreply(title="오늘", data="오늘 시간표")
        response.add_quickreply(title="내일", data="내일 시간표")
        # response.add_quickreply(title="이번주", data="이번주 시간표")
    if not brief:
        return response.create_response()
    else:
        return response.SkillTemplate['outputs']

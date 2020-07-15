# -*- coding: utf-8 -*-
from flask import Flask
import os
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

app.config['STRICT_AUTHENTICATION'] = True
app.secret_key = os.urandom(16)
app.config['CHATBOT_AUTH_KEY'] = os.urandom(3).hex().upper()
app.logger.info("SETTING NEW AUTH KEY : %s" % (app.config['CHATBOT_AUTH_KEY']))

from information import schedule_list, timetable, weather
from information import meal as meal_
from management import schedule, notification, misc

##########################################
# 이미지 생성                            #
##########################################
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
def create_image(original_text, fontsize=30, _filename='image.png',
                 colors=((122, 191, 17), (248, 250, 245)), max_char=16):
    text = ''
    img = Image.new('RGB', (400, 400), color=colors[0])

    for temp_string in original_text.split('\n'):
        for string in wrap(temp_string, max_char):
            text += (string + '\n')
        text += '\n' if len(wrap(temp_string, 16)) > 1 else ''

    d = ImageDraw.Draw(img)
    d.text(xy=(20, 20), text=text, fill=colors[1],
           font=ImageFont.truetype('/usr/share/fonts/truetype/nanum/NanumSquareR.ttf', fontsize))
    img.save('./images/' + _filename)


@app.route('/chatbot/briefing', methods=['POST'])
def briefing():
    # 20.06.25 TODO 내일 일정 브리핑도 제작
    from flask import request
    from kakao_wrapper.kakao_response import KakaoChatbotResponse as Response
    from datetime import datetime

    response = Response()
    cards = []

    ##########################################
    # 1. 일정 정보                           #
    ##########################################
    schedules = schedule_list.list_schedule(brief=True)

    for idx in range(len(schedules)):
        filename = str(datetime.now().timestamp())
        create_image(original_text=schedules[idx]['simpleText']['text'].split('등록자')[0],
                     _filename=f'{filename}.png',
                     colors=((117, 115, 28), (235, 238, 242)))
        cards.append(response.card(image=request.url_root + f'images/{filename}.png')['basicCard'])

    ##########################################
    # 2. 공지사항                            #
    ##########################################
    # 20.06.25 TODO 공지사항 브리핑

    ##########################################
    # 3. 시간표                              #
    ##########################################
    filename = str(datetime.now().timestamp())
    create_image(original_text='[시간표]\n \n' + timetable.fetch_timetable(brief=True)[0]['simpleText']['text'],
                 _filename=f'{filename}.png', fontsize=40,
                 colors=((93, 194, 166), (235, 238, 242)))
    cards.append(response.card(image=request.url_root + f'images/{filename}.png')['basicCard'])

    ##########################################
    # 4. 급식 정보                           #
    ##########################################
    filename = str(datetime.now().timestamp())
    create_image(original_text=meal_.meal(brief=True)[0]['simpleText']['text'],
                 _filename=f'{filename}.png',
                 colors=((98, 74, 194), (235, 238, 242)))
    cards.append(response.card(image=request.url_root + f'images/{filename}.png')['basicCard'])

    ##########################################
    # 5. 일기예보                            #
    ##########################################
    filename = str(datetime.now().timestamp())
    create_image(original_text=weather.weather(brief=True)[0]['simpleText']['text'],
                 _filename=f'{filename}.png', fontsize=35,
                 colors=((106, 179, 154), (235, 238, 242)))
    cards.append(response.card(image=request.url_root + f'images/{filename}.png')['basicCard'])

    response.SkillTemplate = {}
    response.add_output(response.carousel(cards))
    return response.create_response()


@app.route('/images/<path:path>')
def serve_image(path):
    from flask import send_from_directory
    return send_from_directory('images', path)


@app.before_request
def log_request_info():  # TOO MANY HACKERS :(
    from flask import request
    app.logger.info('[HTTP REQUEST FROM %s ]\n' % request.remote_addr +
                    '[Location] : %s\n' % request.url +
                    '[Body]: %s\n' % (str(request.get_data())
                                      if type(request.get_data()).__name__ == 'bytes' else request.get_data()) +
                    '[Headers]: \n%s' % request.headers)

    # 20.06.25 TODO 블랙리스트 기반 차단 제작
    return


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='10000')

# -*- coding: utf-8 -*-
"""
parsers/weather_parser.py : 일기예보를 받아오는 모듈

function Parser(nx, ny, mode) : 공공 API 이용해 기상청에서 동네예보를 받아온다.
- nx : 해당 동의 X좌표 (API 명세 참조)
- ny : 해당 동의 Y좌표 (API 명세 참조)
- mode : 받아올 날씨 (1=오늘, 2=내일)
"""


def Parser(nx=56, ny=128, mode=1):
    #  기본설정은 정발고등학교가 있는 마두동의 좌표

    #  필요한 모듈을 참조한다.
    from datetime import datetime, timedelta
    import json
    import os
    import requests

    #  발급받은 API 키를 받아온다. json 파일에 저장해둔 정보를 받아온다.
    with open(os.path.dirname(os.path.realpath(__file__)) + '/api_key.json', 'r', encoding='utf-8') as fp:
        key = json.load(fp)['WEATHER_API_KEY']

    '''
    mode (언제의 날씨를 받아올것인지 결정)
        - 1. 오늘
        - 2. 내일
    '''
    if mode == 1:
        base_date = datetime.now()
    else:
        # 20.06.25 TODO 내일의 일기예보 받아오기
        base_date = (datetime.now() + timedelta(days=1))

    #  API 명세에 맞춰 URL 제작 (REST 방식)
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?" + \
          f"serviceKey={key}&" + \
          "numOfRows=2&" + \
          "pageNo=1&" + \
          "dataType=JSON&" + \
          f"nx={nx}&ny={ny}&" + \
          f"base_date={((base_date - timedelta(days=1)) if base_date.hour < 2 else base_date).strftime('%Y%m%d')}&" + \
          f"base_time=%d00" % (23 if base_date.hour < 2 else (lambda x: x - (x - 2) % 3)(base_date.hour))

    #  JSON 형식으로 요청 후 파싱
    data = json.loads(requests.get(url).text)
    return_data = {'rain_percentage': 0, 'rain_type': '맑음'}

    #  자료는 response/body/items/item 안에 list 형식으로 있다. 리스트의 각 원소를 돌면서 키를 확인한다.
    for info in data['response']['body']['items']['item']:
        if info['category'] == 'POP':  # 강수확률
            return_data['rain_percentage'] = int(info['fcstValue'])
        elif info['category'] == 'PTY':  # 강수형태 (0 없음, 1 비, 2 진눈깨비, 3 눈, 4 소나기)
            if int(info['fcstValue']) == 1:
                return_data['rain_type'] = '비'
            elif int(info['fcstValue']) == 2:
                return_data['rain_type'] = '눈'
            elif int(info['fcstValue']) == 3:
                return_data['rain_type'] = '진눈깨비'
            elif int(info['fcstValue']) == 4:
                return_data['rain_type'] = '소나기'

    #  응답을 dictionary 형식으로 반환한다.
    return return_data

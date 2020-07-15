# -*- coding: utf-8 -*-
def Parser(mode=1):
    from datetime import date, timedelta
    import json
    import os
    import requests

    """
    mode : 몇일의 급식 정보를 받아올건지
    - 1: 오늘만
    - 2: 내일 급식
    - 3: 이번주 급식
    """

    if mode == 1:
        MLSV_YMD = date.today().strftime('%Y%m%d')
    elif mode == 3:
        MLSV_FROM_YMD = date.today().strftime('%Y%m%d')
        MLSV_TO_YMD = (date.today() + timedelta(days=7)).strftime("%Y%m%d")
    elif mode == 2:
        MLSV_YMD = (date.today() + timedelta(days=1)).strftime('%Y%m%d')
    else:
        return False

    with open(os.path.dirname(os.path.realpath(__file__)) + '/api_key.json', 'r', encoding='utf-8') as fp:
        key = json.load(fp)['NEIS_API_KEY']

    ATPT_OFCDC_SC_CODE = "J10"
    SD_SCHUL_CODE = "7530119"
    url = f"""https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}&Type=json&""" + \
          f"""ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}&SD_SCHUL_CODE={SD_SCHUL_CODE}&""" + \
          (f"""MLSV_YMD={MLSV_YMD}""" if mode == 1 or mode == 2 else
           f"""MLSV_FROM_YMD={MLSV_FROM_YMD}&MLSV_TO_YMD={MLSV_TO_YMD}""")

    r = requests.get(url)
    meal_data = []
    for meal in json.loads(r.text)['mealServiceDietInfo'][1]['row']:
        meal_data.append((meal['MLSV_YMD'], meal['DDISH_NM'].replace('<br/>', '\n'),))

    return meal_data

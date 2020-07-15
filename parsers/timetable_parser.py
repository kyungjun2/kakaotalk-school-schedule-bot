# -*- coding: utf-8 -*-


class Parser:
    def __init__(self):
        import re
        import requests

        r = requests.get('http://112.186.146.81:4082/st')
        r.encoding = 'euc-kr'
        self.url_prefix = re.compile(r"""url:[^\d]+([\d]+\?[\d]+l)""").findall(r.text)[0]

        self.timetable_prefix = re.compile(r"""sc_data\('([\d]+)""").findall(r.text)[0]
        self.timetable_key = re.compile(r"자료=자료\.(자료[\d]+)").findall(r.text)

    def fetch_school_code(self, school_name, region="경기"):
        import requests
        import json
        from urllib.parse import quote

        url = quote(school_name, encoding="euc-kr")
        data = requests.get("http://112.186.146.81:4082/" + self.url_prefix + url)
        data.encoding = 'utf-8'
        data = json.loads(data.text.split('\x00')[0])

        for school in data["학교검색"]:
            if school[1] == region and school[2] == school_name:
                return school[3]

    def fetch_timetable(self, school_code, grade_no, class_no, date=1):
        import requests
        import json
        import base64
        from datetime import datetime, timedelta

        """
        date : 몇일 후의 시간표 정보?
        """

        date = (datetime.today() + timedelta(days=date - 1)).weekday() + 1

        url = "http://112.186.146.81:4082/" + self.url_prefix.split('?')[0] + "?" + \
              base64.b64encode(f"{self.timetable_prefix}_{school_code}_0_1".encode('utf-8')).decode('utf-8')
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = json.loads(data.text.split('\x00')[0])

        for key in data.keys():
            if key.startswith('긴자료'):
                subject_key = key
        timetable_key = self.timetable_key[data['오늘r'] - 1]

        try:
            timetable = []
            idx = 0
            for lecture in data[timetable_key][grade_no][class_no][date][1:data['요일별시수'][grade_no][date] + 1]:
                lecture = str(lecture)
                idx += 1

                timetable.append((idx, data[subject_key][int(lecture[-2:])],))

        except IndexError:
            timetable = []

        return timetable

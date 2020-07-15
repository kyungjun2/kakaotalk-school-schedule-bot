# -*- coding: utf-8 -*-
import sqlite3


class Database:
    def __init__(self):
        import os
        # 데이터베이스 호출
        self.conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "/database.db")
        self.cursor = self.conn.cursor()

        # 스키마 정의
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `schedule` "
                            "(author TEXT, date INT, title TEXT, description TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `notice` "
                            "(author TEXT, date INT, title TEXT, description TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `authorized` "
                            "(id TEXT UNIQUE, name TEXT UNIQUE)")
        return

    def exit(self):
        self.cursor.close()
        self.conn.close()
        return

    def add_schedule(self, data):
        """
        data (dict)
            {
                'author': 작성자 (str),
                'date': 등록일자 (int, Timestamp),
                'title': 제목 (str),
                'description': 내용 (str)
            }
        """
        try:
            self.cursor.execute("INSERT INTO `SCHEDULE` (`author`, `date`, `title`, `description`) VALUES (?, ?, ?, ?)",
                                (data['author'], data['date'], data['title'], data['description'],))
            self.conn.commit()
            return True

        except sqlite3.Error as e:
            print(e)
            return False

    def fetch_schedule(self, mode=2):
        """
        mode (int) : 언제까지의 일정을 받아올건지
            1: 일주일 이내의 일정을 받아옴
            2: 오늘 일정을 받아옴
            3: 4주 이내의 일정을 받아옴
        """
        from datetime import datetime, timedelta
        today = int(datetime.timestamp(datetime.combine(datetime.now().date(), datetime.min.time())))

        # 타임스탬프 제작
        if mode == 1:
            date = (today, int(datetime.timestamp(datetime.fromtimestamp(today) + timedelta(days=7)),))
        elif mode == 2:
            date = (today, today,)
        elif mode == 3:
            date = (today, int(datetime.timestamp(datetime.fromtimestamp(today) + timedelta(weeks=4)),))
        else:
            return False

        # 쿼리 실행
        try:
            return_data = []
            self.cursor.execute("SELECT * FROM `schedule` WHERE `date` >= ? and `date` <= ? ORDER BY `date` ASC",
                                date)

            row = self.cursor.fetchall()
            for data in row:
                return_data.append(data)
            return return_data

        except sqlite3.Error as e:
            print(e)
            return False

    def get_name(self, unique_id):
        """
        unique_id (str) : 카카오 챗봇에서 생성한 고유ID
        """
        try:
            self.cursor.execute("SELECT `name` FROM `authorized` WHERE `id` = ?", (unique_id,))
            row = self.cursor.fetchone()
            return row[0]

        except sqlite3.Error as e:  # DB 오류
            print(e)
            return False
        except TypeError:  # 일치하는 데이터 없음
            return False

    def add_authorize(self, unique_id, name):
        """
        unique_id (str) : 카카오 챗봇에서 생성한 고유ID
        name (str) : 사용자 이름
        """
        try:
            self.cursor.execute("INSERT INTO `authorized` (`id`, `name`) VALUES (?, ?)", (unique_id, name))
            self.conn.commit()

        except sqlite3.Error as e:
            print(e)
            return False

#: 여기저기서 자꾸쓰는 함수 모음집
from datetime import datetime

def convert_datetime_4mysql(basedate):
    """
    client에서 보내주는 datetime이 MySQL 포맷에 맞지 않기 때문에 포맷형식을 바꿔주는 함수입니다
    """
    formatfrom = "%a, %d %b %Y %H:%M:%S GMT"
    formatto = "%Y-%m-%d %H:%M:%S:00"
    convertdate = datetime.strptime(basedate, formatfrom).strftime(formatto)
    return convertdate

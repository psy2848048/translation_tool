#: 여기저기서 자꾸쓰는 함수 모음집
from app import app
from datetime import datetime
import hashlib
import string
import random
import traceback
import requests
import re
import io

import boto3
S3 = boto3.client(
        's3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
        # aws_session_token=SESSION_TOKEN,
    )
BUCKET_NAME = 'marocat'


def convert_datetime_4mysql(basedate):
    """
    client에서 보내주는 datetime이 MySQL 포맷에 맞지 않기 때문에 포맷형식을 바꿔주는 함수입니다
    """
    formatfrom = "%a, %d %b %Y %H:%M:%S GMT"
    formatto = "%Y-%m-%d %H:%M:%S:00"
    convertdate = datetime.strptime(basedate, formatfrom).strftime(formatto)
    return convertdate


def encrypt_pwd(password):
    """
    비밀번호 암호화하기
    """
    m = hashlib.sha512()
    m.update(password.encode('utf-8'))
    hashpwd = m.hexdigest()
    return hashpwd


def create_token(sth, size=13):
    """
    토큰 만들기
    sth과 현재시간(UTC)을 가지고 해싱하여 토큰을 만든다.

    :param sth: 이 함수를 사용하는 어딘가에서 쓰이는 아무 변수
    :param len: 원하는 토큰의 길이
    :return:
    """
    m = hashlib.sha1()

    t1 = sth + str(datetime.utcnow())
    m.update(t1.encode('utf-8'))
    t2 = m.hexdigest()
    t3 = t2 + string.ascii_uppercase

    token = ''.join(random.choice(t3) for _ in range(size))
    return token


def send_mail(mail_to, title, content, mail_from='no-reply@ciceron.me', name='CICERON', password='ciceron3388!'):
    """
    :param mail_to: 받는 사람
    :param title: 이메일 제목
    :param content: 이메일 내용
    :param mail_from: 보내는 사람
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    try:
        content = MIMEText(content, 'html', _charset='utf-8')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = '{} team <{}>'.format(name, mail_from)
        msg['To'] = str(mail_to)
        msg.attach(content)

        a = smtplib.SMTP('smtp.gmail.com:587')
        a.ehlo()
        a.starttls()
        a.login(mail_from, password)
        a.sendmail('no-reply@ciceron.me', str(mail_to), msg.as_string())
        a.quit()
        return True
    except:
        traceback.print_exc()
        return False


def upload_photo_to_bytes_on_s3(picture, mimetype, name):
    """
    S3에 Bytes로 사진 저장하기
    :param picture: 사진, bytes
    :param mimetype:
    :param name:
    :return: S3에 저장한 이름과 URL + 성공유무
    """
    try:
        t = create_token(name)
        pname = 'profile/' + str(datetime.utcnow().strftime('%Y%m%d%H%M%S')) + t + '.' + mimetype

        S3.upload_fileobj(io.BytesIO(picture), BUCKET_NAME, pname)

        purl = S3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': pname
            }
        )

        return pname, purl, True
    except:
        print('Wrong! (S3 upload_fileobj)')
        traceback.print_exc()
        return None, None, False


# def ddos_check_and_write_log(conn):
#     """
#     API 실행 전, 해당 IP에서 1초에 100번 이상 실행되면 30분동안 접속 차단한다.
#     그리고 차단하지 않은 IP는 임시 테이블에 로그를 남겨 나중에 분석 자료로 이용한다.
#
#     * 추후 변경 사항
#     """
#     cursor = conn.cursor()
#
#     if session.get('useremail') != None:
#         user_id = get_user_id(conn, session['useremail'])
#     else:
#         user_id = 0
#
#     method = request.method
#     api_endpoint = request.environ['PATH_INFO']
#     ip_address = request.headers.get('x-forwarded-for-client-ip')
#
#     query_apiCount = """
#         SELECT count(*) FROM CICERON.TEMP_ACTIONS_LOG
#           WHERE (user_id = %s OR ip_address = %s)
#             AND log_time BETWEEN (CURRENT_TIMESTAMP - interval '1 seconds') AND CURRENT_TIMESTAMP"""
#     cursor.execute(query_apiCount, (user_id, ip_address, ))
#     conn_count = cursor.fetchone()[0]
#
#     query_getBlacklist = """
#         SELECT count(*) FROM CICERON.BLACKLIST
#           WHERE user_id = %s
#             AND CURRENT_TIMESTAMP BETWEEN time_from AND time_to
#     """
#     cursor.execute(query_getBlacklist, (user_id, ))
#     blacklist_count = cursor.fetchone()[0]
#
#     is_OK = True
#     if conn_count > 100:
#         session.pop('logged_in', None)
#         session.pop('useremail', None)
#         query_insertBlackList = """
#             INSERT INTO CICERON.BLACKLIST (id, user_id, ip_address, time_from, time_to)
#             VALUES
#             (
#                nextval('CICERON.SEQ_BLACKLIST')
#               ,%s
#               ,%s
#               ,CURRENT_TIMESTAMP
#               ,CURRENT_TIMESTAMP + interval('30 minutes')
#             )
#         """
#         cursor.execute(query_insertBlackList, (user_id, ip_address, ))
#         is_OK = False
#
#     if blacklist_count > 0:
#         session.pop('logged_in', None)
#         session.pop('useremail', None)
#         is_OK = False
#
#     query_insertLog = """
#         INSERT INTO CICERON.TEMP_ACTIONS_LOG
#           (id, user_id, method, api, log_time, ip_address)
#         VALUES
#           (
#              nextval('CICERON.SEQ_USER_ACTIONS')
#             ,%s
#             ,%s
#             ,%s
#             ,CURRENT_TIMESTAMP
#             ,%s
#           )
#     """
#     cursor.execute(query_insertLog, (user_id, method, api_endpoint, ip_address, ))
#     conn.commit()
#
#     return is_OK

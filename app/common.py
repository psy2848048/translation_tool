#: 여기저기서 자꾸쓰는 함수 모음집
from datetime import datetime
import hashlib
import string
import random
import traceback


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

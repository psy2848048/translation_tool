import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import traceback
from pprint import pprint

#: 기본
LOGIN_EMAIL = 'no-reply@ciceron.me'
LOGIN_PASSWORD = 'ciceron3388!'

#: Baogao
# LOGIN_EMAIL = 'baogao@baogao.co'
# LOGIN_PASSWORD = 'baogao7777!'


def send_mail_using_template(info, content):
    """
    기본이 되는 함수입니다.
    
    :param info: 
        mail_info = {
            'mail_from': email,
            'mail_to': ['sunny@ciceron.me'],
            'subject': '이메일 제목',
            'which_mail': '보낼 html 파일 이름'
        }
        :mail_from: 보내는 사람
        :mail_to: 받는 사람. 여러명이 받는 경우를 위해 배열로 받습니다. ex) ['chingoo@ciceron.me', 'betty@ciceron.me']
        :subject: 이메일 제목
        :which_mail: 어떤 메일을 보내는가
        
    :param content: which_mail에 따라서 내용이 달라집니다.
    """
    try:
        msg = MIMEMultipart()

        msg['From'] = info['mail_from']
        msg['Subject'] = info['subject']

        #: 받는 사람
        if type(info['mail_to']) != list:
            msg['To'] = info['mail_to']
        else:
            msg['To'] = ', '.join(info['mail_to'])

        #: 메일 내용 채우기
        with open('app/mail/templates/{}.html'.format(info['which_mail']), 'r') as f:
            html = f.read().format(**content)
        content = MIMEText(html, 'html', _charset='utf-8')
        msg.attach(content)

        # print(msg)

        #: 첨부파일 붙이기
        filename = content['filename']
        filebin = content['filebin']
        if not None in [filename, filebin]:
            attachment = MIMEApplication(filebin, Name=filename)
            attachment['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            msg.attach(attachment)

        #: 메일 전송
        a = smtplib.SMTP('smtp.gmail.com:587')
        a.ehlo()
        a.starttls()
        a.login(LOGIN_EMAIL, LOGIN_PASSWORD)
        a.sendmail(info['mail_from'], info['mail_to'], msg.as_string())
        a.quit()

        return True
    except:
        traceback.print_exc()
        return False


def send_mail_directly(mail_from, mail_to, subject, content, team_name='CICERON'):
    """
    :param mail_from: 보내는 사람
    :param mail_to: 받는 사람
    :param subject: 메일 제목
    :param content: 메일 내용
    :param team_name: 팀 이름
    """
    try:
        msg = MIMEMultipart('alternative')

        msg['From'] = '{} team <{}>'.format(team_name, mail_from)
        # msg['To'] = mail_to
        #: 받는 사람
        if type(mail_to) != list:
            msg['To'] = mail_to
        else:
            msg['To'] = ', '.join(mail_to)

        msg['Subject'] = subject

        msg_content = MIMEText(content, 'html', _charset='utf-8')
        msg.attach(msg_content)

        # print(msg)

        a = smtplib.SMTP('smtp.gmail.com:587')
        a.ehlo()
        a.starttls()
        a.login(LOGIN_EMAIL, LOGIN_PASSWORD)
        a.sendmail(mail_from, mail_to, msg.as_string())
        a.quit()

        return True
    except:
        traceback.print_exc()
        return False

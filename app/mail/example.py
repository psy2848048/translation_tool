# 예시입니다. 복붙해서 데이터부분만 잘 바꿔쓰면 될듯해여!
import app.mail as mail


"""
# request_sent_confirm.html
content = {
    'main_text': '',
    'sub_text': '',
    'mail_text': '',
    'email': '',
    'name': '',
    'message': '',
    'original_language': '',
    'target_language': '',
    'deadline_date': None,
    'text_counter': 322,
    'coupon': None,
    'filename': None,
    'filebin': None
}
"""
def send_request_sent_confirm_mail(email, client_name, ol, tl, str_cnt):
    """
    request_sent_confirm.html 사용할 때
    아래 예시는 스팀잇에서 사용된 것입니다.
    """
    admin = {
        'mail_from': email,
        'mail_to': ['sunny@ciceron.me'],  # 스팀잇 담당자
        'subject': '스팀잇에서 의뢰가 들어왔습니다.',
        'which_mail': 'request_sent_confirm'
    }
    client = {
        'mail_from': 'no-reply@ciceron.me',
        'mail_to': [email],
        'subject': '의뢰 접수 안내/Confirmation of the request',
        'which_mail': 'request_sent_confirm'
    }
    admin_data = {
        'main_text': '의뢰가 들어왔습니다.',
        'sub_text': '확인 후 가격을 지정해주세요.',
        'mail_text': '의뢰가 완료되었습니다. 가격을 지정해주세요.'
    }
    client_data = {
        'main_text': '의뢰가 성공적으로 접수되었습니다.',
        'sub_text': '입금이 완료되면 번역이 진행됩니다. 감사합니다.',
        'mail_text': '의뢰 접수가 완료되었습니다. 결제를 완료해주세요. 감사합니다.'
    }
    common_data = {
        'email': email,
        'name': client_name,
        'message': '스팀잇 만들면서 메일 모듈 정리중입니다.',
        'original_language': ol,
        'target_language': tl,
        'deadline_date': None,
        'text_counter': str_cnt,
        'coupon': None,
        'filename': None,
        'filebin': None
    }

    #: 씨세론 담당자에게 이메일 보내기
    is_done = mail.send_mail(admin, admin_data.update(common_data))
    if is_done is False:
        return False

    #: 고객에게 이메일 보내기
    is_done = mail.send_mail(client, client_data.update(common_data))
    if is_done is False:
        return False
    return True

var pageScript = function () {
    var local = this,
        type = getUrlParameter('type');
    this.preEvents = function () {
        local.social_text();
    };
    this.clickEvents = function(){
        $('.add').on('click', function(e){
            e.preventDefault();
            local.check_form();
        });
    };
    this.check_form = function(){
        var email = $('#email'),
        pass = $('#pass'),
        pass_confirm = $('#pass_confirm'),
        nick = $('#nick'),
        social_type = type;
        
        // 공백
        if(email.val().trim() == ''){
            alert('이메일을 입력해주세요');
            email.focus();
            return false;
        }
        if(pass.val().trim() == ''){
            alert('비밀번호를 입력해주세요');
            pass.focus();
            return false;
        }
        if(pass_confirm.val().trim() == ''){
            alert('비밀번호 확인을 입력해주세요');
            pass_confirm.focus();
            return false;
        }
        if(nick.val().trim() == ''){
            alert('이름(닉네임)을 입력해주세요');
            nick.focus();
            return false;
        }

        // 글자수 체크
        if(pass.val().trim().length < 4){
            alert('비밀번호는 4자이상 입니다.');
            pass.focus();
            return false;
        }
        if(nick.val().trim().length < 2){
            alert('이름(닉네임)은 2자이상 입니다.');
            nick.focus();
            return false;
        }

        // 비밀번호 일치 체크
        if(pass.val().trim() != pass_confirm.val().trim()){
            alert('비밀번호가 일치하지 않습니다');
            pass.focus();
            return false;
        }

        // 이메일 정규식
        if(!CheckEmail){
            alert('이메일 형식이 올바르지 않습니다');
            email.focus();
            return false;
        }

        // 동의
        if(!$('#chk_agree').prop('checked')){
            alert('이용약관에 동의 해주세요');
            $('#chk_agree').focus();
            return false;
        }
        if(!$('#chk_policy').prop('checked')){
            alert('개인정보 보호정책에 동의 해주세요');
            $('#chk_policy').focus();
            return false;
        }
    };
    this.social_text = function () {
        if (type != undefined && type.trim() != '') {
            $('#con_social').html('');
            $(type.split(',')).each(function (idx, res) {
                if (res.trim() == 'g') $('#con_social').append('구글');
                else if (res.trim() == 'f') $('#con_social').append('페이스북');

                if (type.split(',').length != parseInt(idx) + 1) $('#con_social').append(', ');
            });
        }
    };
    this.bind = function () {
        local.preEvents();
        local.clickEvents();
    };
};
$(function () {
    var script = new pageScript();
    script.bind();
});
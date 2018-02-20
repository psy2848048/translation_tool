var pageScript = function () {
    var local = this;
    this.loginCheck = function () {
        setTimeout(function () {
            if (IsValidStr(_USER_ID)) {
                alert('로그온 상태입니다.');
                location.href = '/static/front/project/projects.html';
            }
        }, 500);
    };
    this.mask = function () {
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        $('#mask').css({
            'width': maskWidth,
            'height': maskHeight
        }).show();
    };
    this.clickEvent = function () {
        // 비밀번호 찾기 버튼 클릭하면
        // 해당 이메일의 비밀번호를 새로운 암호화된 비밀번호로 변경한 후
        // 서버에서 기재한 이메일로 복호화 된 암호를 보내준다.
        $('#new_pass_btn').on('click', function (e) {
            e.preventDefault();
            var email = $('#txt_id').val().trim();
            if (!IsValidStr(email)) {
                alert('이메일을 입력해주세요');
                $('#txt_id').focus();
                return false;
            }

            // 이메일 정규식
            if (!CheckEmail(email)) {
                alert('이메일 형식이 올바르지 않습니다');
                $('#txt_id').focus();
                return false;
            }

            $('#desc2').text('화면이 잠시 멈춰도 새로운 비밀번호를 만들고 이메일을 보내는 과정 중이니 조금만 기다려주세요!');

            //local.mask();
            $('#dvLoading').show();
            setTimeout(function () {
                var result = AjaxExecute('/api/v1/auth/recoverPwd', 'POST', {
                    email: email
                });

                if (IsValidStr(result.result_ko)) {
                    alert(result.result_ko);
                } else {
                    //$('#mask').fadeOut('slow');
                    $('#dvLoading').fadeOut('slow');
                    alert(result);
                }

                if (result.result == 200) location.href = '/static/front/user/login.html';
            }, 500);
        });
    };
    this.bind = function () {
        local.loginCheck();
        local.clickEvent();
    };
};
$(function () {
    var script = new pageScript();
    script.bind();
});
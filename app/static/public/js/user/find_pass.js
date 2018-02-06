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
    this.clickEvent = function () {
        // 비밀번호 찾기 버튼 클릭하면
        // 해당 이메일의 비밀번호를 새로운 암호화된 비밀번호로 변경한 후
        // 서버에서 기재한 이메일로 복호화 된 암호를 보내준다.
        $('#new_pass_btn').on('click', function (e) {
            e.preventDefault();
            var email = $('#txt_id').val().trim();
            if(!IsValidStr(email)){
                alert('이메일을 입력해주세요');
                $('#txt_id').focus();
                return false;
            }
            var url = '비밀번호찾기api_url';
            var data = {
                비밀번호찾기api_data:email
            };
            console.log('######### 8596 ###########');
            console.log(data);

            var result = AjaxExecute(url, 'POST', data);
            console.log('=== result ===');
            console.log(result);
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
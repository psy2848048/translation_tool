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
        //$('#loginBtn').on('click', function(){
        //    if($('#txt_id').val() == 'ciceron' && $('#txt_pass').val() == 'ciceron8888') location.href='/static/front/project/projects.html';
        //    else alert('로그인정보가 일치하지 않습니다');
        //});
        $('#loginBtn').on('click', function () {
            var data = {
                email: $('#txt_id').val().trim(),
                password: $('#txt_pass').val().trim()
            };
            var url = '/api/v1/auth/local/signin';

            console.log('######### 8596 ###########');
            console.log(data);

            $.ajax({
                url: url,
                data: data,
                type: 'POST',
                async: true,
                success: function (res) {
                    alert(res.result_ko);
                    if (res.result == 200) {
                        location.href = '/static/front/project/projects.html';
                    } else console.log(res);
                },
                error: function (e) {
                    //alert(e.responseJSON.result_ko);
                    console.log('[fail : 1658]');
                    console.log(e);
                }
            });
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
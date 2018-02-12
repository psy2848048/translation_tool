$('#hd_social_result').val(getUrlParameter('result') == undefined ? '' : getUrlParameter('result').ReplaceAll('+',' '));
$('#hd_social_result_ko').val(getUrlParameter('result') == undefined ? '' : getUrlParameter('result_ko').ReplaceAll('+',' '));
$('#hd_social_result_en').val(getUrlParameter('result') == undefined ? '' : getUrlParameter('result_en').ReplaceAll('+',' '));
if($('#hd_social_result_ko').val().trim() != ''){
    alert($('#hd_social_result_ko').val().trim());
}

var pageScript = function () {
    var local = this;
    this.loginCheck = function () {
        setTimeout(function () {
            if (IsValidStr(_USER_ID)) {
                alert('로그온 상태입니다.');
                location.href = '/static/front/project/projects.html';
            } 
            // else {
            //     $('#hd_social_result').val(getUrlParameter('result'));
            //     $('#hd_social_result_ko').val(getUrlParameter('result_ko'));
            //     $('#hd_social_result_en').val(getUrlParameter('result_en'));
            // }
        }, 500);
    };
    this.preInit = function () {
        $('#hd_msg').val(getUrlParameter('results'));
        setTimeout(function () {
            if ($('#hd_social_result_ko').val() != '') $('#p_msg').css({
                'color': 'red'
            }).text($('#hd_social_result_ko').val());
        }, 200);
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
                    alert(e.responseJSON.result_ko);
                    console.log('[fail : 1658]');
                    console.log(e);
                }
            });
        });
    };
    this.bind = function () {
        local.loginCheck();
        local.preInit();
        local.clickEvent();
    };
};
$(function () {
    var script = new pageScript();
    script.bind();
});
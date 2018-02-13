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
    this.preEvent = function () {
        //var ver = getUrlParameter('ver');
        //var lang = getUrlParameter('lang');
        //if(ver != undefined && ver.trim() != '') $('#selVersion').val(ver);
        //if(lang != undefined && lang.trim() != '') $('#selLang').val(lang);
        if ($('#hd_msg').val() != '{{result_ko}}') $('#p_msg').css({'color': 'red'}).text($('#hd_msg').val());          
    };
    this.clickEvents = function () {
        $('#googleLink').on('click', function () {
            var url = '/api/v1/auth/google/signin';
            $.ajax({
                url: url,
                type: 'GET',
                //data: data,
                async: true,
                success: function (res) {
                    //console.log('##### res #####');
                    //console.log(res);
                },
                error: function (err) {
                    //console.log('##### err #####');
                    //console.log(err);
                }
            });
        });
        $('#facebookLink').on('click', function () {
            var url = '/api/v1/auth/facebook/signin';
            $.ajax({
                url: url,
                type: 'GET',
                //data: data,
                async: true,
                success: function (res) {
                    //console.log('##### res #####');
                    //console.log(res);
                },
                error: function (err) {
                    //console.log('##### err #####');
                    //console.log(err);
                }
            });
        });
    };
    this.bind = function () {
        local.loginCheck();
        local.preEvent();
        local.clickEvents();
    };
};
$(function () {
    var script = new pageScript();
    script.bind();
});
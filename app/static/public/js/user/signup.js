$('#hd_nick').val(getUrlParameter('name') == undefined ? '' : getUrlParameter('name'));
$('#hd_email').val(getUrlParameter('email') == undefined ? '' : getUrlParameter('email'));
$('#hd_social_id').val(getUrlParameter('social_id') == undefined ? '' : getUrlParameter('social_id'));
$('#hd_picture').val(getUrlParameter('picture') == undefined ? '' : getUrlParameter('picture'));
$('#hd_type').val(getUrlParameter('signup_type') == undefined ? '' : getUrlParameter('signup_type'));

var pageScript = function () {
    var local = this;
    //type = getUrlParameter('type');
    this.loginCheck = function () {
        setTimeout(function () {
            if (IsValidStr(_USER_ID)) {
                alert('로그온 상태입니다.');
                location.href = '/static/front/project/projects.html';
            }
        }, 500);        
        // setTimeout(function () {
        //     if ($('#hd_nick').val() == '{{name}}') $('#hd_nick').val('');
        //     if ($('#hd_email').val() == '{{email}}') $('#hd_email').val('');
        //     if ($('#hd_social_id').val() == '{{social_id}}') $('#hd_social_id').val('');
        //     if ($('#hd_picture').val() == '{{picture}}') $('#hd_picture').val('');
        //     if ($('#hd_type').val() == '{{signup_type}}') $('#hd_type').val('local');
        // }, 1000);
    };
    this.preEvents = function () {        
        local.social_init();      
    };
    this.clickEvents = function () {
        $('.add').on('click', function (e) {
            e.preventDefault();
            local.check_form();
        });
    };
    this.mask = function () {
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        $('#mask').css({'width': maskWidth,'height': maskHeight}).show();
    };
    this.check_form = function () {
        var email = $('#email'),
            pass = $('#pass'),
            pass_confirm = $('#pass_confirm'),
            nick = $('#nick');

        // 공백        
        if (nick.val().trim() == '') {
            alert('닉네임을 입력해주세요');
            nick.focus();
            return false;
        }
        if (email.val().trim() == '') {
            alert('이메일을 입력해주세요');
            email.focus();
            return false;
        }
        if (pass.val().trim() == '') {
            alert('비밀번호를 입력해주세요');
            pass.focus();
            return false;
        }
        if (pass_confirm.val().trim() == '') {
            alert('비밀번호 확인을 입력해주세요');
            pass_confirm.focus();
            return false;
        }
        // 글자수 체크
        if (nick.val().trim().length < 2) {
            alert('닉네임은 2자이상 입니다.');
            nick.focus();
            return false;
        }
        if (pass.val().trim().length < 4) {
            alert('비밀번호는 4자이상 입니다.');
            pass.focus();
            return false;
        }

        // 비밀번호 일치 체크
        if (pass.val().trim() != pass_confirm.val().trim()) {
            alert('비밀번호가 일치하지 않습니다');
            pass.focus();
            return false;
        }

        // 이메일 정규식
        if (!CheckEmail($('#email').val())) {
            alert('이메일 형식이 올바르지 않습니다');
            email.focus();
            return false;
        }

        // 동의
        if (!$('#chk_agree').prop('checked')) {
            alert('이용약관에 동의 해주세요');
            $('#chk_agree').focus();
            return false;
        }
        if (!$('#chk_policy').prop('checked')) {
            alert('개인정보 보호정책에 동의 해주세요');
            $('#chk_policy').focus();
            return false;
        }

        var data = {
            email: email.val().trim(),
            password: pass.val().trim(),
            nickname: nick.val().trim(),
            social_id: $('#hd_social_id').val().trim(),
            picture: $('#hd_picture').val().trim()
        };

        console.log('######### 4596 ###########');
        console.log(data);
 
        local.mask();
        $('#dvLoading').show();

        $.ajax({
            url: '/api/v1/auth/signup/' + $('#hd_type').val(),
            data: data,
            type: 'POST',
            async: true,
            success: function (res) {
                alert(res.result_ko);
                if (res.result == 200) {
                    location.href = '/static/front/user/login.html';
                } else console.log(res);
            },
            error: function (e) {
                $('#mask').hide();
                $('#dvLoading').hide();
                alert(e.responseJSON.result_ko);
                console.log('[fail : 1658]');
                console.log(e.responseJSON.result + ' : ' + e.responseJSON.result_ko);
            }
        });
    };
    this.social_init = function () {
        if ($('#hd_social_id').val() != '') {
            $('#nick').val($('#hd_nick').val());
            $('#email').val($('#hd_email').val());
        }
    };
    // this.social_text = function () {
    //     if (type != undefined && type.trim() != '') {
    //         $('#con_social').html('');
    //         $(type.split(',')).each(function (idx, res) {
    //             if (res.trim() == 'g') $('#con_social').append('구글');
    //             else if (res.trim() == 'f') $('#con_social').append('페이스북');

    //             if (type.split(',').length != parseInt(idx) + 1) $('#con_social').append(', ');
    //         });
    //     }
    // };
    this.bind = function () {
        local.loginCheck();
        local.preEvents();
        local.clickEvents();
    };
};
$(function () {
    var script = new pageScript();
    script.bind();
});
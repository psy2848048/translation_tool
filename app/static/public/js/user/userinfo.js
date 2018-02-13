$('#hd_social_result').val(getUrlParameter('result') == undefined ? '' : getUrlParameter('result').ReplaceAll('+',' '));
$('#hd_social_result_ko').val(getUrlParameter('result_ko') == undefined ? '' : getUrlParameter('result_ko').ReplaceAll('+',' '));
$('#hd_social_result_en').val(getUrlParameter('result_en') == undefined ? '' : getUrlParameter('result_en').ReplaceAll('+',' '));
if($('#hd_social_result_ko').val().trim() != ''){
    alert($('#hd_social_result_ko').val().trim());
}

var pageScript = function () {
    var local = this,
        userinfo = '';
    this.preInit = function () {
        local.memberInfo();
        // setTimeout(function () {
        //     if ($('#hd_msg').val() != '') alert($('#hd_msg').val());
        // }, 200);
    };
    this.selectEvent = function () {};
    this.mask = function () {
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        $('#mask').css({
            'width': maskWidth,
            'height': maskHeight
        }).show();
    };
    this.btnClickEvents = function () {
        // 사진변경 버튼
        $('#picture_btn').on('click', function (e) {
            e.preventDefault();

            local.mask();
            $('#dvLoading').show();

            var reg_ext = ['JPG', 'JPEG', 'GIF', 'PNG'];
            var msg = 'JPG, JPEG, GIF, PNG 이미지 파일 확장자만 허용합니다.';
            var fileUpload = $('#file_frm').get(0);
            var files = fileUpload.files;
            var f_data = new FormData();
            var is_allowed_ext = false;
            for (var i = 0; i < files.length; i++) {
                /* 사이즈 체크 */
                var fileSize = files[i].size;
                var mega = 10; // 메가 : 서버에는 썸네일 방식으로 떨구기러 함(가로세로 30px 정도가 적당)
                var maxFilesize = parseInt(mega) * 1025 * 1000;
                if (fileSize > maxFilesize) {
                    $('#mask').fadeOut('slow');
                    $('#dvLoading').fadeOut('slow');

                    alert('파일당 최대용량은 ' + mega + '메가 입니다.');
                    //$('#file_frm').val('');
                    location.href = location.href;
                    return false;
                }
                /* 확장자 체크 */
                var ext = getFileExtension(files[i].name);
                if (ext == '') alert('파일 확장자에 문제가 있습니다!');
                else {
                    for (var j = 0; j < reg_ext.length; j++) {
                        if (reg_ext[j].toUpperCase() == ext) {
                            is_allowed_ext = true;
                            continue;
                        }
                    }
                }
                f_data.append('picture', files[i]);
            }
            if (is_allowed_ext) {
                local.mask();
                $('#dvLoading').show();

                $.ajax({
                    url: '/api/v1/users/me/picture',
                    type: "PUT",
                    contentType: false,
                    processData: false,
                    data: f_data,
                    success: function (res) {
                        alert(res.result_ko);
                        location.href = '/static/front/user/userinfo.html';
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        if (IsValidStr(xhr.responseText.result_ko)) alert(xhr.responseText.result_ko);
                        else alert('error code : ' + xhr.status);
                    }
                });

                $('#mask').fadeOut('slow');
                $('#dvLoading').fadeOut('slow');

            } else {
                alert('JPG, JPEG, GIF, PNG 이미지 확장자만 업로드가 가능합니다.');
                //$('#file_frm').val('');
                location.href = location.href;
                return false;
            }
        });
        // 닉네임 수정 실행버튼
        $('#nick_btn').on('click', function (e) {
            e.preventDefault();
            var nick = $('#txt_name').val().trim();
            if (nick.length < 2) {
                alert('닉네임은 2자이상 입니다.');
                $('#txt_name').focus();
                return false;
            }
            var ajax_result = AjaxExecute('/api/v1/users/me/nickname', 'PUT', {
                nickname: nick
            });
            if (IsValidStr(ajax_result.result_ko)) alert(ajax_result.result_ko);
            else alert(ajax_result);
        });
        // 비밀번호 변경 버튼
        $('#local_connect_btn').on('click', function (e) {
            e.preventDefault();
            var pass = $('#local_pass');
            var pass_confirm = $('#local_pass_confirm');
            // 공백 및 글자수 확인(4자이상)
            if (pass.val().trim() == '' || pass.val().trim().length < 4) {
                alert('비밀번호는 4자이상 입니다.');
                pass.focus();
                return false;
            }
            if (pass_confirm.val().trim() == '' || pass_confirm.val().trim().length < 4) {
                alert('비밀번호는 4자이상 입니다.');
                pass_confirm.focus();
                return false;
            }
            // 비밀번호 일치 확인   
            if (pass.val().trim() !== pass_confirm.val().trim()) {
                alert('비밀번호가 일치하지 않습니다.');
                pass.focus();
                return false;
            }
            var data = {
                new_pwd: pass.val().trim()
            };

            var ajax_result = AjaxExecute('/api/v1/users/me/pwd', 'PUT', data);
            if (IsValidStr(ajax_result.result_ko)) alert(ajax_result.result_ko);
            else alert(ajax_result);
        });
        // // 로컬계정 생성 취소 버튼
        // $('#local_connect_cancel_btn').on('click', function (e) {
        //     e.preventDefault();
        //     $('#local_pass').val('');
        //     $('#local_pass_confirm').val('');
        //     $('#local_connect_area').hide();
        //     $('#sp_local_desc').show();
        // });
        // 구글 연동 실행 버튼
        $('#google_btn').on('click', function (e) {
            e.preventDefault();
            location.href = '/api/v1/auth/google/signin';
        });
        // 페이스북 연동 실행 버튼
        $('#facebook_btn').on('click', function (e) {
            e.preventDefault();
            location.href = '/api/v1/auth/facebook/signin';
        });
        // 탈퇴 실행 버튼
        $('#remove_btn').on('click', function (e) {
            e.preventDefault();
            var ajax_result = AjaxExecute('/api/v1/users/me/bye', 'DELETE');
            if (IsValidStr(ajax_result.result_ko)) {
                alert(ajax_result.result_ko);
                logout();
            } else alert(ajax_result);
        });
    };
    this.memberInfo = function () {
        // 회원정보
        userinfo = AjaxExecute('/api/v1/users/me', 'GET');
        $('#sp_user_email').text(userinfo.email);
        $('#txt_name').val(userinfo.name);
        var g_btn = $('#google_btn');
        var f_btn = $('#facebook_btn');
        var tran_date = '';
        var connect_date = '';
        if (IsValidStr(userinfo.google.connect_time)) {
            g_btn.removeClass('connect_before').addClass('connect_after').val('연동완료').prop('disabled', 'disabled');
            if (IsValidObj(userinfo.google.connect_time)) {
                connect_date = new Date(userinfo.google.connect_time);
                tran_date = ConvertDateToString(connect_date);
            }
            $('#sp_google_desc').text(tran_date + ' (' + userinfo.google.name + ') 구글 계정과 연동됨');
        } else {
            $('#sp_google_desc').text('구글 계정과 연동되지 않은 상태입니다.');
            g_btn.removeClass('connect_after').addClass('connect_before').val('연동하기');
        }
        if (IsValidStr(userinfo.facebook.connect_time)) {
            f_btn.removeClass('connect_before').addClass('connect_after').val('연동완료').prop('disabled', 'disabled');
            if (IsValidObj(userinfo.facebook.connect_time)) {
                connect_date = new Date(userinfo.facebook.connect_time);
                tran_date = ConvertDateToString(connect_date);
            }
            $('#sp_facebook_desc').text(tran_date + ' (' + userinfo.facebook.name + ') 페이스북 계정과 연동됨');
        } else {
            $('#sp_facebook_desc').text('페이스북 계정과 연동되지 않은 상태입니다.');
            f_btn.removeClass('connect_after').addClass('connect_before').val('연동하기');
        }
    };
    this.bind = function () {
        local.preInit();
        local.selectEvent();
        local.btnClickEvents();
    };
};
$(function () {
    var script = new pageScript();
    script.bind();
});
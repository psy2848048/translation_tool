var pageScript = function () {
    var local = this,
        userinfo = '';
    this.preInit = function () {
        local.memberInfo();
        $('#hd_msg').val(getUrlParameter('results'));
        setTimeout(function () {
            if ($('#hd_msg').val() != '') alert($('#hd_msg').val());
        }, 200);
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

                        console.log('##### Upload Success #####');
                        console.log(res);
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        if (IsValidStr(xhr.responseText.result_ko)) alert(xhr.responseText.result_ko);
                        else alert('error code : ' + xhr.status);

                        console.log('##### Upload Error #####');
                        console.log('### xhr ###');
                        console.log(xhr);
                        console.log('### xhr.status ###');
                        console.log(xhr.status);
                        console.log('### xhr.responseText ###');
                        console.log(xhr.responseText);
                        console.log('### thrownError ###');
                        console.log(thrownError);
                        console.log('### ajaxOptions ###');
                        console.log(ajaxOptions);
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
            // $.ajax({
            //     url: '/api/v1/users/me/nickname',
            //     type: 'PUT',
            //     data: {
            //         nickname: nick
            //     },
            //     async: true,
            //     success: function (res) {
            //         alert(res.result_ko);

            //         console.log('##### 5214 #####');
            //         console.log(res);
            //     },
            //     error: function (err) {
            //         alert(err.result_ko);

            //         console.log('##### 9876 #####');
            //         console.log(err.responseText);
            //     }
            // });
            var ajax_result = AjaxExecute('/api/v1/users/me/nickname', 'PUT', {
                nickname: nick
            });
            if (IsValidStr(ajax_result.result_ko)) alert(ajax_result.result_ko);
            else alert(ajax_result);
        });
        // // 업로드 버튼 : onselected 방식으로 할지 click 방식으로 할지 미정
        // $('#name_btn').on('click', function (e) {
        //     e.preventDefault();
        //     alert('업로드 작업예정');
        // });
        // // 로컬계정 생성 버튼
        // $('#email_btn').on('click', function (e) {
        //     e.preventDefault();
        //     if (!$(this).hasClass('connect_after')) {
        //         $('#sp_local_desc').hide();
        //         $('#local_connect_area').show();
        //         $('#local_pass').focus();
        //     }
        // });
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
            // var res = AjaxExecute('/api/v1/users/me/pwd', 'PUT', data);
            // alert(res.result_ko);
            // console.log(res);

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
            // if (!$(this).hasClass('connect_after')) {
            //     $.ajax({
            //         url: '구글연동실행URL',
            //         type: 'GET',
            //         data: {
            //             구글연동: '데이타'
            //         },
            //         async: true,
            //         success: function (res) {
            //             alert('구글과 연동됐다 OK 헐크버전');
            //             $('#sp_google_desc').text('구글 계정과 연동되어 있습니다.');
            //             $('#google_btn').removeClass().addClass('local_connect_after');

            //             console.log('##### 9512 #####');
            //             console.log(res);
            //         },
            //         error: function (err) {
            //             alert('구글계정과 연동되지 않았습니다');

            //             console.log('##### 7599 #####');
            //             console.log(err.responseText);
            //         }
            //     });
            // }
            location.href = '/api/v1/auth/google/signin';
        });
        // 페이스북 연동 실행 버튼
        $('#facebook_btn').on('click', function (e) {
            e.preventDefault();
            // if (!$(this).hasClass('connect_after')) {
            //     $.ajax({
            //         url: '페이스북연동URL',
            //         type: 'GET',
            //         data: {
            //             페이스북연동: '데이타'
            //         },
            //         async: true,
            //         success: function (res) {
            //             alert('페이스북과 연동됐다 OK 헐크버전');
            //             $('#sp_facebook_desc').text('페이스북 계정과 연동되어 있습니다.');
            //             $('#facebook_btn').removeClass().addClass('local_connect_after');

            //             console.log('##### 1135 #####');
            //             console.log(res);
            //         },
            //         error: function (err) {
            //             alert('페이스북과 연동되지 않았습니다');

            //             console.log('##### 7592 #####');
            //             console.log(err.responseText);
            //         }
            //     });
            // }
            location.href = '/api/v1/auth/facebook/signin';
        });
        // 탈퇴 실행 버튼
        $('#remove_btn').on('click', function (e) {
            e.preventDefault();
            // $.ajax({
            //     url: '탈퇴실행URL',
            //     type: 'POST',
            //     data: {
            //         탈퇴: '데이타'
            //     },
            //     async: true,
            //     success: function (res) {
            //         alert('정상적으로 탈퇴되었습니다.\n\n굿바이 사요나라~');
            //         location.href = '/';

            //         console.log('##### 5858 #####');
            //         console.log(res);
            //     },
            //     error: function (err) {
            //         alert('회원탈퇴에 실패했습니다.');

            //         console.log('##### 4592 #####');
            //         console.log(err.responseText);
            //     }
            // });
            var ajax_result = AjaxExecute('/api/v1/users/me/bye', 'DELETE');
            if (IsValidStr(ajax_result.result_ko)) {
                alert(ajax_result.result_ko);
                logout();
                //location.href='/';
            } else alert(ajax_result);
        });
    };
    this.memberInfo = function () {
        // 회원정보
        userinfo = AjaxExecute('/api/v1/users/me', 'GET');
        $('#sp_user_email').text(userinfo.email);
        $('#txt_name').val(userinfo.name);
        // if (IsValidStr(userinfo.picture)) {
        //     $('#sp_user_picture').css('background', 'url(' + userinfo.picture + ')');
        // }
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

        // 회원사진정보
        //var mem_phpto = AjaxExecute('/api/v1/users/me/picture', 'GET');
        //console.log('mem_phpto' );
        //console.log(mem_phpto);
        //$('#sp_user_picture').html('<img src="' + 'data:image/jpeg;base64,' + hexToBase64(mem_phpto) + '" style="width:30px;height:30px;">');
        //$('#sp_user_picture').html('<img src="/api/v1/users/me/picture" style="width:50px;height:50px;">');
        //$('#sp_user_picture').html('<img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />');

        // var settings = {
        //     "async": true,
        //     "crossDomain": true,
        //     "url": "https://localhost:5001/api/v1/users/me/picture",
        //     "method": "GET",
        //     "headers": {
        //         "cache-control": "no-cache",
        //         "postman-token": "74c7bab0-9a05-27ab-c3f1-e1d11d79d915"
        //     }
        // };

        // $.ajax(settings).done(function (response) {
        //     console.log('response');
        //     console.log(response);
        // });
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
var pageScript = function () {
    var local = this;
    this.preInit = function () {
        setTimeout(function () {
            $('#txt_name').val(_USER_NICK);
        }, 200);
    };
    this.selectEvent = function () {
        $('#file_frm').on('change', function (e) {
            e.preventDefault();
            var reg_ext = ['JPG', 'JPEG', 'GIF', 'PNG'];
            var msg = 'JPG, JPEG, GIF, PNG 이미지 파일 확장자만 허용합니다.';
            onFileSelect($('#file_frm'), '업로드api-URL', 5, reg_ext, msg, 'upload_result');
        });
    };
    this.btnClickEvents = function () {
        // 닉네임 수정 실행버튼
        $('#nick_btn').on('click', function (e) {
            e.preventDefault();
            $.ajax({
                url: '닉네임수정URL',
                type: 'UPDATE',
                data: {
                    닉네임수정: '데이타'
                },
                async: true,
                success: function (res) {
                    console.log('##### 5214 #####');
                    console.log(res);
                },
                error: function (err) {
                    alert('닉네임이 수정되지 않았습니다');
                    console.log('##### 9876 #####');
                    console.log(err.responseText);
                }
            });
        });
        // 업로드 버튼 : onselected 방식으로 할지 click 방식으로 할지 미정
        $('#name_btn').on('click', function (e) {
            e.preventDefault();
            alert('업로드');
        });
        // 로컬계정 생성 버튼
        $('#email_btn').on('click', function (e) {
            e.preventDefault();
            if (!$(this).hasClass('connect_after')) {
                $('#sp_local_desc').hide();
                $('#local_connect_area').show();
                $('#local_pass').focus();
            }
        });
        // 로컬계정 생성 실행 버튼
        $('#local_connect_btn').on('click', function (e) {
            e.preventDefault();
            var pass = $('#local_pass');
            var pass_confirm = $('#local_pass_confirm');
            // 공백 및 글자수 확인(4자이상)
            if(pass.val().trim() == '' || pass.val().trim().length < 4){
                alert('비밀번호는 4자이상 입니다.');
                pass.focus();
                return false;
            }
            if(pass_confirm.val().trim() == '' || pass_confirm.val().trim().length < 4){
                alert('비밀번호는 4자이상 입니다.');
                pass_confirm.focus();
                return false;
            }
            // 비밀번호 일치 확인   
            if(pass.val().trim() !== pass_confirm.val().trim()){
                alert('비밀번호가 일치하지 않습니다.');
                pass.focus();
                return false;
            }         
            $.ajax({
                url: '로컬계정생성실행URL',
                type: 'POST',
                data: {
                    로컬계정생성: '데이타'
                },
                async: true,
                success: function (res) {
                    alert('로컬계정 비밀번호가 저장되었습니다.');
                    $('#local_connect_area').hide();
                    $('#sp_local_desc').text('로컬계정이 생성되어 있습니다.').show();
                    $('#email_btn').val('비밀번호 변경').removeClass().addClass('local_connect_after');

                    console.log('##### 6595 #####');
                    console.log(res);
                },
                error: function (err) {
                    alert('로컬계정이 생성되지 않았습니다');

                    console.log('##### 4563 #####');
                    console.log(err.responseText);
                }
            });
        });
        // 로컬계정 생성 취소 버튼
        $('#local_connect_cancel_btn').on('click', function (e) {
            e.preventDefault();
            $('#local_pass').val('');
            $('#local_pass_confirm').val('');
            $('#local_connect_area').hide();
            $('#sp_local_desc').show();
        });
        // 구글 연동 실행 버튼
        $('#google_btn').on('click', function (e) {
            e.preventDefault();
            if (!$(this).hasClass('connect_after')) {
                $.ajax({
                    url: '구글연동실행URL',
                    type: 'GET',
                    data: {
                        구글연동: '데이타'
                    },
                    async: true,
                    success: function (res) {
                        alert('구글과 연동됐다 OK 헐크버전');
                        $('#sp_google_desc').text('구글 계정과 연동되어 있습니다.');

                        console.log('##### 9512 #####');
                        console.log(res);
                    },
                    error: function (err) {
                        alert('구글계정과 연동되지 않았습니다');

                        console.log('##### 7599 #####');
                        console.log(err.responseText);
                    }
                });
            }
        });
        // 페이스북 연동 실행 버튼
        $('#facebook_btn').on('click', function (e) {
            e.preventDefault();
            if (!$(this).hasClass('connect_after')) {
                $.ajax({
                    url: '페이스북연동URL',
                    type: 'GET',
                    data: {
                        페이스북연동: '데이타'
                    },
                    async: true,
                    success: function (res) {
                        alert('페이스북과 연동됐다 OK 헐크버전');
                        $('#sp_google_desc').text('구글 계정과 연동되어 있습니다.').removeClass().addClass('local_connect_after');

                        console.log('##### 1135 #####');
                        console.log(res);
                    },
                    error: function (err) {
                        alert('페이스북과 연동되지 않았습니다');

                        console.log('##### 7592 #####');
                        console.log(err.responseText);
                    }
                });
            }
        });
        // 탈퇴 실행 버튼
        $('#remove_btn').on('click', function (e) {
            e.preventDefault();
            $.ajax({
                url: '탈퇴실행URL',
                type: 'POST',
                data: {
                    탈퇴: '데이타'
                },
                async: true,
                success: function (res) {
                    alert('정상적으로 탈퇴되었습니다.\n\n굿바이 사요나라~');
                    location.href='/';

                    console.log('##### 5858 #####');
                    console.log(res);
                },
                error: function (err) {
                    alert('회원탈퇴에 실패했습니다.');

                    console.log('##### 4592 #####');
                    console.log(err.responseText);
                }
            });
        });
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
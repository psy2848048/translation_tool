var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project');
    this.preInits = function () {
        var minutePadding = 10;
        $('#limited_date_area').append(SetDateSelect(2028, minutePadding) + ' <input type="checkbox" id="chk_no_limit"> <label for="chk_no_limit">제한없음</label>');
        SetToday();
        ResetDay();
        if ($('#sel_month').val() == 2 || $('#sel_month').val() == '02') SetToday();
    };
    this.btnEvents = function () {
        // 기간 제한없음 체크박스
        $(document).on('click', '#chk_no_limit', function (e) {
            if ($(this).prop('checked') == true) {
                $('#sel_year').attr('disabled', true);
                $('#sel_month').attr('disabled', true);
                $('#sel_day').attr('disabled', true);
                $('#sel_hour').attr('disabled', true);
                $('#sel_minute').attr('disabled', true);
            } else {
                $('#sel_year').attr('disabled', false);
                $('#sel_month').attr('disabled', false);
                $('#sel_day').attr('disabled', false);
                $('#sel_hour').attr('disabled', false);
                $('#sel_minute').attr('disabled', false);
            }
        });
        // 프로젝트 저장버튼
        $('#mainArea input[type=button]').on('click', function () {
            if ($('#txt_title').val().trim() == '') {
                alert('프로젝트명을 입력해주세요');
                $('#txt_title').focus();
                return false;
            }
            var date = '';
            if ($('#chk_no_limit').prop('checked') == false) {
                var year = $('#limited_date_area select:nth-of-type(1)').val(),
                    month = $('#limited_date_area select:nth-of-type(2)').val(),
                    day = $('#limited_date_area select:nth-of-type(3)').val(),
                    hour = $('#limited_date_area select:nth-of-type(4)').val(),
                    minute = $('#limited_date_area select:nth-of-type(5)').val();
                if (year == '') {
                    alert('년도를 선택해주세요');
                    return false;
                }
                if (month == '') {
                    alert('월을 선택해주세요');
                    return false;
                }
                if (day == '') {
                    alert('일을 선택해주세요');
                    return false;
                }
                if (hour == '') {
                    alert('시를 선택해주세요');
                    return false;
                }
                if (minute == '') {
                    alert('분을 선택해주세요');
                    return false;
                }
                date = year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
            }
            date = $('#chk_no_limit').prop('checked') ? '' : new Date(date).toGMTString();
            var data = {
                name: $('#txt_title').val(),
                due_date: date
            };
            $.ajax({
                url: '/api/v1/projects/',
                type: 'POST',
                data: data,
                async: true,
                success: function (args) {
                    if (args.result.toUpperCase() == 'OK') {
                        alert('프로젝트가 정상적으로 등록되었습니다.');
                        location.href = 'projects.html';
                    } else {
                        alert('등록실패\n\n에러코드 : 8893');
                    }
                },
                error: function (e) {
                    alert('등록실패\n\n에러코드 : 9976');
                }
            });
        });
    };
    this.bind = function () {
        local.preInits();
        local.btnEvents();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();
});
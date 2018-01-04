var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project');
    this.preInits = function () {
        var minutePadding = 10;
        $('#limited_date_area').append(SetDateSelect(2028, minutePadding));   
        SetToday();
        ResetDay();   
        if ($('#sel_month').val() == 2 || $('#sel_month').val() == '02') SetToday();         
    };
    this.btnEvents = function () {
        // 프로젝트 등록버튼 클릭
        $('#mainArea input[type=button]').on('click', function () {
            if ($('#txt_title').val().trim() == '') {
                alert('프로젝트명을 입력해주세요');
                $('#txt_title').focus();
                return false;
            }
            var date = '',
                year = $('#limited_date_area select:nth-of-type(1)').val(),
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
            var data = {
                project_name: $('#txt_title').val(),
                duration_date: date
            };
            console.log('data 4251 : ', data);
            $.ajax({
                url: '/api/v1/users/1/projects',
                type: 'POST',
                data: data,
                async: true,
                success: function (args) {
                    if (args == 'OK') {
                        alert(args);
                        location.href = 'project_view.html?project=프로젝트아이디';
                    } else {
                        alert('등록실패 8893');
                    }
                },
                error: function (e) {
                    alert('fail 9976');
                    console.log(e.responseText);
                }
            });
        });
    };
    this.changeEvents = function () {

    };
    this.bind = function () {
        local.preInits();
        local.btnEvents();
        local.changeEvents();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();
});
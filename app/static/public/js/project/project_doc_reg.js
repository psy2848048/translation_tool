var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project');
    this.preInits = function () {
        SetMenuColor(getUrlParameter('project'), '프로젝트', '#ulProjectList li', '?project=', 'a', 'orange');

        var minutePadding = 10;
        $('#limited_date').append(SetDateSelect(2028, minutePadding) + ' <input type="checkbox" id="chk_no_limit"> <label for="chk_no_limit">제한없음</label>');
        SetToday();
        ResetDay();
        if ($('#sel_month').val() == 2 || $('#sel_month').val() == '02') SetToday();

        var jqxhr = $.get('/api/v1/7/projects/', function (data) {
                //console.log('[/api/v1/7/projects/] : ', data);
                //console.log('[/api/v1/7/projects/ data.results[0] : ', data.results[0]);
                // 좌측 프로젝트 리스트
                var menu = '',
                    list = '';
                if (data != undefined && data.results != '') {
                    menu += '<ul id="ulProjectList" style="max-height:200px;overflow-x:hidden;overflow-y:auto;">';
                    $(data.results).each(function (idx, res) {
                        menu += '<li>';
                        if (project_id == res.id) menu += '   <a style="color:orange" href="/static/front/project/project_view.html?project=' + res.id + '">└ ' + res.name + '</a>';
                        else menu += '   <a href="/static/front/project/project_view.html?project=' + res.id + '">└ ' + res.name + '</a>';
                        menu += '</li>';
                    });
                    menu += '</ul>';

                    $('#left_menu_area>li:nth-of-type(1)').append(menu);
                }
            })
            .done(function () {})
            .fail(function () {
                console.log("error 4416");
            })
            .always(function () {});
        jqxhr.always(function () {});
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
        // 파일로 업로드 버튼
        $('#rdo_file').on('click', function (e) {
            e.preventDefault();
            //$('#dv_file').fadeIn();
            //$('#dv_text').fadeOut();
            alert('파일업로드 방식은 개발중에 있습니다.');
        });
        // 텍스트로 등록
        $('#rdo_text').on('click', function () {
            $('#dv_file').fadeOut();
            $('#dv_text').fadeIn();
        });
        // 문서 추가
        $('#mainArea input[type=button]').on('click', function (e) {
            e.preventDefault();  
            if($('#txt_title').val().trim() == ''){
                alert('문서제목을 입력해주세요.');
                  $('#txt_title').focus();
              return false;
            }          
            var date = '';
            if ($('#chk_no_limit').prop('checked') == false) {
                var year = $('#limited_date select:nth-of-type(1)').val(),
                    month = $('#limited_date select:nth-of-type(2)').val(),
                    day = $('#limited_date select:nth-of-type(3)').val(),
                    hour = $('#limited_date select:nth-of-type(4)').val(),
                    minute = $('#limited_date select:nth-of-type(5)').val();
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
                'title': $('#txt_title').val(),
                'origin_lang': $('#org_sel').val(),
                'trans_lang': $('#tran_sel').val(),
                'due_date': date,
                'type': 'text',
                'content': $('#mainArea textarea').val()
            };
            console.log('[data] : ', data);
            $.ajax({
                url: '/api/v1/7/projects/' + project_id + '/docs',
                type: 'POST',
                data: data,
                async: true,
                success: function (args) {
                    if(args.result == 'OK'){
                        alert('정상적으로 저장되었습니다.');
                        location.href='project_view.html?project=' + project_id;
                    }else{
                        alert('저장에 실패했습니다.\n\n오류코드 : 7784');
                    }
                },
                error: function (err) {
                    alert('fail : error code 4157');
                    console.log('fail : error code 4157');
                    console.log(err.responseText);
                }
            });
        });
    };
    this.selectEvent = function () {
        $('#mainArea article input[type=file]').on('change', function (e) {
            e.preventDefault();
            //var reg_ext = ['JPG','JPEG','GIF','PNG'];
            var reg_ext = ['TXT'];
            var msg = 'txt 파일 확장자만 허용합니다.';
            onFileSelect($('#mainArea article input[type=file]'), '파일을받을서버URL', 5, reg_ext, msg);
        });
    };
    this.bind = function () {
        local.preInits();
        local.btnEvents();
        local.selectEvent();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();

    $('#ulProjectList').show();
});
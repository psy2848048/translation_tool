var PageScript = function () {
    var local = this,
        rows = IsValidStr(getUrlParameter('rows')) ? getUrlParameter('rows') : '15',
        page = IsValidStr(getUrlParameter('page')) ? getUrlParameter('page') : '1',
        project_id = getUrlParameter('project'),
        cur_path = $(location).attr('pathname');
    this.preInits = function () {
        var minutePadding = 10;
        //$('#limited_date_area').append(SetDateSelect(2028, minutePadding) + ' <input type="checkbox" id="chk_no_limit"> <label for="chk_no_limit">제한없음</label><br>Mon, 05 Feb 2018 16:57:39 GMT<br>Tue Feb 06 2018 01:57:39 GMT+0900 (KST)');
        $('#limited_date_area').append(SetDateSelect(2028, minutePadding) + ' <input type="checkbox" id="chk_no_limit"> <label for="chk_no_limit">제한없음</label>');
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
        // 프로젝트 저장버튼 클릭
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
                status: $('#status_sel').val(),
                due_date: date
            };
            console.log('[data 4251] : ', data);
            $.ajax({
                url: '/api/v1/7/projects/' + project_id,
                type: 'PUT',
                data: data,
                async: true,
                success: function (args) {
                    if (args.result == 'OK') {
                        alert('정상적으로 수정되었습니다.');
                        location.href = 'project_view.html?project=' + project_id;
                    } else {
                        alert('수정실패\n\n오류코드 : 8893');
                    }
                },
                error: function (e) {
                    alert('fail\n\n오류코드 : 7591');
                    console.log(e.responseText);
                }
            });
        });
    };
    this.getProjects = function () {
        local.mask();

        $(document).ajaxStart(function () {
            $('#dvLoading').show();
        });
        $(document).ajaxComplete(function (event, request, settings) {
            $('#dvLoading').hide();
        });

        // 본문중앙 프로젝트 상세설명            
        $.ajax({
            url: '/api/v1/7/projects/' + project_id,
            type: 'GET',
            async: true,
            success: function (res) {
                console.log('[/api/v1/7/projects/' + project_id + '] : ', res);
                if (res != undefined && res != '') {
                    $('#txt_title').val(res.name);
                    $('#status_sel').val(res.status);

                    if (IsValidObj(res.due_date)) {
                        var dt_duedate = new Date(res.due_date);
                        $('#sel_year').val(dt_duedate.getFullYear());
                        $('#sel_month').val(AddPreZero(parseInt(dt_duedate.getMonth() + 1)));
                        $('#sel_day').val(AddPreZero(dt_duedate.getDate()));
                        var h = dt_duedate.getHours(),
                            m = dt_duedate.getMinutes();
                        if (parseInt(m) > 54) {
                            h = parseInt(h) + parseInt(1);
                            m = '00';
                        }
                        $('#sel_hour').val(AddPreZero(h));
                        $('#sel_minute').val(AddPreZero(m));
                    } else {
                        $('#chk_no_limit').prop('checked', true);

                        $('#sel_year').attr('disabled', true);
                        $('#sel_month').attr('disabled', true);
                        $('#sel_day').attr('disabled', true);
                        $('#sel_hour').attr('disabled', true);
                        $('#sel_minute').attr('disabled', true);
                    }
                }
            },
            error: function (e) {
                console.log('fail 8526');
                console.log(e.responseText);
            }
        });
        // 좌측 프로젝트 메뉴리스트
        var jqxhr = $.get('/api/v1/7/projects?rows=1000', function (data) {
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
                console.log("error 3594");
            })
            .always(function () {});
        jqxhr.always(function () {});

        $('#mask').fadeIn(1000);
        $('#mask').fadeTo("slow", 1000).hide();
    };
    this.mask = function () {
        $('#mask').css({
            'width': $(document).height(),
            'height': $(window).width()
        });
    };
    this.bind = function () {
        local.preInits();
        local.btnEvents();
        local.getProjects(project_id);
    };
};
$(function () {
    var script = new PageScript();
    script.bind();
});
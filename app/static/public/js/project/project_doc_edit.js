var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project');
    this.preInits = function () {
        SetMenuColor(getUrlParameter('project'), '프로젝트', '#ulProjectList li', '?project=', 'a', 'orange');

        var minutePadding = 10;
        $('#limited_date').append(SetDateSelect(2028, minutePadding) + ' <input type="checkbox" id="chk_no_limit"> <label for="chk_no_limit">제한없음</label>');

        // 좌측 프로젝트 메뉴리스트
        var jqxhr = $.get('/api/v1/users/1/projects/', function (data) {
                console.log('(좌측메뉴) /api/v1/users/1/projects/ : ', data);
                // 좌측메뉴
                var menu = '',
                    list = '';
                if (data != undefined && data.result != '') {
                    menu += '<ul id="ulProjectList" style="max-height:200px;overflow-x:hidden;overflow-y:auto;">';
                    $(data.result).each(function (idx, res) {
                        menu += '<li>';
                        if (project_id == res.project_id) menu += '   <a style="color:orange" href="/static/front/project/project_view.html?project=' + res.project_id + '">└ ' + res.project_name + '</a>';
                        else menu += '   <a href="/static/front/project/project_view.html?project=' + res.project_id + '">└ ' + res.project_name + '</a>';
                        menu += '</li>';
                    });
                    menu += '</ul>';

                    $('#left_menu_area>li:nth-of-type(1)').append(menu);
                }
            })
            .done(function () {})
            .fail(function () {
                alert("error 4268");
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
        $('#rdo_file').on('click', function () {
            $('#dv_file').fadeIn();
            $('#dv_text').fadeOut();
        });
        // 텍스트로 등록
        $('#rdo_text').on('click', function () {
            $('#dv_file').fadeOut();
            $('#dv_text').fadeIn();
        });
        $('#mainArea input[type=button]').on('click', function () {
            var data = {
                // example!
                "project_id": 1,
                "doc_title": $('#txt_title').val(),
                "doc_content": $('#mainArea textarea').val()
            };
            $.ajax({
                url: 'http://52.196.164.64/translate',
                type: 'post',
                data: data,
                async: true,
                success: function (args) {
                    alert(args);
                    location.href = 'project_view.html?project=' + getUrlParameter('project');
                },
                error: function (e) {
                    alert('fail');
                    console.log(e.responseText);
                    location.href = 'project_view.html?project=' + getUrlParameter('project');
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

    $('#ulProjectList').show();
});
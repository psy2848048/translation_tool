var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project');
    this.preInits = function () {
        // 프로젝트의 작업리스트 신규 버튼
        $('#listTitleGroup li:nth-of-type(1) a').attr('href', 'project_doc_reg.html?project=' + project_id);
    };
    this.btnEvents = function () {
        // 체크박스 전체선택, 해제
        $('#listContents th input[type=checkbox]').on('click', function (e) {
            e.preventDefault();
            if ($(this).prop('checked')) {
                $('#listContents td input[type=checkbox]').each(function () {
                    $(this).prop('checked', true);
                });
            } else {
                $('#listContents td input[type=checkbox]').each(function () {
                    $(this).prop('checked', false);
                });
            }
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
            url: '/api/v1/users/1/projects/' + project_id,
            type: 'GET',
            //data: data,
            async: true,
            success: function (res) {
                console.log('res 5546 : ', res);
                //location.href = 'project_view.html?project=새프로젝트번호';
                if (res != undefined && res != '') {
                    $('#sp_project_id').val(res.id);
                    $('#sp_status').val(res.status);
                    $('#sp_org_lang').val(res.origin_langs);
                    $('#sp_trans_lang').val(res.trans_langs);
                    $('#requester').val(res.client_company + ' ' + res.clients);
                    $('#transer').val(res.trans_company + ' ' + res.translators);
    
                    var str_ddate = '';
                    if (res.duration_time != '') str_ddate = GetStringDate(new Date(res.duration_time));
                    $('#duration_date').val(str_ddate);

                    var str_cdate = '';
                    if (res.create_time != '') str_cdate = GetStringDate(new Date(res.duration_time));
                    $('#reg_date').val(str_cdate);
                }
            },
            error: function (e) {
                alert('fail 4516');
                console.log(e.responseText);
                //location.href = 'project_view.html?project=새프로젝트번호';
            }
        });

        // 좌측 프로젝트 메뉴리스트
        var jqxhr = $.get('/api/v1/users/1/projects/', function (data) {
                console.log('/api/v1/users/1/projects/ : ', data);
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

        // 본문 프로젝트 문서 목록
        var doc_list = $.get('/api/v1/users/1/projects/' + project_id, function (data) {
                console.log('/api/v1/users/1/projects/1 : ', data);
                var row = '';
                $(data.project_docs).each(function (idx, res) {
                    if (data != undefined) {
                        row += '<tr>';
                        row += '    <td><input type="checkbox"></td>';
                        row += '    <td>' + parseInt(idx + 1) + '</td>';
                        row += '    <td>' + res.progress_percent + '</td>';
                        row += '    <td class="oneline_wrap"><a target="_blank" title="' + res.name + '" href="/static/trans/trans.html?project_id=' + project_id + '&doc_id="' + res.doc_id + '>' + res.name + '</a></td>';
                        row += '    <td>' + res.status + '</td>';
                        row += '    <td><a target="_blank" href="' + res.link + '">링크</a></td>';
                        //row += '    <td>KO<span class="super">KR</span></td>';
                        row += '    <td>' + res.trans_lang + '</td>';
                        row += '    <td>' + res.trans_company + ' ' + res.translator + '</td>';

                        var str_date = '';
                        if (res.duration_time != '') str_date = GetStringDate(new Date(res.duration_time));
                        row += '    <td>' + str_date + '</td>';

                        row += '</tr>';
                    }
                });
                $('#listContents table tbody').append(row);
            })
            .done(function () {})
            .fail(function () {
                alert("error");
            })
            .always(function () {});
        doc_list.always(function () {});

        $('#mask').fadeIn(1000);
        $('#mask').fadeTo("slow", 1000).hide();
    };
    this.mask = function () {
        //화면의 높이와 너비를 구한다.
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        //마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
        $('#mask').css({
            'width': maskWidth,
            'height': maskHeight
        });
    };
    this.bind = function () {
        local.preInits();
        local.btnEvents();
        local.getProjects(getUrlParameter('project'));
    };
};
$(function () {
    var script = new PageScript();
    script.bind();

    $(document).tooltip({
        track: true
    });
});
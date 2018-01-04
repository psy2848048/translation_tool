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
            //e.preventDefault(); 활성화 하면 체크 안됨!
            CheckAll($(this), '#listContents td input[type=checkbox]');
        });
        // 문서 편집버튼 클릭
        $(document).on('click', '#listContents input[type=button]', function(){
            var doc_id = $(this).attr('data-id');
            location.href='project_doc_edit.html?project=' + project_id + '&doc_id=' + doc_id;
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
                console.log('(프로젝트 상세설명) res : ', res);
                //location.href = 'project_view.html?project=새프로젝트번호';
                if (res != undefined && res != '') {
                    $('#h2_title').text(res.name);
                    $('#sp_project_id').text(res.id);
                    $('#sp_status').text(res.status);

                    if (res.origin_langs != null && res.origin_langs != '') $('#sp_org_lang').text(res.origin_langs.toUpperCase());
                    else $('#sp_org_lang').text(res.origin_langs);

                    if (res.trans_langs != null && res.trans_langs != '') $('#sp_trans_lang').text(res.trans_langs.toUpperCase());
                    else $('#sp_trans_lang').text(res.trans_langs);

                    $('#requester').text(res.client_company + ' ' + res.clients);
                    $('#transer').text(res.trans_company + ' ' + res.translators);

                    var str_ddate = '';
                    if (res.duration_date != '') str_ddate = GetStringDate(new Date(res.duration_date));
                    $('#duration_date').text(str_ddate);

                    var str_cdate = '';
                    if (res.create_time != '') str_cdate = GetStringDate(new Date(res.create_time));
                    $('#reg_date').text(str_cdate);
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

        // 본문 프로젝트 문서 목록
        var doc_list = $.get('/api/v1/users/1/projects/1/docs', function (data) {
                console.log('(문서목록) /api/v1/users/1/projects/1/docs : ', data);
                var row = '';
                $(data.result).each(function (idx, res) {
                    if (data != undefined) {
                        row += '<tr>';
                        row += '    <td><input type="checkbox"></td>';
                        row += '    <td>' + parseInt(idx + 1) + '</td>';
                        row += '    <td>' + res.progress_percent + '</td>';
                        row += '    <td class="oneline_wrap"><a target="_blank" title="' + res.title + '" href="/static/front/trans/trans.html?project=' + project_id + '&doc_id=' + res.project_docs_id + '">' + res.title + '</a></td>';
                        row += '    <td>' + res.status + '</td>';
                        //if(res.progress_percent == 100) row += '    <td>완료</td>';
                        //else row += '    <td>' + res.status + '</td>';
                        row += '    <td><a target="_blank" href="' + res.link + '">링크</a></td>';
                        //row += '    <td>KO<span class="super">KR</span></td>';

                        if (res.origin_lang != null && res.origin_lang != '') row += '    <td>' + res.origin_lang.toUpperCase() + '</td>';
                        else row += '    <td>' + res.origin_lang + '</td>';

                        if (res.trans_lang != null && res.trans_lang != '') row += '    <td>' + res.trans_lang.toUpperCase() + '</td>';
                        else row += '    <td>' + res.trans_lang + '</td>';

                        //row += '<td class="oneline_wrap" title="' + NullToEmpty(res.translators) + '">' + NullToEmpty(res.translators) + '</td>';

                        var str_date = '';
                        if (res.duration_date != '' && res.duration_date != null) str_date = GetStringDate(new Date(res.duration_date));
                        row += '    <td>' + str_date + '</td>';
                        row += '    <td><input data-id="' + res.project_docs_id + '" type="button" value="편집"></td>';

                        row += '</tr>';
                    }
                });
                //console.log('문서목록 : ', row);
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
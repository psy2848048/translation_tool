var PageScript = function () {
    var local = this,
        rows = IsValidStr(getUrlParameter('rows')) ? getUrlParameter('rows') : '20',
        page = IsValidStr(getUrlParameter('page')) ? getUrlParameter('page') : '1',
        project_id = getUrlParameter('project'),
        cur_path = $(location).attr('pathname');
    this.preInits = function () {
        // 문서 목록 신규 버튼
        $('#listTitleGroup li:nth-of-type(1) a').attr('href', 'project_doc_reg.html?project=' + project_id);
    };
    this.btnEvents = function () {
        // 프로젝트 수정 버튼
        $('#edit_btn').on('click', function () {
            location.href = 'project_edit.html?project=' + project_id;
        });
        // 프로젝트 삭제 버튼                
        $('#del_btn').on('click', function () {
            if (confirm('정말로 삭제하시겠습니까?')) {
                $.ajax({
                    url: '/api/v1/projects/' + project_id,
                    type: 'DELETE',
                    async: true,
                    success: function (res) {
                        if (res.result == 'OK') {
                            alert('프로젝트가 삭제되었습니다.');
                            location.href = 'projects.html?rows=' + rows + '&page=' + page;
                        }
                    },
                    error: function (e) {
                        alert('fail 8965');
                    }
                });
            }
        });
        // 프로젝트 문서 삭제 버튼
        $('#listTitleGroup li:nth-of-type(2) a').on('click', function () {
            if (confirm('정말로 삭제하시겠습니까?')) {
                if ($('#listContents td input[type=checkbox]:checked').length > 0) {
                    //alert('프로젝트 삭제 프로세스 : 체크된 문서 갯수만큼 루핑 하면서 삭제한다.');

                    $('#listContents td input[type=checkbox]:checked').each(function () {
                        $.ajax({
                            url: '/api/v1/projects/docs/' + $(this).attr('data-id'),
                            type: 'DELETE',
                            async: true,
                            success: function (res) {
                                if(res.result == 'OK') {
                                    alert('문서가 삭제되었습니다.');
                                }
                            },
                            error: function (e) {
                                alert('삭제실패\n\nfail code : 3365');
                                return false;
                            }
                        });
                    });
                } else {
                    alert('체크된 문서가 없습니다.');
                }
                location.href = 'project_view.html?project=' + project_id;
            }
        });
        // 프로젝트 참가자 초대 버튼
        $('#invite_btn, #invite_btn_min').on('click', function () {
            location.href = '/static/front/user/users.html?project=' + project_id;
        });
        // 체크박스 전체선택, 해제
        $('#listContents th input[type=checkbox]').on('click', function (e) {
            //e.preventDefault(); 활성화 하면 체크 안됨!
            CheckAll($(this), '#listContents td input[type=checkbox]');
        });
        // 문서 편집버튼 클릭
        $(document).on('click', '#listContents input[type=button]', function () {
            var doc_id = $(this).attr('data-id');
            location.href = 'project_doc_edit.html?project=' + project_id + '&doc_id=' + doc_id;
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
            url: '/api/v1/projects/' + project_id,
            type: 'GET',
            async: true,
            success: function (res) {
                if (res != undefined && res != '') {
                    $('#h2_title').text(res.name);
                    $('#sp_project_id').text(res.id);
                    $('#sp_status').text(res.status);

                    if (res.origin_langs != null) $('#sp_org_lang').text(res.origin_langs.toUpperCase());
                    else $('#sp_org_lang').text('');

                    if (res.trans_langs != null) $('#sp_trans_lang').text(res.trans_langs.toUpperCase());
                    else $('#sp_trans_lang').text('');

                    $('#requester').text(res.client_company + ' ' + res.clients);
                    $('#transer').text(res.trans_company + ' ' + res.translators);

                    //var str_ddate = GetDurationText(res.due_date);
                    // if (res.due_date == null || res.due_date == '' || res.due_date == '1970-01-01 09:00') str_ddate = '제한없음';
                    // else str_ddate = GetStringDate(new Date(res.due_date), '1');                    
                    $('#duration_date').text(GetDateText(res.due_date, '1', '1'));

                    // var str_cdate = '';
                    // if (res.create_time == null || res.create_time == '' || res.create_time == '1970-01-01 09:00') str_cdate = '';
                    // else str_cdate = GetStringDate(new Date(res.create_time), '1');
                    $('#reg_date').text(GetDateText(res.create_time, '0', '1'));

                    var mem = res.project_members == null ? '' : res.project_members;
                    $('#sp_members').text(mem);
                }
            },
            error: function (e) {
                alert('fail 4436');
            }
        });
        // 좌측 프로젝트 메뉴리스트
        var jqxhr = $.get('/api/v1/projects?rows=1000', function (data) {
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
                alert("error 4416");
            })
            .always(function () {});
        jqxhr.always(function () {});

        // 본문 프로젝트 문서 목록
        var doc_list = $.get('/api/v1/projects/' + project_id + '/docs?rows=' + rows + '&page=' + page, function (data) {
                if (data != undefined && data != null && data.results != undefined && data.results != null && parseInt(data.results.length) > 0) {
                    var row = '';
                    $(data.results).each(function (idx, res) {
                        row += '<tr>';
                        row += '    <td><input type="checkbox" data-id="' + res.id + '"></td>';
                        row += '    <td>' + parseInt(idx + 1) + '</td>';

                        if(res.progress_percent == 100) row += '    <td><a href="/api/v1/toolkit/workbench/docs/' + res.id + '/output?type=txt" download>다운로드</a></td>';
                        else row += '    <td>' + res.progress_percent + '%</td>';

                        row += '    <td class="oneline_wrap"><a target="_blank" title="' + res.title + '" href="/static/front/trans/trans.html?project=' + project_id + '&doc_id=' + res.id + '">' + res.title + '</a></td>';
                        row += '    <td>' + res.status + '</td>';

                        if (res.link == null || res.link.trim() == '') row += '    <td>&nbsp;</td>';
                        else row += '    <td><a target="_blank" href="' + res.link + '">링크</a></td>';

                        if (res.origin_lang != null && res.origin_lang != '') row += '    <td>' + res.origin_lang.toUpperCase() + '</td>';
                        else row += '    <td>' + res.origin_lang + '</td>';

                        if (res.trans_lang != null && res.trans_lang != '') row += '    <td>' + res.trans_lang.toUpperCase() + '</td>';
                        else row += '    <td>' + res.trans_lang + '</td>';

                        row += '    <td>' + GetDateText(res.due_date, '1', '1') + '</td>';
                        
                        row += '    <td><input data-id="' + res.id + '" type="button" value="편집"></td>';

                        row += '</tr>';
                    });
                    $('#listContents table tbody').append(row);
                }
                var param_path = cur_path + '?project=' + project_id + '&rows=' + rows + '&';
                SetPagebar(parseInt(data.total_cnt), rows, page, param_path, 10);
            })
            .done(function () {})
            .fail(function () {
                alert("error 3396");
            })
            .always(function () {});
        doc_list.always(function () {});

        $('#mask').fadeIn(1000);
        $('#mask').fadeTo("slow", 2000).hide();
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

    $(document).tooltip({
        track: true
    });
});
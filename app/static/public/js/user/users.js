var PageScript = function () {
    var local = this,
        rows = IsValidStr(getUrlParameter('rows')) ? getUrlParameter('rows') : '10',
        page = IsValidStr(getUrlParameter('page')) ? getUrlParameter('page') : '1',
        project_id = getUrlParameter('project'),
        //first_project_id = '',
        cur_path = $(location).attr('pathname');
    this.preInits = function () {
        // 좌측 프로젝트 리스트
        var jqxhr = $.get('/api/v1/7/projects?rows=1000', function (data) {
                //console.log('[/api/v1/7/projects/] : ', data);
                //console.log('[/api/v1/7/projects/ data.results[0] : ', data.results[0]);
                // 좌측 프로젝트 리스트
                var menu = '',
                    list = '';
                if (data != undefined && data.results != '') {

                    if (project_id == undefined || project_id.trim() == '') {
                        location.href = 'users.html?project=' + data.results[0].id + '&rows=' + rows + '&page=' + page;
                    } else {
                        menu += '<ul id="ulProjectList2" style="max-height:200px;overflow-x:hidden;overflow-y:auto;">';
                        $(data.results).each(function (idx, res) {
                            menu += '<li>';
                            if (project_id == res.id) menu += '   <a style="color:orange" href="/static/front/user/users.html?project=' + res.id + '">└ ' + res.name + '</a>';
                            else menu += '   <a href="/static/front/user/users.html?project=' + res.id + '">└ ' + res.name + '</a>';
                            menu += '</li>';
                        });
                        menu += '</ul>';
                        $('#left_menu_area>li:nth-of-type(4)').append(menu);

                        local.getUsers();
                    }
                }
            })
            .done(function () {})
            .fail(function () {
                console.log("error 4416");
            })
            .always(function () {});
        jqxhr.always(function () {});
    };
    this.btnEvents = function () { // 체크박스 전체선택, 해제   
        // 프로젝트 참가자 삭제
        $('#listTitleGroup li:nth-of-type(1)').on('click', function () {
            if ($('#listContents table td:nth-of-type(1) input[type=checkbox]:checked').length > 0) {
                $('#listContents table td:nth-of-type(1) input[type=checkbox]:checked').each(function () {
                    console.log('선택된 사용자 삭제 : ', $(this).closest('tr').find('td:eq(3)').text());
                });
            } else {
                alert('선택된 사용자가 없습니다.');
            }
        });
        // 검색버튼 클릭
        $('#listTitleGroup2 li:nth-of-type(2)').on('click', function () {
            alert($('#txt_search').val());
        });
        // (검색 후)추가버튼 클릭
        $('#listTitleGroup2 li:nth-of-type(3)').on('click', function () {
            if ($('#listContents2 table td:nth-of-type(1) input[type=checkbox]:checked').length > 0) {
                $('#listContents2 table td:nth-of-type(1) input[type=checkbox]:checked').each(function () {
                    console.log('체크된 사용자 : ', $(this).closest('tr').find('td:eq(3)').text());
                });
            } else {
                alert('선택된 사용자가 없습니다.');
            }
        });
        // 체크박스 전체선택, 해제
        $('#listContents th input[type=checkbox]').on('click', function (e) {
            //e.preventDefault(); 활성화 하면 체크 안됨!
            CheckAll($(this), '#listContents td input[type=checkbox]');
        });
        $('#listContents2 th input[type=checkbox]').on('click', function (e) {
            //e.preventDefault(); 활성화 하면 체크 안됨!
            CheckAll($(this), '#listContents2 td input[type=checkbox]');
        });
    };
    this.show = function () {
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();
        $('#mask').css({
            'width': maskWidth,
            'height': maskHeight
        });
    };
    this.hide = function () {
        $('#mask').fadeTo("slow", 1000).hide();
        $('#loading_img').fadeTo("slow", 1000).hide();
    };
    this.getUsers = function (first_project_id) {
        if (project_id == undefined || project_id.trim() == '') {
            location.href = 'users.html?project=' + first_project_id + '&rows=' + rows + '&page=' + page;
        } else {            
            local.show();
            $.ajax({
                url: '/api/v1/7/projects/' + project_id + '/members?page=' + page + '&rows=' + rows,
                type: 'GET',
                async: true,
                success: function (res) {
                    console.log('7784 [/api/v1/7/projects/' + project_id + '/members?page=' + page + '&rows=' + rows + '] : ', res);
                    var html = '';
                    if (res != undefined && res.results.length > 0) {
                        $(res.results).each(function (idx) {
                            var result = res.results[idx];
                            console.log('1542 [result]');
                            console.log(result);
                            html += '<tr>';
                            html += '    <td>';
                            html += '        <input type="checkbox">';
                            html += '    </td>';
                            html += '    <td>' + parseInt(idx + 1) + '</td>';
                            html += '    <td>' + result.name + '</td>';
                            html += '    <td>' + result.email + '</td>';
                            html += '    <td>';
                            html += '        <input type="checkbox" checked="checked" disabled="disabled">';
                            html += '    </td>';
                            html += '    <td>';
                            html += '        <input type="checkbox" checked="checked" disabled="disabled">';
                            html += '    </td>';
                            html += '    <td>';
                            html += '        <input type="checkbox" checked="checked" disabled="disabled">';
                            html += '    </td>';
                            html += '    <td>';
                            html += '        <input type="checkbox" checked="checked" disabled="disabled">';
                            html += '    </td>';
                            html += '</tr>';
                        });
                        $('#listContents table tbody tr').after(html);
                        var param_path = cur_path + '?project=' + project_id + '&rows=' + rows + '&';
                        SetPagebar(parseInt(res.total_cnt), rows, page, param_path, 10);
                    }
                    local.hide();
                },
                error: function (e) {
                    console.log('fail 3348');
                    console.log(e.responseText);
                    local.hide();
                }
            });
        }
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
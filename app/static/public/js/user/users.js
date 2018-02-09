var PageScript = function () {
    var local = this,
        rows = IsValidStr(getUrlParameter('rows')) ? getUrlParameter('rows') : '10',
        page = IsValidStr(getUrlParameter('page')) ? getUrlParameter('page') : '1',
        project_id = getUrlParameter('project'),
        //first_project_id = '',
        cur_path = $(location).attr('pathname');
    this.preInits = function () {
        // 좌측 프로젝트 리스트
        var jqxhr = $.get('/api/v1/projects?rows=1000', function (data) {
                //console.log('[/api/v1/projects/] : ', data);
                //console.log('[/api/v1/projects/ data.results[0] : ', data.results[0]);
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
    this.btnEvents = function () {
        // 체크박스 전체선택, 해제
        $(document).on('click', '#listContents th input[type=checkbox]', function (e) {
            //e.preventDefault(); 활성화 하면 체크 안됨!
            CheckAll($(this), '#listContents td input[type=checkbox]');
        });
        // 체크박스 전체선택, 해제
        $(document).on('click', '#listContents2 th input[type=checkbox]', function (e) {
            //e.preventDefault(); 활성화 하면 체크 안됨!
            CheckAll($(this), '#listContents2 td input[type=checkbox]');
        });
        // 프로젝트 참가자 삭제
        $('#listTitleGroup li:nth-of-type(1)').on('click', function () {
            if ($('#listContents table td:nth-of-type(1) input[type=checkbox]:checked').length > 0) {
                $('#listContents table td:nth-of-type(1) input[type=checkbox]:checked').each(function () {
                    var user = $(this).closest('tr').find('td:eq(1)').text();
                    var url = '/api/v1/projects/' + project_id + '/members/' + user;
                    console.log('[4512 url]');
                    console.log(url);
                    $.ajax({
                        url: url,
                        type: 'DELETE',
                        async: true,
                        success: function (res) {
                            console.log('[3362 res] : ', res);
                            if (res.result == 'OK') {
                                alert('참가자가 삭제 되었습니다.');
                                location.href = location.href;
                                //local.showList();
                            } else if (res.result == 463) {
                                // 463 : Founder can not be deleted!
                                alert('개설자는 삭제되지 않습니다.');
                                location.href = location.href;
                            }
                        },
                        error: function (e) {
                            alert('참가자가 삭제되지 않았습니다.');
                            console.log('[fail 4452]');
                            console.log(e.responseText);
                        }
                    });
                });
            } else {
                alert('선택된 사용자가 없습니다.');
            }
        });
        // 검색버튼 클릭
        $('#listTitleGroup2 li:nth-of-type(2)').on('click', function (e) {
            e.preventDefault();
            if ($('#txt_search').val().trim() == '') {
                alert('검색할 이메일을 입력해주세요.');
                $('#txt_search').focus();
                return false;
            }
            $.ajax({
                url: '/api/v1/search?q=' + $('#txt_search').val() + '&target=u',
                type: 'GET',
                async: true,
                success: function (res) {
                    console.log('[4594 res] : ', res);
                    //$('#listContents2 table tbody tr:nth-of-type(1)').next().empty();
                    var html = '';
                    html += '<tr>';
                    html += '<th>';
                    html += '    <input type="checkbox">';
                    html += '</th>';
                    html += '<th>번호</th>';
                    html += '<th>이름</th>';
                    html += '<th>이메일</th>';
                    html += '</tr>';

                    if (res.u == undefined || res.u == null) {
                        html += '<tr><td colspan=4 style="padding-top:10px;">존재하지 않는 사용자 입니다.</td></td>';
                    } else {
                        if (res.u.length < 1) {
                            html += '<tr><td colspan=4 style="padding-top:10px;">존재하지 않는 사용자 입니다.</td></td>';
                        } else {
                            $(res.u).each(function (idx, data) {
                                html += '<tr>';
                                html += '<td>';
                                html += '    <input type="checkbox">';
                                html += '</td>';
                                html += '    <td>' + data.user_id + '</td>';
                                html += '    <td>' + data.name + '</td>';
                                html += '    <td>' + data.email + '</td>';
                                html += '</tr>';
                            });
                        }
                    }
                    $('#listContents2 table tbody').empty().append(html);
                },
                error: function (e) {
                    console.log('fail 4265');
                    console.log(e.responseText);
                }
            });
        });
        // (검색 후)추가버튼 클릭
        $('#listTitleGroup2 li:nth-of-type(3)').on('click', function () {
            if ($('#listContents2 table td:nth-of-type(1) input[type=checkbox]:checked').length > 0) {
                $('#listContents2 table td:nth-of-type(1) input[type=checkbox]:checked').each(function () {
                    var user = $(this).closest('tr').find('td:eq(1)').text();
                    var url = '/api/v1/projects/' + project_id + '/members';
                    var data = {
                        mid: user,
                        can_read: 1,
                        can_modify: 1,
                        can_delete: 1,
                        can_create_doc: 1
                    };
                    $.ajax({
                        url: url,
                        type: 'POST',
                        data: data,
                        async: true,
                        success: function (res) {
                            console.log('[5469 res] : ', res);
                            if (res.result.toUpperCase() == 'OK') {
                                alert('참가자가 추가 되었습니다.');
                                location.href = location.href;
                                //local.showList();
                            }else if(res.result.toUpperCase() == 'DUP'){
                                alert('이미 초대된 사용자 입니다.');
                            }
                        },
                        error: function (e) {
                            alert('참가자가 추가되지 않았습니다.');
                            console.log('fail 5562');
                            console.log(e.responseText);
                        }
                    });
                });
            } else {
                alert('선택된 사용자가 없습니다.');
            }
        });
        // // 체크박스 전체선택, 해제
        // $('#listContents th input[type=checkbox]').on('click', function (e) {
        //     //e.preventDefault(); 활성화 하면 체크 안됨!
        //     CheckAll($(this), '#listContents td input[type=checkbox]');
        // });
        // $('#listContents2 th input[type=checkbox]').on('click', function (e) {
        //     //e.preventDefault(); 활성화 하면 체크 안됨!
        //     CheckAll($(this), '#listContents2 td input[type=checkbox]');
        // });
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
                url: '/api/v1/projects/' + project_id + '/members?page=' + page + '&rows=' + rows,
                type: 'GET',
                async: true,
                success: function (res) {
                    console.log('7784 [/api/v1/projects/' + project_id + '/members?page=' + page + '&rows=' + rows + '] : ', res);
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
                            html += '    <td>' + result.id + '</td>';

                            if (result.is_founder == 1) html += '    <td>' + result.name + ' <img src="/static/public/img/king.png" style="height:15px;"></td>';
                            else html += '    <td>' + result.name + '</td>';

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
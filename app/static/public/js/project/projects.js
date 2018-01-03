var PageScript = function () {
    var local = this;
    this.preInits = function () {};
    this.btnEvents = function () {};
    this.getProjects = function (lang) {
        $(document).ajaxStart(function () {
            $('#dvLoading2').show();
        });
        $(document).ajaxComplete(function (event, request, settings) {
            $('#dvLoading2').hide();
        });
        var jqxhr = $.get('/api/v1/users/1/projects/', function (data) {
                console.log('/api/v1/users/1/projects/ : ', data);
                // 좌측메뉴
                var menu = '',
                    list = '';
                if (data != undefined && data.result != '') {
                    menu += '<ul id="ulProjectList" style="max-height:200px;overflow-x:hidden;overflow-y:auto;">';
                    $(data.result).each(function (idx, res) {
                        menu += '<li>';
                        menu += '<a href="/static/front/project/project_view.html?project=' + res.project_id + '">└ ' + res.project_name + '</a>';
                        menu += '</li>';
                    });
                    menu += '</ul>';
                }
                // 본문리스트
                if (data != undefined && data.result != '') {
                    $(data.result).each(function (idx, res) {
                        list += '<tr>';
                        list += '   <td>' + parseInt(idx + 1) + '</td>';
                        list += '   <td style="max-width:150px;display: inline-block;white-space: nowrap;overflow:hidden;vertical-align:middle;">';
                        list += '       <a href="project_view.html?project=' + res.project_id + '">' + res.project_name + '</a>';
                        list += '   </td>';
                        list += '   <td>' + res.progress_percent + '</td>';
                        list += '   <td>' + res.status + '</td>';
                        list += '   <td style="max-width:150px;display: inline-block;white-space: nowrap;overflow:hidden;vertical-align:middle;">';
                        list += res.client_company + ' ';
                        if (res.clients != undefined) {
                            $(res.clients).each(function (idx, clients) {
                                list += ', ' + clients[idx];
                            });
                        }
                        list += '   </td>';

                        var ko_res_time = '',
                            ko_duration_date = '';
                        if (res.create_time != '') {
                            var dt1 = new Date(res.create_time);
                            ko_res_time = GetStringDate(dt1);
                        }
                        if (res.create_time != '') {
                            var dt2 = new Date(res.duration_date);
                            ko_duration_date = GetStringDate(dt2);
                        }

                        list += '   <td>' + ko_res_time + '</td>';
                        list += '   <td>' + ko_duration_date + '</td>';
                        list += '</tr>';
                    });
                }

                $('#left_menu_area>li:nth-of-type(1)').append(menu);
                $('#listContents table tbody tr').after(list);
                console.log('menu : ', menu);
                console.log('list : ', list);
            })
            .done(function () {})
            .fail(function () {
                alert("error 1245");
            })
            .always(function () {});
        jqxhr.always(function () {});
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
});
var PageScript = function () {
    var local = this,
        rows = IsValidStr(getUrlParameter('rows')) ? getUrlParameter('rows') : '20',
        page = IsValidStr(getUrlParameter('page')) ? getUrlParameter('page') : '1',
        project_id = getUrlParameter('project'),
        cur_path = $(location).attr('pathname');
    this.getProjects = function () {
        local.show();
        console.log('[current pc] : ', new Date());
        console.log('[current pc gmt basic] : ', new Date().toGMTString());
        var jqxhr_l = $.get('/api/v1/projects?rows=1000', function (data) {
                var menu = '',
                    list = '';
                if (data != undefined && data.result != '') {
                    menu += '<ul id="ulProjectList" style="max-height:200px;overflow-x:hidden;overflow-y:auto;">';
                    $(data.results).each(function (idx, res) {
                        menu += '<li>';
                        menu += '<a href="/static/front/project/project_view.html?project=' + res.id + '">└ ' + res.name + '</a>';
                        menu += '</li>';
                    });
                    menu += '</ul>';
                    $('#left_menu_area>li:nth-of-type(1)').append(menu);
                }
            })
            .done(function () {

            })
            .fail(function () {
                console.log("error 9958");
            })
            .always(function () {});
        jqxhr_l.always(function () {});
        var jqxhr = $.get('/api/v1/projects?rows=' + rows + '&page=' + page, function (data) {
                console.log('[/api/v1/projects?rows=' + rows + '&page=' + page + '] : ', data);
                console.log('[/api/v1/projects?rows=' + rows + '&page=' + page + ' data.results[0]] : ', data.results[0]);
                var menu = '',
                    list = '';
                if (data != undefined && data.result != '') {
                    $(data.results).each(function (idx, res) {
                        list += '<tr>';
                        list += '   <td>' + parseInt(idx + 1) + '</td>';
                        list += '   <td style="min-width:220px;display: inline-block;white-space: nowrap;overflow:hidden;vertical-align:middle;text-align:left;">';
                        list += '       <a href="project_view.html?project=' + res.id + '">' + res.name + '</a>';
                        list += '   </td>';
                        var prog = res.progress == undefined ? '0' : res.progress;
                        list += '   <td>' + prog + '%</td>';
                        list += '   <td>' + res.status + '</td>';
                        list += '   <td>' + res.founder + '</td>';

                        var ko_res_time = '',
                            ko_duration_date = '';
                        // if (res.create_time == null || res.create_time == '' || res.create_time == '1970-01-01 9:0') {
                        //     ko_res_time = '';
                        // }else{
                        //     var dt1 = new Date(res.create_time);
                        //     ko_res_time = GetStringDate(dt1);
                        // }
                        ko_res_time = GetDateText(res.create_time, '0', '1');

                        // if (res.due_date == null || res.due_date == '' || res.due_date == '1970-01-01 9:0') {
                        //     ko_duration_date = '제한없음';
                        // }else{
                        //     var dt2 = new Date(res.due_date);
                        //     ko_duration_date = GetStringDate(dt2);
                        // }
                        ko_duration_date = GetDateText(res.due_date, '1', '1');

                        list += '   <td>' + ko_res_time + '</td>';
                        list += '   <td>' + ko_duration_date + '</td>';
                        list += '</tr>';
                    });
                    $('#listContents table tbody tr').after(list);
                    var param_path = cur_path + '?rows=' + rows + '&';
                    SetPagebar(parseInt(data.total_cnt), rows, page, param_path, rows);
                }
            })
            .done(function () {

            })
            .fail(function () {
                console.log("error 5462");
            })
            .always(function () {});
        jqxhr.always(function () {
            local.hide();
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
    this.bind = function () {
        local.getProjects();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();
});
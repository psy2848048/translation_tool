var PageScript = function () {
    var local = this;
    this.getProjects = function () {
        console.log('[current pc] : ', new Date());
        console.log('[current pc gmt basic] : ', new Date().toGMTString());
        local.mask();

        $(document).ajaxStart(function () {
            $('#dvLoading2').show();
        });
        $(document).ajaxComplete(function (event, request, settings) {
            $('#dvLoading2').hide();
        });
        var jqxhr = $.get('/api/v1/7/projects/', function (data) {
                console.log('[/api/v1/7/projects/] : ', data);
                console.log('[/api/v1/7/projects/ data.results[0]] : ', data.results[0]);
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
                if (data != undefined && data.result != '') {
                    $(data.results).each(function (idx, res) {
                        list += '<tr>';
                        list += '   <td>' + parseInt(idx + 1) + '</td>';
                        list += '   <td style="max-width:150px;display: inline-block;white-space: nowrap;overflow:hidden;vertical-align:middle;">';
                        list += '       <a href="project_view.html?project=' + res.id + '">' + res.name + '</a>';
                        list += '   </td>';
                        list += '   <td>' + res.progress + '</td>';
                        list += '   <td>' + res.status + '</td>';
                        list += '   <td>' + res.founder + '</td>';

                        var ko_res_time = '',
                            ko_duration_date = '';
                        if (res.create_time != '') {
                            var dt1 = new Date(res.create_time);
                            ko_res_time = GetStringDate(dt1);
                        }
                        if (res.due_date != '') {
                            var dt2 = new Date(res.due_date);
                            ko_duration_date = GetStringDate(dt2);
                        }

                        list += '   <td>' + ko_res_time + '</td>';
                        list += '   <td>' + ko_duration_date + '</td>';
                        list += '</tr>';
                    });
                    $('#listContents table tbody tr').after(list);
                    SetPagebar(parseInt(data.total_count), 15, getUrlParameter('page') == undefined || getUrlParameter('page') == '' ? 1 : getUrlParameter('page'), $(location).attr('pathname') + '?', 10);
                }
            })
            .done(function () {

            })
            .fail(function () {
                console.log("error 5462");
            })
            .always(function () {});
        jqxhr.always(function () {});
    };
    this.mask = function () {
        $('#mask').css({
            'width': $(document).height(),
            'height': $(window).width()
        });
    };
    this.bind = function () {
        local.getProjects();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();
});
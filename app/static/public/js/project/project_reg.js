var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project');
    this.preInits = function () {
        SetMenuColor(getUrlParameter('project'), '프로젝트', '#ulProjectList li', '?project=', 'a', 'orange');

        setTimeout(function () {
            var menu = '';

            menu += '<ul id="ulProjectList">';
            menu += '<li>';
            menu += '<a href="/static/front/project/project_view.html?project=1">└ 내픽뉴스 영문번역</a>';
            menu += '</li>';
            menu += '<li>';
            menu += '<a href="/static/front/project/project_view.html?project=2">└ 내픽뉴스 중문번역</a>';
            menu += '</li>';
            menu += '</ul>';

            $('#left_menu_area>li:nth-of-type(1)').append(menu);

            if (project_id == undefined || project_id == '1') {
                $('#menuArea ul li ul li:nth-of-type(1) a').css({'color': 'orange'});
                $('#menuArea ul li ul li:nth-of-type(2) a').css({'color': '#333'});
            } else {
                $('#menuArea ul li ul li:nth-of-type(1) a').css({'color': '#333'});
                $('#menuArea ul li ul li:nth-of-type(2) a').css({'color': 'orange'});
            }
        }, 100);
    };
    this.btnEvents = function () {
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
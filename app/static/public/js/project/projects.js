var PageScript = function () {
    var local = this;
    this.preInits = function () {

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
        }, 100);
    };
    this.btnEvents = function () {

    };
    this.getProjects = function (lang) {
        $(document).ajaxStart(function () {
            $('#dvLoading2').show();
        });
        $(document).ajaxComplete(function (event, request, settings) {
            $('#dvLoading2').hide();
        });

        var jqxhr = $.get("http://ciceron.xyz:5000/api/v2/mypick/" + lang, function (data) {
                console.log(data);
            })
            .done(function () {})
            .fail(function () {
                alert("error");
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
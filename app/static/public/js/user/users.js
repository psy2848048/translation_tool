var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project');
    this.preInits = function () {
        // 좌측 프로젝트 리스트
        setTimeout(function () {
            var menu = '';

            menu += '<ul id="ulProjectList2 ">';
            menu += '<li>';
            menu += '<a href="/static/front/user/users.html?project=1">└ 내픽뉴스 영문번역</a>';
            menu += '</li>';
            menu += '<li>';
            menu += '<a href="/static/front/user/users.html?project=2">└ 내픽뉴스 중문번역</a>';
            menu += '</li>';
            menu += '</ul>';

            $('#left_menu_area>li:nth-of-type(4)').append(menu);

            if (project_id == undefined || project_id == '1') {
                $('#left_menu_area>li:nth-of-type(4) ul li:nth-of-type(1) a').css({'color': 'orange'});
                $('#left_menu_area>li:nth-of-type(4) ul li:nth-of-type(2) a').css({'color': '#333'});
            } else {
                $('#left_menu_area>li:nth-of-type(4) ul li:nth-of-type(1) a').css({'color': '#333'});
                $('#left_menu_area>li:nth-of-type(4) ul li:nth-of-type(2) a').css({'color': 'orange'});
            }
        }, 100);
    };
    this.btnEvents = function () { // 체크박스 전체선택, 해제 
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
    this.getUsers = function () {};
    this.bind = function () {
        local.preInits();
        local.btnEvents();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();

    $(document).tooltip({
        track: true
    });
});
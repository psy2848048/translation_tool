var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project');
    this.preInits = function () {
        // 좌측 프로젝트 리스트
        setTimeout(function () {
            var menu = '';

            menu += '<ul id="ulProjectList2" style="max-height:200px;overflow-x:hidden;overflow-y:auto;">';
            menu += '<li>';
            menu += '<a href="/static/front/user/users.html?project=1">└ 내픽뉴스 영문번역</a>';
            menu += '</li>';
            menu += '<li>';
            menu += '<a href="/static/front/user/users.html?project=2">└ 내픽뉴스 중문번역</a>';
            menu += '</li>';
            menu += '</ul>';

            $('#left_menu_area>li:nth-of-type(4)').append(menu);

            if (project_id == undefined || project_id == '1') {
                $('#left_menu_area>li:nth-of-type(4) ul li:nth-of-type(1) a').css({
                    'color': 'orange'
                });
                $('#left_menu_area>li:nth-of-type(4) ul li:nth-of-type(2) a').css({
                    'color': '#333'
                });
            } else {
                $('#left_menu_area>li:nth-of-type(4) ul li:nth-of-type(1) a').css({
                    'color': '#333'
                });
                $('#left_menu_area>li:nth-of-type(4) ul li:nth-of-type(2) a').css({
                    'color': 'orange'
                });
            }
        }, 100);
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
    this.getUsers = function () {};
    this.bind = function () {
        local.preInits();
        local.btnEvents();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();
});
$(function () {
    $('#rightMenuArticle').load('/static/front/common_html/right_top_menu.html ul');
    $('#menuArea').load('/static/front/common_html/left_menu.html ul');

    $(document).on('click', '#topSearch li img', function (e) {
        e.preventDefault();
        if ($('#total_search').val().trim().length < 2) {
            alert('검색어는 2자이상 입력하셔야 합니다.');
            $('#total_search').focus();
        } else {
            location.href = '/static/front/project/total_search.html?text=' + $(this).closest('li').find('input[type=text]').val();
        }
    });

    // 로그아웃 체크
    setTimeout(function () {
        if (_USER_ID == undefined || _USER_ID.trim() == '') {
            alert('로그아웃 상태입니다.');
            location.href = '/static/front/user/login.html';
            return false;
        }else{
            $('#sp_user_nick').text(_USER_NICK);
            $('#sp_user_email').text(_USER_ID);    
        }
    }, 1000);

    // // 우측상단 유저
    // setTimeout(function () {
    //     $('#sp_user_nick').text(_USER_NICK);
    //     $('#sp_user_email').text(_USER_ID);
    // }, 200);
});
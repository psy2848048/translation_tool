$(function () {
    getSession();
    
    $('#mainHeader').load('/static/front/common_html/main_header.html ul');
    $('#rightMenuArticle').load('/static/front/common_html/right_top_menu.html ul');
    $('#menuArea').load('/static/front/common_html/left_menu.html ul');
    $('#mainFooter').load('/static/front/common_html/main_footer.html ul, br');

    $(document).on('click', '#topSearch li img', function (e) {
        e.preventDefault();
        if ($('#total_search').val().trim().length < 2) {
            alert('검색어는 2자이상 입력하셔야 합니다.');
            $('#total_search').focus();
        } else {
            location.href = '/static/front/project/total_search.html?text=' + $(this).closest('li').find('input[type=text]').val();
        }
    });

    // 우측상단 유저
    setTimeout(function(){$('#sp_user_nick').text(_USER_ID);}, 200);
});
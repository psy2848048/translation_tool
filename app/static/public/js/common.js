// 특정 파라미터값 추출
function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

// 특정한 엘리먼트에 색깔 주기
function SetMenuColor(param, paramName, eachObj, compare_sentence, color_attr, color) {
    if (param == undefined || param == '') {
        alert(paramName + ' 정보가 없습니다.');
        history.back();
    } else {
        $(eachObj).each(function (idx, value) {
            if ($(value).html().indexOf(compare_sentence + param) != -1) {
                $(this).find(color_attr).css({
                    'color': color
                });
            }
        });
    }
}

// null 을 공백으로 치환
function NullToEmpty(s) {
    if (s == null) return '';
    else return s;
}

// 전체선택, 전체해제
// checkerObj : 전체선택, 해제 체크박스
// checkboxes : 선택 및 해제 될 체크박스들
function CheckAll(checkerObj, checkboxes) {
    var is_check = $(checkerObj).prop('checked');
    $(checkboxes).prop('checked', is_check);
}

$(function () {
    $('#mainHeader').load('/static/front/common_html/main_header.html ul');
    $('#rightMenuArticle').load('/static/front/common_html/right_top_menu.html ul');
    $('#menuArea').load('/static/front/common_html/left_menu.html ul');
    $('#mainFooter').load('/static/front/common_html/main_footer.html ul, br');

    $(document).on('click', '#topSearch li img', function () {
        location.href = '/static/front/project/total_search.html?text=' + $(this).closest('li').find('input[type=text]').val();
    });
});
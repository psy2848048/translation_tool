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

// date 타입을 string 타입으로 전환
function GetStringDate(date) {
    var strMonth = parseInt(date.getMonth()) + parseInt(1);
    var strToday = date.getFullYear() + '-' + strMonth + '-' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes();
    return strToday;
}

// 년,월,일,시,분 동적폼
// id 로 지정되어 있기 때문에 한 화면에서 한번만 사용 주의!
function SetDateSelect(maxYear, minuteBlock) {
    var result = '';
    var currentDate = new Date();

    // 년
    result += '<select id="sel_year">';
    result += '    <option value="">년도</option>';
    for (var i = currentDate.getFullYear(); i <= maxYear; i++) {
        result += '    <option value="' + i + '">' + i + '</option>';
    }
    result += '</select>';

    // 월
    // 년도별 2월 마지막날
    // 2018 : 28
    // 2019 : 28
    // 2020 : 29
    // 2021 : 28
    // 2022 : 28
    // 2023 : 28
    // 2024 : 29
    // 2025 : 28
    // 2026 : 28
    // 2027 : 28
    // 2028 : 29
    result += '<select id="sel_month">';
    result += '    <option value="">월</option>';
    for (var j = 1; j < 13; j++) {
        if (j < 10) result += '    <option value="0' + j + '">0' + j + '</option>';
        else result += '    <option value="' + j + '">' + j + '</option>';
    }
    result += '</select>';

    // 일
    result += '<select id="sel_day">';
    result += '    <option value="">일</option>';
    for (var k = 1; k < 32; k++) {
        if (k < 10) result += '    <option value="0' + k + '">0' + k + '</option>';
        else result += '    <option value="' + k + '">' + k + '</option>';
    }
    result += '</select>';

    // 시
    result += '<select>';
    result += '    <option value="">시</option>';
    for (var l = 0; l < 24; l++) {
        if (l < 10) result += '    <option value="0' + l + '">0' + l + '</option>';
        else result += '    <option value="' + l + '">' + l + '</option>';
    }
    result += '</select>';

    // 분
    result += '<select>';
    result += '    <option value="">분</option>';
    for (var m = 0; m < 60; m++) {
        if (m % minuteBlock == 0) {
            if (m < 10) result += '    <option value="0' + m + '">0' + m + '</option>';
            else result += '    <option value="' + m + '">' + m + '</option>';
        }
    }
    result += '</select>';

    return result;
}
// 월 선택 : 윤달에 따른 2월의 일수 자동으로 변경
$(document).on('change', '#sel_year, #sel_month', function () {
    var maxK = 0;
    if ($('#sel_month').val() % 2 == 0) {
        if ($('#sel_month').val() == 2) {
            if ($('#sel_year').val() == 2020 || $('#sel_year').val() == 2024 || $('#sel_year').val() == 2028) maxK = 30;
            else maxK = 29;
        } else maxK = 31;
    } else {
        maxK = 32;
    }
    var result = '    <option value="">일</option>';
    for (var k = 1; k < maxK; k++) {
        if (k < 10) result += '    <option value="0' + k + '">0' + k + '</option>';
        else result += '    <option value="' + k + '">' + k + '</option>';
    }
    $('#sel_day').empty();
    $('#sel_day').html(result);
});

// null 을 공백으로 치환
function NullToEmpty(s){
    if(s == null) return '';
    else return s;
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
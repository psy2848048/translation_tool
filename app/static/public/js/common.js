var _OFFSET = new Date().getTimezoneOffset(); 

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


// date 타입을 string 타입으로 전환
function GetStringDate(date, format) {
    if(date == undefined || date == null) return '';

    format = format == undefined || format == null || format.trim() == '' ? '0' : format; // 콤마주의!
    var strMonth = parseInt(date.getMonth()) + parseInt(1);
    strMonth = strMonth < 10 ? '0' + strMonth.toString() : strMonth;
    var strDay = parseInt(date.getDate()) < 10 ? '0' + date.getDate().toString() : date.getDate().toString();
    var strHour = parseInt(date.getHours()) < 10 ? '0' + date.getHours().toString() : date.getHours().toString();
    var strMinute = parseInt(date.getMinutes()) < 10 ? '0' + date.getMinutes().toString() : date.getMinutes().toString();
    var result = '';
    switch(format){
        case '0': // 2018-01-11 9:7
            result = date.getFullYear() + '-' + strMonth + '-' + strDay + ' ' + parseInt(strHour) + ':' + parseInt(strMinute);
        break;
        case '1': // 2018-01-11 09:07
            result = date.getFullYear() + '-' + strMonth + '-' + strDay + ' ' + strHour + ':' + strMinute;
        break;
    }
    return result;
}


jQuery.fn.center = function () {
    this.css("position", "absolute");
    this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2 - 100) + $(window).scrollTop()) +
        "px");
    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + $(window).scrollLeft()) +
        "px");
    return this;
};

function getFileExtension(file_name) {
    var result;
    //console.log('[6652] file_name : ', file_name);
    //console.log('[1145] file_name.length : ', file_name.length);
    //console.log('[2415] file_name.lastIndexOf(".") : ', file_name.lastIndexOf('.'));
    if (file_name != undefined && file_name.length > 0 && file_name.lastIndexOf('.') != -1) {
        result = file_name.substring(file_name.lastIndexOf('.') + 1, file_name.length).toUpperCase();
        //console.log('[5487] result : ', result);
        return result;
    } else {
        //console.log('[8526] result : ', result);
        return '';
    }
}

function onFileSelect(id, server_url, max_mb_size, reg_ext, ext_msg) {
    var fileUpload = id.get(0);
    var files = fileUpload.files;
    var f_data = new FormData();
    var is_allowed_ext = false;
    for (var i = 0; i < files.length; i++) {
        /* 사이즈 체크 */
        var fileSize = files[i].size;
        var mega = max_mb_size; // 메가
        var maxFilesize = parseInt(mega) * 1025 * 1000;
        if (fileSize > maxFilesize) {
            alert('파일당 최대용량은 ' + mega + '메가 입니다.');
            break;
        }
        /* 확장자 체크 */
        var ext = getFileExtension(files[i].name);
        //console.log('[1254] ext : ', ext);
        if (ext == '') alert('파일 확장자에 문제가 있습니다!');
        else {
            for (var j = 0; j < reg_ext.length; j++) {
                //alert(reg_ext[j].toUpperCase());
                if (reg_ext[j].toUpperCase() == ext) {
                    //alert(0);
                    is_allowed_ext = true;
                    continue;
                }
            }
        }
    }
    if (is_allowed_ext) {
        $.ajax({
            url: server_url,
            type: "POST",
            contentType: false,
            processData: false,
            data: f_data,
            // dataType: "json",
            success: function (result) {
                console.log('[4576] result : ', result);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log('[9786] xhr.status : ', xhr.status);
                console.log('[6458] thrownError : ', thrownError);
                console.log('[3197] xhr.responseText : ', xhr.responseText);
            }
        });
    } else {
        alert(ext_msg);
        id.val('');
        return false;
    }
}

function IsValidObj(o){
    if(o == undefined || o == null) return false;
    else return true;
}
function IsValidStr(s){
    if(s == undefined || s == null || s == '') return false;
    else return true;
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
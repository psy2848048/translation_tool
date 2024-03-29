function checkBrowserType() {   
    var bCR = new RegExp(/Chrome/).test(navigator.userAgent); // Google Chrome
    var bIE = new RegExp(/MSIE/).test(navigator.userAgent); // MS Internet Explorer
    var bFF = new RegExp(/Firefox/).test(navigator.userAgent); // Mozilla Firefox
    var bNS = new RegExp(/Netscape/).test(navigator.userAgent); // Mozilla Netscape

    if (bCR) {
        //alert("크롬");
    } else {
        if (bIE) {
            //alert("인터넷 익스플로러");
        } else if (bFF) {
            //alert("파이어폭스");
        } else if (bNS) {
            //alert("넷스케이프");
        } else {
            //alert("기타 브라우저");
        }
        alert('마이캣툴 Ver.1은 웹표준에 최적화 된 크롬 브라우저만 지원합니다.\n\n크롬 브라우저로 접속 바랍니다!');
        location.href='/static/front/browser_err.html';
    }
}

var _OFFSET = new Date().getTimezoneOffset();
var _USER_ID = '',
    _USER_NICK = '',
    _USER_PICTURE;  


// 특정 파라미터값 추출
function getUrlParameter(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));    
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
    if (date == undefined || date == null) return '';

    format = format == undefined || format == null || format == '' ? '0' : format; // 콤마주의!
    var strMonth = parseInt(date.getMonth()) + parseInt(1);
    strMonth = strMonth < 10 ? '0' + strMonth.toString() : strMonth;
    var strDay = parseInt(date.getDate()) < 10 ? '0' + date.getDate().toString() : date.getDate().toString();
    var strHour = parseInt(date.getHours()) < 10 ? '0' + date.getHours().toString() : date.getHours().toString();
    var strMinute = parseInt(date.getMinutes()) < 10 ? '0' + date.getMinutes().toString() : date.getMinutes().toString();
    var result = '';
    switch (format) {
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
    if (file_name != undefined && file_name.length > 0 && file_name.lastIndexOf('.') != -1) {
        result = file_name.substring(file_name.lastIndexOf('.') + 1, file_name.length).toUpperCase();
        return result;
    } else {
        return '';
    }
}

function onFileSelect(id, server_url, max_mb_size, reg_ext, ext_msg, result_p) {
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
        f_data.append('file', files[i]);
    }
    if (is_allowed_ext) {
        $.ajax({
            url: server_url,
            type: "POST",
            contentType: false,
            processData: false,
            data: f_data,
            // dataType: "json",
            success: function (res) {
                if (res.result == 'OK') {
                    $('#' + result_p).text('업로드가 완료되었습니다.');
                    setTimeout(hidePopup, 1000);
                } else $(result_p).text('업로드에 문제가 있습니다.');
            },
            error: function (xhr, ajaxOptions, thrownError) {
                $(result_p).text('업로드에 문제가 있습니다.');
            }
        });
    } else {
        alert(ext_msg);
        id.val('');
        return false;
    }
}

function hidePopup() {
    $('#mainWrap').css('opacity', '1');
    $("#upload_div").fadeOut('slow');
    location.href = location.href;
}

function IsValidObj(o) {
    if (o == undefined || o == null) return false;
    else return true;
}

function IsValidStr(s) {
    if (s == undefined || s == null || $.trim(s) == '') return false;
    else return true;
}

// 날짜용도와 타입에 따른 결과 반환
function GetDateText(o, purpose, format) {
    //alert(format);
    if (purpose == 1) {
        if (o == null || o == '' || o == '1970-01-01 9:0') {
            return '제한없음';
        } else {
            var dt1 = new Date(o);
            return GetStringDate(dt1, format);
        }
    } else {
        if (o == null || o == '' || o == '1970-01-01 9:0') {
            return '';
        } else {
            var dt2 = new Date(o);
            return GetStringDate(dt2, format);
        }
    }
}

// 이메일 정규식
function CheckEmail(email) {
    var is_ok = false;

    var regExp = /^[0-9a-zA-Z]([\-.\w]*[0-9a-zA-Z\-_+])*@([0-9a-zA-Z][\-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9}$/;
    if (email.match(regExp) != null) is_ok = true;

    return is_ok;
}

// 로그아웃
function logout() {
    $.ajax({
        url: '/api/v1/auth/signout',
        type: 'GET',
        async: true,
        success: function (res) {
            if (res.result == 200) {
                alert(res.result_ko);
                location.href = '/';
            }
        },
        error: function (err) {
            alert('로그아웃에 실패했습니다.\n\n급할경우 브라우저를 모두 닫아도 로그아웃 됩니다.');
        }
    });
}

// 세션값 가져오기
function getSession() {
    $.ajax({
        url: '/api/v1/auth/check',
        type: 'GET',
        async: true,
        success: function (res) {
            $('#sp_user_email').text(res.user_id);  
            $('#sp_user_nick').text(res.user_nickname);
            //$('.circle').css({'background':'url('+ res.user_picture +')'}); // 프로필사진 

            _USER_ID = res.user_id;
            _USER_NICK = res.user_nickname;
            _USER_PICTURE = res.user_picture;

            $('#hd_id').val(res.user_id);
            $('#hd_nick').val(res.user_nickname);
            $('#hd_picture').val(res.user_picture);
        },
        error: function (e) {
        }
    });
}
function mask() {
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();

    $('#mask').css({
        'width': maskWidth,
        'height': maskHeight
    }).show();
}
// 공통 ajax
// url = 실행할 url
// method = POST, GET, PUT, DELETE...
// data : 넘길 데이타
//var AjaxExecute = function (url, method, data) {
var AjaxExecute = function (url, method, data) {
    var result = '';
    $.ajax({
        url: url,
        type: method,
        data: data,
        async: false, // 변경 시 값이 넘어오지 않을 수 있음!!
        success: function (res) {
            result = res;  

            //console.log('##### AjaxExecute Success #####');
            //console.log(res);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            if(IsValidStr(xhr.result_ko)) result = xhr.result_ko;
            else result = 'err';

            //console.log('##### AjaxExecute Error #####');
            //console.log('### xhr ###');
            //console.log(xhr);
            //console.log('### xhr.status ###');
            //console.log(xhr.status);
            //console.log('### xhr.responseText ###');
            //console.log(xhr.responseText);
            //console.log('### thrownError ###');
            //console.log(thrownError);
            //console.log('### ajaxOptions ###');
            //console.log(ajaxOptions);
        }
    });        
    return result;
};

// 날짜객체를 스트링 형식으로 반환
function ConvertDateToString(date){
    return date.getFullYear() + '년 ' + parseInt(date.getMonth()+1) + '월 ' + date.getDate() + '일 ' + date.getHours() + '시 ' + date.getMinutes() + '분';
}

// 바이너리 이미지 받기
function hexToBase64(str) {
    return btoa(String.fromCharCode.apply(null, str.replace(/\r|\n/g, "").replace(/([\da-fA-F]{2}) ?/g, "0x$1 ").replace(/ +$/, "").split(" ")));
}

// ReplaceAll prototype 선언
String.prototype.ReplaceAll = function(org, dest) {
    return this.split(org).join(dest);
};      

// 개행문자 제거
function RemoveBr(value){
    value = value.replace(/\n/g, " "); // 행바꿈제거
    value = value.replace(/\r/g, " "); // 엔터제거
    return value;
}

$(function () {
    checkBrowserType();

    $('#mainHeader').load('/static/front/common_html/main_header.html ul');
    $('#mainFooter').load('/static/front/common_html/main_footer.html ul, br');

    getSession();
});
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

$(function () {
    $('#mainHeader').html('<ul> <li> <img src="/public/img/marocat_logo.png" style="cursor:pointer;" onclick="javascript:location.href=\'/index.html\';"> </li> </ul> <ul> <li> <a href="/app/product/marocat.html">제품소개</a> </li> <li> <a href="/app/question/faq.html">FAQ</a> </li> <li> <a href="/app/buy/marocat.html">제품구매</a> </li> <li> <a href="/app/user/login.html">로그인</a> </li> </ul>');
    $('#rightMenuArticle').html('<input type="text" id="txtSearchWord" placeholder=" 프로젝트, 작업 검색... "> <ul id="rightMenu"> <li> <span class="circle"></span>&nbsp;&nbsp;</li> <li id="spUser">(주)민국번역 홍길동</li> </ul>');
    $('#menuArea').html('<ul id="logoArea"> <li> <img src="/public/img/marocat_logo.png" style="cursor:pointer;" onclick="javascript:location.href=\'/index.html\';"> </li> </ul> <ul> <li> <a href="/app/project/projects.html"> <i class="fa fa-folder" aria-hidden="true"></i> 프로젝트</a> <ul id="ulProjectList" style="display:none;"> <li> <a href="/app/project/project_view.html?project=1">└ 내픽뉴스 영문번역</a> </li> <li> <a href="/app/project/project_view.html?project=2">└ 내픽뉴스 중문번역</a> </li> </ul> </li> <li> <a href="/app/tran_memory/tran_memory.html"> <i class="fa fa-list-alt" aria-hidden="true"></i> 번역메모리</a> </li> <li> <a href="/app/word_db/word_db.html"> <i class="fa fa-database" aria-hidden="true"></i> 용어 데이터베이스</a> </li> <li> <a href="/app/user/users.html"> <i class="fa fa-users" aria-hidden="true"></i> 프로젝트 참가자</a> <ul id="ulProjectList2" style="display:none;"> <li> <a href="users.html?project=1">└ 내픽뉴스 영문번역</a> </li> <li> <a href="users.html?project=2">└ 내픽뉴스 중문번역</a> </li> </ul> </li> <li> <a href="/app/user/userinfo.html"> <i class="fa fa-user" aria-hidden="true"></i> 나의정보</a> </li> </ul>');
    $('#mainFooter').html('<ul> <li> <a target="_blank" href="/app/terms.html">이용약관</a> </li> <li>|</li> <li> <a target="_blank" href="/app/privacy.html">개인정보취급방침</a> </li> <li>|</li> <li> <a target="_blank" href="https://goo.gl/forms/cQMkN2gpYXOBtruz2">문의하기</a> </li> </ul> <br> <ul> <li>주식회사 씨세론</li> <li>|</li> <li>대표이사 : 윤영선</li> <li>|</li> <li>개인정보관리책임자 : 이준행</li> </ul> <br> <ul> <li>사업자등록번호 : 367-81-00182</li> <li>|</li> <li>통신판매업신고번호 : 제 2016-서울중구-0676</li> <li>|</li> <li>대표번호 : (+82)2-6441-3838</li> </ul> <br> <p>COPYRIGHT ⓒ CICÉRON All RIGHTS RESERVED.</p>');
});
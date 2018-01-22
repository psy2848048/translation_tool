var PageScript = function () {
    var local = this;
    this.preInits = function () {
        local.getSearchs();
    };
    this.btnEvents = function () {
    };
    this.getSearchs = function () {
        // 프로젝트
        var jqxhr = $.get('/api/v1/search/?q=' + getUrlParameter('text') + '&target=p', function (result) {
                console.log(result); 
                if(result.p == null || result.p == undefined || result.p.length < 1){
                    $('#s_project').html('프로젝트 검색결과가 없습니다.');
                }else{
                    var html = '';
                    html += '<ul>';
                    $(result.p).each(function(idx, res){
                        html += '    <li>' + res.name + '</li>';
                    });
                    html += '</ul>';
                    $('#s_project').html(html);
                }
            })
            .done(function () {})
            .fail(function () {
                alert("error 5485");
            })
            .always(function () {});
        jqxhr.always(function () {});

        // 프로젝트 문서
        var jqxhr2 = $.get('/api/v1/search/?q=' + getUrlParameter('text') + '&target=d', function (result) {
                console.log(result); 
                if(result.d == null || result.d == undefined || result.d.length < 1){
                    $('#s_doc').html('프로젝트 문서 검색결과가 없습니다.');
                }else{
                    var html = '';
                    html += '<ul>';
                    $(result.d).each(function(idx, res){
                        html += '    <li>' + res.title + '</li>';
                    });
                    html += '</ul>';
                    $('#s_doc').html(html);
                }
            })
            .done(function () {})
            .fail(function () {
                alert("error 4956");
            })
            .always(function () {});
        jqxhr2.always(function () {});

        // 사용자
        var jqxhr3 = $.get('/api/v1/search/?q=' + getUrlParameter('text') + '&target=u', function (result) {
                console.log(result); 
                if(result.u == null || result.u == undefined || result.u.length < 1){
                    $('#s_user').html('사용자 검색결과가 없습니다.');
                }else{
                    var html = '';
                    html += '<ul>';
                    $(result.u).each(function(idx, res){
                        html += '    <li>' + res.name + '</li>';
                    });
                    html += '</ul>';
                    $('#s_user').html(html);
                }
            })
            .done(function () {})
            .fail(function () {
                alert("error 6535");
            })
            .always(function () {});
        jqxhr3.always(function () {});

        // 단어
        var jqxhr4 = $.get('/api/v1/search/?q=' + getUrlParameter('text') + '&target=tb', function (result) {
                console.log(result);
                if(result.tb == null || result.tb == undefined || result.tb.length < 1){
                    $('#s_tb').html('단어 검색결과가 없습니다.');
                }else{
                    var html = '';
                    html += '<ul>';
                    $(result.tb).each(function(idx, res){
                        html += '    <li>' + res.origin_text + ' : ' + res.trans_text + '</li>';
                    });
                    html += '</ul>';
                    $('#s_tb').html(html);
                }
            })
            .done(function () {})
            .fail(function () {
                alert("error 1576");
            })
            .always(function () {});
        jqxhr4.always(function () {});

        // 문장
        var jqxhr5 = $.get('/api/v1/search/?q=' + getUrlParameter('text') + '&target=tm', function (result) {
                console.log(result); 
                if(result.tm == null || result.tm == undefined || result.tm.length < 1){
                    $('#s_tm').html('문장 검색결과가 없습니다.');
                }else{
                    var html = '';
                    html += '<ul>';
                    $(result.tm).each(function(idx, res){
                        html += '    <li>' + res.origin_text + ' : ' + res.trans_text + '</li>';
                    });
                    html += '</ul>';
                    $('#s_tm').html(html);
                }
            })
            .done(function () {})
            .fail(function () {
                alert("error 9468");
            })
            .always(function () {});
        jqxhr5.always(function () {});
    };
    this.bind = function () {
        local.preInits();
        local.btnEvents();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();

    setTimeout(SearchInIt, 200);
});
function SearchInIt(){
    $('#total_search').val(getUrlParameter('text'));
}
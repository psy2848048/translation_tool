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
                console.log(result); // Not Found!!!!!
            })
            .done(function () {})
            .fail(function () {
                alert("error 4596");
            })
            .always(function () {});
        jqxhr.always(function () {});

        // 프로젝트 문서
        var jqxhr2 = $.get('/api/v1/search/?q=' + getUrlParameter('text') + '&target=d', function (result) {
                console.log(result); // Not Found!!!!!
            })
            .done(function () {})
            .fail(function () {
                alert("error 4956");
            })
            .always(function () {});
        jqxhr2.always(function () {});

        // 사용자
        var jqxhr3 = $.get('/api/v1/search/?q=' + getUrlParameter('text') + '&target=u', function (result) {
                console.log(result); // Not Found!!!!!
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
            })
            .done(function () {})
            .fail(function () {
                alert("error 1576");
            })
            .always(function () {});
        jqxhr4.always(function () {});

        // 문장
        var jqxhr5 = $.get('/api/v1/search/?q=' + getUrlParameter('text') + '&target=tm', function (result) {
                console.log(result); // Not Found!!!!!
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
var PageScript = function () {
    var local = this;
    this.preInits = function () {
        local.getSearchs();
    };
    this.btnEvents = function () {
    };
    this.getSearchs = function () {
        // 프로젝트
        var jqxhr = $.get('/api/v1/search/project?text=' + getUrlParameter('text'), function (result) {
                console.log(result); // Not Found!!!!!
            })
            .done(function () {})
            .fail(function () {
                alert("error 4596");
            })
            .always(function () {});
        jqxhr.always(function () {});

        // 프로젝트 문서
        var jqxhr2 = $.get('/api/v1/search/project_doc?text=' + getUrlParameter('text'), function (result) {
                console.log(result); // Not Found!!!!!
            })
            .done(function () {})
            .fail(function () {
                alert("error 4956");
            })
            .always(function () {});
        jqxhr2.always(function () {});

        // 사용자
        var jqxhr3 = $.get('/api/v1/search/user?text=' + getUrlParameter('text'), function (result) {
                console.log(result); // Not Found!!!!!
            })
            .done(function () {})
            .fail(function () {
                alert("error 6535");
            })
            .always(function () {});
        jqxhr3.always(function () {});

        // 단어
        /*var jqxhr4 = $.get('/api/v1/search/word?text=' + getUrlParameter('text'), function (result) {
                console.log(result);
            })
            .done(function () {})
            .fail(function () {
                alert("error 1576");
            })
            .always(function () {});
        jqxhr4.always(function () {});*/

        // 문장
        var jqxhr5 = $.get('/api/v1/search/sentence?text=' + getUrlParameter('text'), function (result) {
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
});
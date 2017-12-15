var PageScript = function () {
    var local = this;
    this.preInits = function () {};
    this.btnEvents = function () {

    };
    this.getProjects = function (lang) {
        $(document).ajaxStart(function () {
            $('#dvLoading2').show();
        });
        $(document).ajaxComplete(function (event, request, settings) {
            $('#dvLoading2').hide();
        });

        var jqxhr = $.get("http://ciceron.xyz:5000/api/v2/mypick/" + lang, function (data) {
                console.log(data);
            })
            .done(function () {})
            .fail(function () {
                alert("error");
            })
            .always(function () {});
        jqxhr.always(function () {});
    };
    this.bind = function () {
        local.preInits();
        local.btnEvents();
        local.getProjects(getUrlParameter('project'));
    };
};
$(function () {
    var script = new PageScript();
    script.bind();

    $('#ulProjectList').show();
});
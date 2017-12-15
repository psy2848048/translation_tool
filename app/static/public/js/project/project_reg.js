var PageScript = function () {
    var local = this;
    this.preInits = function () {
        SetMenuColor(getUrlParameter('project'), '프로젝트', '#ulProjectList li', '?project=', 'a', 'orange');
    };
    this.btnEvents = function () {
        $('#mainArea input[type=button]').on('click', function () {
            var data = {
                // example!
                "project_id": 1,
                "doc_title": $('#txt_title').val(),
                "doc_content": $('#mainArea textarea').val()
            };
            $.ajax({
                url: 'http://52.196.164.64/translate',
                type: 'post',
                data: data,
                async: true,
                success: function (args) {
                    alert(args);
                    location.href = 'project_view.html?project=' + getUrlParameter('project');
                },
                error: function (e) {
                    alert('fail');
                    console.log(e.responseText);
                    location.href = 'project_view.html?project=' + getUrlParameter('project');
                }
            });
        });
    };
    this.bind = function () {
        local.preInits();
        local.btnEvents();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();

    $('#ulProjectList').show();
});
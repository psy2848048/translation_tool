var pageScript = function () {
    var local = this;
    this.preEvent = function () {
        //var ver = getUrlParameter('ver');
        //var lang = getUrlParameter('lang');
        //if(ver != undefined && ver.trim() != '') $('#selVersion').val(ver);
        //if(lang != undefined && lang.trim() != '') $('#selLang').val(lang);
    };
    this.clickEvents = function () {
        $('#googleLink').on('click', function () {
            var url = '/api/v1/auth/google/signin';
            //location.href = 'signup.html?type=g';
            $.ajax({
                url: url,
                type: 'GET',
                //data: data,
                async: true,
                success: function (res) {
                    console.log('##### res #####');
                    console.log(res);
                },
                error: function (err) {
                    console.log('##### err #####');
                    console.log(err);
                }
            });
        });
        $('#facebookLink').on('click', function () {
            var url = '/api/v1/auth/facebook/signin';
            //location.href = 'signup.html?type=g';
            $.ajax({
                url: url,
                type: 'GET',
                //data: data,
                async: true,
                success: function (res) {
                    console.log('##### res #####');
                    console.log(res);
                },
                error: function (err) {
                    console.log('##### err #####');
                    console.log(err);
                }
            });
        });
    };
    this.bind = function () {
        local.preEvent();
        local.clickEvents();
    };
};
$(function () {
    var script = new pageScript();
    script.bind();
});
var pageScript = function(){
    var local = this;
    this.preEvent = function(){
        var ver = getUrlParameter('ver');
        var lang = getUrlParameter('lang');
        if(ver != undefined && ver.trim() != '') $('#selVersion').val(ver);
        if(lang != undefined && lang.trim() != '') $('#selLang').val(lang);
    };
    this.bind = function(){
        local.preEvent();
    };
};
$(function(){
    var script = new pageScript();
    script.bind();
});
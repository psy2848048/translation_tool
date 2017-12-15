var pageScript = function(){
    var local = this;
    this.clickEvent = function(){
        $('#loginBtn').on('click', function(){
            if(1 == 1) location.href='/project/projects.html';
            else alert('로그인정보 불일치!');
        });
    };
    this.bind = function(){
        local.clickEvent();
    };
};
$(function(){
    var script = new pageScript();
    script.bind();
});
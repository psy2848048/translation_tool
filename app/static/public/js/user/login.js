var pageScript = function(){
    var local = this;
    this.clickEvent = function(){
        $('#loginBtn').on('click', function(){
            if($('#txt_id').val() == 'ciceron' && $('#txt_pass').val() == 'ciceron8888') location.href='/static/front/project/projects.html';
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
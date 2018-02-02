var pageScript = function(){
    var local = this;
    this.btnClickEvents = function(){
        $('#nick_btn').on('click', function(){
            alert('닉네임');
        });
        $('#name_btn').on('click', function(){
            alert('업로드');
        });
        $('#email_btn').on('click', function(){
            alert('자체계정 연동하기');
        });
        $('#google_btn').on('click', function(){
            alert('구글 연동하기');
        });
        $('#facebook_btn').on('click', function(){
            alert('페이스북 연동하기');
        });
        $('#remove_btn').on('click', function(){
            alert('탈퇴하기');
        });
    };
    this.bind = function(){
        local.btnClickEvents();
    };
};
$(function(){
    var script = new pageScript();
    script.bind();
});